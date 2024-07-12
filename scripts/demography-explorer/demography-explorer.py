# %%
from os import path
from string import Template
import textwrap
import pandas as pd
import re

# There are two datasets available:
# - DATASET_PATH_PREFIX: Classic dataset, with estimates for 1950-2023 and projections for 2024-2100.
# - DATASET_PATH_PREFIX_FULL: Alternative daraset, with projections for 1950-2100 (the 1950-2023 part is the same in all projections). This dataset is helpful in explorers to be able to plot the complete time series (estimates + projections) for a given projection.
DATASET_PATH_PREFIX = "grapher/un/2024-07-12/un_wpp/"
DATASET_PATH_PREFIX_FULL = "grapher/un/2024-07-12/un_wpp_full/"

COLS_TO_DROP = []


# %%
def substitute_rows(row):
    # Rows can include placeholders like ${sex__slug}, which will be replaced here
    for key in row.keys():
        if isinstance(row[key], str):
            while "${" in row[key]:
                template = Template(row[key])
                row[key] = template.substitute(
                    **row, DATASET_PATH_PREFIX=DATASET_PATH_PREFIX
                )
    return row


def table_def(rows, display_names):
    rows["yVariableIds"] = rows["yVariableIds"].map(lambda x: x.split(" "))
    rows = (
        rows.explode("yVariableIds")
        .drop_duplicates("yVariableIds")
        .reset_index(drop=True)
    )

    column_defs = rows.filter(regex="^column__", axis=1).rename(
        columns=lambda x: re.sub("^column__", "", x)
    )
    col_names = [
        "catalogPath",
        "name",
        *column_defs.columns,
    ]
    col_names = "\t".join(col_names)

    col_defs = [
        [
            row["yVariableIds"],
            display_names.get(row["yVariableIds"]) or "",
            *column_defs.loc[idx].values.tolist(),
        ]
        for (idx, row) in rows.iterrows()
    ]
    col_defs = ["\t".join(col) for col in col_defs]
    col_defs = textwrap.indent("\n".join(col_defs), "\t")

    return f"""columns
	{col_names}
{col_defs}"""


# %%
outfile = "../../explorers/population-and-demography.explorer.tsv"

# %%
# Read inputs
with open("demography-explorer.template.tsv", "r") as templateFile:
    template = Template(templateFile.read())
input_files = ["metrics", "sex", "age_group", "projection"]
input_df = {
    file: pd.read_csv(f"{file}.csv", dtype=str, keep_default_na=False)
    for file in input_files
}
df = input_df["metrics"]

# %%
merge_cols = input_files[1:]
for merge_col in merge_cols:
    explode_col = "_" + merge_col
    df[explode_col] = df[explode_col].apply(lambda x: x.split(" "))
    df = df.explode(explode_col)
    merge_df = input_df[merge_col]
    merge_df.columns = merge_col + "__" + merge_df.columns.values
    df = df.merge(
        merge_df,
        how="left",
        left_on=explode_col,
        right_on=merge_col + "__slug",
        validate="many_to_one",
        indicator=merge_col + "__merge",
    )
    assert df[merge_col + "__merge"].isin(["both"]).all()
    df = df.drop([explode_col, merge_col + "__merge"], axis=1)

# We want to specify some variants twice, once with more specific information (e.g. manual map brackets).
# Use the first occurrence of every view.
df = df.drop_duplicates(
    subset=["Metric Dropdown", *[f"{col}__slug" for col in merge_cols]]
)

# %%

df = df.apply(substitute_rows, axis=1)
for col in ["title", "subtitle"]:
    df[col] = (
        df[col]
        .apply(lambda x: x.strip())
        .apply(lambda x: x[0].upper() + x[1:] if len(x) else x)
        .apply(lambda x: re.sub(" {2,}", " ", x))
        .apply(lambda x: x.replace("\\-\\", " "))
        # .apply(lambda x: x or " ")
    )
    # explicitly set empty strings to a single space, so we don't inherit it from ETL
    # df.loc[df[col] == "-", col] = " "


# %%
# Use DATASET_PATH_PREFIX_FULL when variant is not "None" (i.e. some projection scenario)
mask = df["projection__slug"] != "estimates"
df.loc[mask, "yVariableIds"] = df.loc[mask, "yVariableIds"].str.replace(
    DATASET_PATH_PREFIX, DATASET_PATH_PREFIX_FULL
)

# %%
# Extract column display names from yVariableIds
# The `yVariableIds` column can contain names for column slugs, e.g.:
# population_broad__all__15-24__records:"15-24 years"
# Note the colon, and especially the quotes around the name. They are required!
# This config will use the name "15-24 years" as the display name for the column.
# If an explicit name is not given, the row's title will be used instead.
col_display_names = {}

y_slug_re = r"([\w\-\/_#]+):\"([^\"]+)\""
for idx, row in df.iterrows():
    matches = re.finditer(y_slug_re, row["yVariableIds"])
    slugs = []
    for match in matches:
        col_slug, col_name = match.groups()
        slugs.append(col_slug)
        if col_slug not in col_display_names:
            col_display_names[col_slug] = col_name

    if len(slugs):
        df.loc[idx, "yVariableIds"] = " ".join(slugs)

# %%
col_defs = table_def(
    df.reset_index(drop=True),
    col_display_names,
)

# %%

col_rename = {
    "sex__name": "Sex Radio",
    "age_group__name": "Age group Dropdown",
    "projection__name": "Projection Scenario Radio",
}
df = df.rename(columns=col_rename)

# Reorder columns such that the different Dropdown/Radio columns are next to each other
metric_dropdown_idx = df.columns.get_loc("Metric Dropdown")
cols = df.columns.tolist()
for i, col in enumerate(col_rename.values()):
    cols.remove(col)
    cols.insert(metric_dropdown_idx + 1 + i, col)
df = df.loc[:, cols]

# Drop all remaining programmatic columns containing __
df = df.drop(columns=df.filter(regex="__"))

# %%
df = df.rename(columns={col_name: "_" + col_name for col_name in COLS_TO_DROP})

# %%
graphers_tsv = df.to_csv(sep="\t", index=False)
graphers_tsv_indented = textwrap.indent(graphers_tsv, "\t")

# %%
warning = "# DO NOT EDIT THIS FILE BY HAND. It is automatically generated using a set of input files. Any changes made directly to it will be overwritten.\n\n"

with open(outfile, "w", newline="\n") as f:
    f.write(
        warning
        + template.substitute(
            graphers_tsv=graphers_tsv_indented,
            table_defs=col_defs,
        )
    )

    print(f"💾 Explorer config written to {path.abspath(outfile)}")

# %%
