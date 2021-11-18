# This script takes three input files and combines them into a big explorer spreadsheet for the global food explorer.
# The files are:
# - (1) global-food-explorer.template.tsv: A template file that contains the header and footer of the spreadsheet, together with some placeholders.
# - (2) foods.tsv: a list of foods and their singular and plural names.
# - (3) views-per-food.tsv: a list of all available views for every food, including subtitle etc. The title can contain placeholders which are then filled out with the food name.
# This is all further complicated by the fact that we have different categories of foods (currently: crops and animal products), which use different columns, units and subtitles.
# We take the cartesian product between (2) and (3) - according to the category -, sprinkle some magic dust to make the titles work, and then place that massive table into the template (1).

# %%
from string import Template
import pandas as pd
import textwrap

# %%


def food_url(food):
    return f"https://owid-catalog.nyc3.digitaloceanspaces.com/garden/explorers/2021/food_explorer/{food}.csv"


def substitute_title(row):
    # The title can include placeholders like ${food_singular_title}, which will be replaced with the actual food name here.
    food_slug = row['tableSlug']
    food_names = foods_df.loc[food_slug]
    for key in ['title', 'subtitle']:
        if isinstance(row[key], str):
            template = Template(row[key])
            row[key] = template.substitute(
                food_singular_title=food_names['singular'],
                food_singular_lower=food_names['singular'].lower(),
                food_plural_title=food_names['plural'],
                food_plural_lower=food_names['plural'].lower(),
            )
    return row


def table_def(food):
    return f"table\t{food_url(food)}\t{food}"
    # return f"table\t{food_url('apples' if random.randint(0, 1) == 0 else 'bananas')}\t{food}"


# %%
with open('global-food-explorer.template.tsv', 'r') as templateFile:
    template = Template(templateFile.read())
foods_df = pd.read_csv('foods.tsv', sep='\t', index_col='slug')
views_df = pd.read_csv('views-per-food.tsv', sep='\t', dtype=str)

# %%
# convert comma-separated list of categories to an actual list, such that we can explode and merge by category
views_df['_categories'] = views_df['_categories'].apply(lambda x: x.split(','))
views_df = views_df.explode('_categories').rename(
    columns={'_categories': '_category'})
foods = pd.DataFrame([{'Food Dropdown': row['dropdown'], 'tableSlug': slug, '_category': row['category']}
                     for slug, row in foods_df.iterrows()])

# %%
# merge on column: _category
graphers = foods.merge(views_df).apply(
    substitute_title, axis=1)
graphers = graphers.drop(columns='_category').sort_values(
    by='Food Dropdown', kind='stable')

# %%
# We want to have a consistent column order for easier interpretation of the output.
# However, if there are any columns added to the views tsv at any point in the future,
# we want to make sure these are also present in the output.
# Therefore, we define the column order and also add any remaining columns to the output.
col_order = ['title', 'Food Dropdown', 'Metric Dropdown', 'Unit Radio',
             'Per Capita Checkbox', 'subtitle', 'type', 'ySlugs', 'tableSlug', 'hasMapTab']
remaining_cols = pd.Index(graphers.columns).difference(
    pd.Index(col_order)).tolist()
graphers = graphers.reindex(columns=col_order + remaining_cols)

# %%
graphers_tsv = graphers.to_csv(sep='\t', index=False)
graphers_tsv_indented = textwrap.indent(graphers_tsv, '\t')

table_defs = '\n'.join([table_def(food) for food in foods_df.index])
food_slugs = '\t'.join(foods_df.index)

# %%
with open('../../explorers/global-food-prototype.explorer.tsv', 'w', newline='\n') as f:
    f.write(template.substitute(
        food_slugs=food_slugs,
        graphers_tsv=graphers_tsv_indented,
        table_defs=table_defs
    ))
