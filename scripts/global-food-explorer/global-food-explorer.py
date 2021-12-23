# This script takes three input files and combines them into a big explorer spreadsheet for the global food explorer.
# The files are:
# - (1) global-food-explorer.template.tsv: A template file that contains the header and footer of the spreadsheet, together with some placeholders.
# - (2) foods.tsv: a list of foods and their singular and plural names.
# - (3) views-per-food.tsv: a list of all available views for every food, including subtitle etc. The title can contain placeholders which are then filled out with the food name.
# This is all further complicated by the fact that we have different tag for food products, which enable views with different columns, units and subtitles.
# We take the cartesian product between (2) and (3) - according to the tag -, sprinkle some magic dust to make the titles work, and then place that massive table into the template (1).

# %%
from string import Template
import pandas as pd
import numpy as np
import textwrap
from os import path
import sys

outfile = "../../explorers/global-food.explorer.tsv"

default_view = '`Food Dropdown` == "Maize (Corn)" and `Metric Dropdown` == "Production" and `Per Capita Checkbox` == "false"'

# %%

# BASE_URI = 'https://catalog.ourworldindata.org'  # CDN
BASE_URI = "https://owid-catalog.nyc3.digitaloceanspaces.com"  # origin


def food_url(food):
    return f"{BASE_URI}/garden/explorers/2021/food_explorer/{food}.csv"


def substitute_title(row):
    # The title can include placeholders like ${food_singular}, which will be replaced with the actual food name here.
    food_slug = row["tableSlug"]
    food_names = foods_df.loc[food_slug]
    for key in ["title", "subtitle"]:
        if isinstance(row[key], str):
            template = Template(row[key])
            row[key] = template.substitute(
                food_singular=food_names["singular"],
                food_singular_lower=food_names["singular"].lower(),
                food_plural=food_names["plural"],
                food_plural_lower=food_names["plural"].lower(),
            )
    return row


def table_def(food):
    return f"table\t{food_url(food)}\t{food}"
    # return f"table\t{food_url('apples' if random.randint(0, 1) == 0 else 'bananas')}\t{food}"


# %%
with open("global-food-explorer.template.tsv", "r") as templateFile:
    template = Template(templateFile.read())
foods_df = pd.read_csv("foods.csv", index_col="slug")
views_df = pd.read_csv("views-per-food.csv", dtype=str)

print(f"🥝 Read {len(foods_df.index)} fruits")
print(f"📑 Read {len(views_df.index)} different views")

# %%
# convert comma-separated list of tags to an actual list, such that we can explode and merge by tag
views_df["_tags"] = views_df["_tags"].apply(lambda x: x.split(" "))
views_df = views_df.explode("_tags").rename(columns={"_tags": "_tag"})
views_df["_tag"] = views_df["_tag"].str.strip()

foods_rename = {
    **{col: col for col in foods_df.columns},
    "dropdown": "Food Dropdown",
    "slug": "tableSlug",
    "singular": None,
    "plural": None,
    "_tags": "_tags",
}
foods_rename = {k: v for k, v in foods_rename.items() if v is not None}

foods = foods_df.reset_index()[foods_rename].rename(columns=foods_rename)
foods["_tags"] = foods["_tags"].apply(lambda x: x.split(" "))
foods = foods.explode("_tags").rename(columns={"_tags": "_tag"})

food_tags = set(foods["_tag"])
view_tags = set(views_df["_tag"])
tags = food_tags | view_tags
print(f"🏷️ Found {len(tags)} tags: {', '.join(tags)}")

symmetric_diff = food_tags.symmetric_difference(view_tags)
if len(symmetric_diff) > 0:
    print(
        f"⚠️ Found {len(symmetric_diff)} tags that only appear in one of the input files: {', '.join(symmetric_diff)}"
    )

# %%
# merge on column: _tag
graphers = views_df.merge(foods).apply(substitute_title, axis=1)
graphers = graphers.drop(columns="_tag").sort_values(by="Food Dropdown", kind="stable")
# drop duplicates introduced by the tag merge
graphers = graphers.drop_duplicates()

print(f"📈 Generated {len(graphers.index)} views")

# %%
# We want to have a consistent column order for easier interpretation of the output.
# However, if there are any columns added to views.tsv at any point in the future,
# we want to make sure these are also present in the output.
# Therefore, we define the column order and also add any remaining columns to the output.
col_order = [
    "title",
    "Food Dropdown",
    "Metric Dropdown",
    "Unit Radio",
    "Per Capita Checkbox",
    "subtitle",
    "type",
    "ySlugs",
    "tableSlug",
]
remaining_cols = pd.Index(graphers.columns).difference(pd.Index(col_order)).tolist()
graphers = graphers.reindex(columns=col_order + remaining_cols)


# %%
# Mark the default view with defaultView=true. This is always the last column.
if default_view is not None:
    default_view_mask = graphers.eval(default_view)
    default_view_count = len(graphers[default_view_mask])
    if default_view_count != 1:
        print(
            f"🛑 fatal! Default view ({default_view}) should match exactly one view, but matches {default_view_count} views:"
        )
        print(graphers[default_view_mask])
        sys.exit(1)
    print(f"📌 Default view:\n{graphers[default_view_mask]}")
    graphers["defaultView"] = np.where(default_view_mask, "true", None)

# %%
graphers_tsv = graphers.to_csv(sep="\t", index=False)
graphers_tsv_indented = textwrap.indent(graphers_tsv, "\t")

table_defs = "\n".join([table_def(food) for food in foods_df.index])
food_slugs = "\t".join(foods_df.index)

# %%
warning = "# DO NOT EDIT THIS FILE BY HAND. It is automatically generated using a set of input files. Any changes made directly to it will be overwritten.\n\n"

with open(outfile, "w", newline="\n") as f:
    f.write(
        warning
        + template.substitute(
            food_slugs=food_slugs,
            graphers_tsv=graphers_tsv_indented,
            table_defs=table_defs,
        )
    )

    print(f"💾 Explorer config written to {path.abspath(outfile)}")
