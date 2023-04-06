# %% [markdown]
# # Inequality Data Explorer of World Bank data
# This code creates the tsv file for the inequality explorer from the World Bank PIP data, available [here](https://owid.cloud/admin/explorers/preview/pip-inequality-explorer)

import textwrap
from pathlib import Path

import numpy as np

# %%
import pandas as pd

PARENT_DIR = Path(__file__).parent.parent.parent.absolute()
outfile = PARENT_DIR / "explorers" / "pip-inequality-explorer.explorer.tsv"

# %% [markdown]
# ## Google sheets auxiliar data
# These spreadsheets provide with different details depending on each relative poverty line or survey type.

# %%
# Read Google sheets
sheet_id = "17KJ9YcvfdmO_7-Sv2Ij0vmzAQI6rXSIqHfJtgFHN-a8"

# Relative poverty sheet
sheet_name = "povlines_rel"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
povlines_rel = pd.read_csv(url)

# Survey type sheet
sheet_name = "survey_type"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
survey_type = pd.read_csv(url)

# %% [markdown]
# ## Header
# General settings of the explorer are defined here, like the title, subtitle, default country selection, publishing status and others.

# %%
# The header is defined as a dictionary first and then it is converted into a index-oriented dataframe
header_dict = {
    "explorerTitle": "Inequality Data Explorer of World Bank data",
    "selection": [
        "Chile",
        "Brazil",
        "South Africa",
        "United States",
        "France",
        "China",
    ],
    "explorerSubtitle": "<i><a href='https://github.com/owid/poverty-data'>Download inequality data on GitHub</a></i>",
    "isPublished": "false",
    "googleSheet": f"https://docs.google.com/spreadsheets/d/{sheet_id}",
    "wpBlockId": "52633",
    "entityType": "country or region",
}

# Index-oriented dataframe
df_header = pd.DataFrame.from_dict(header_dict, orient="index", columns=None)
# Assigns a cell for each entity separated by comma (like in `selection`)
df_header = df_header[0].apply(pd.Series)

# %% [markdown]
# ## Tables
# Variables are grouped by type to iterate by different survey types at the same time. The output is the list of all the variables being used in the explorer, with metadata.
# ### Tables for variables not showing breaks between surveys
# These variables consider a continous series, without breaks due to changes in surveys' methodology

# %%
# Table generation
df_tables = pd.DataFrame()
j = 0

for survey in range(len(survey_type)):
    # Gini coefficient
    df_tables.loc[j, "name"] = f"Gini coefficient"
    df_tables.loc[j, "slug"] = f"gini"
    df_tables.loc[j, "sourceName"] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[
        j, "description"
    ] = f"The Gini coefficient measures inequality on a scale between 0 and 1, where higher values indicate greater inequality."
    df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
    df_tables.loc[
        j, "dataPublishedBy"
    ] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, "unit"] = np.nan
    df_tables.loc[j, "shortUnit"] = np.nan
    df_tables.loc[j, "tolerance"] = 5
    df_tables.loc[j, "type"] = "Numeric"
    df_tables.loc[j, "colorScaleNumericMinValue"] = 0
    df_tables.loc[
        j, "colorScaleNumericBins"
    ] = "0.2;0.25;0.3;0.35;0.4;0.45;0.5;0.55;0.6"
    df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables.loc[j, "colorScaleScheme"] = "Reds"
    df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # Share of the top 10%
    df_tables.loc[
        j, "name"
    ] = f"Share of the richest decile in total {survey_type.text[survey]}"
    df_tables.loc[j, "slug"] = f"decile10_share"
    df_tables.loc[j, "sourceName"] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[
        j, "description"
    ] = f"The {survey_type.text[survey]} of the richest decile (tenth of the population) as a share of total {survey_type.text[survey]}."
    df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
    df_tables.loc[
        j, "dataPublishedBy"
    ] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, "unit"] = "%"
    df_tables.loc[j, "shortUnit"] = "%"
    df_tables.loc[j, "tolerance"] = 5
    df_tables.loc[j, "type"] = "Numeric"
    df_tables.loc[j, "colorScaleNumericMinValue"] = 0
    df_tables.loc[j, "colorScaleNumericBins"] = "10;15;20;25;30;35;40;45;50"
    df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables.loc[j, "colorScaleScheme"] = "Greens"
    df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # P90/P10
    df_tables.loc[j, "name"] = f"P90/P10 ratio"
    df_tables.loc[j, "slug"] = f"p90_p10_ratio"
    df_tables.loc[j, "sourceName"] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[
        j, "description"
    ] = f"P90 is the the level of {survey_type.text[survey]} below which 90% of the population lives. P10 is the level of {survey_type.text[survey]} below which 10% of the population lives. This variable gives the ratio of the two. It is a measure of inequality that indicates the gap between the richest and poorest tenth of the population. It tells you how many times richer someone just in the the poorest tenth would need to be in order to be counted in the richest tenth."
    df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
    df_tables.loc[
        j, "dataPublishedBy"
    ] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
    df_tables.loc[j, "unit"] = np.nan
    df_tables.loc[j, "shortUnit"] = np.nan
    df_tables.loc[j, "tolerance"] = 5
    df_tables.loc[j, "type"] = "Numeric"
    df_tables.loc[j, "colorScaleNumericMinValue"] = 0
    df_tables.loc[j, "colorScaleNumericBins"] = "0;2;4;6;8;10;12;14;16;18"
    df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables.loc[j, "colorScaleScheme"] = "OrRd"
    df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # P90/P50
    df_tables.loc[j, "name"] = f"P90/P50 ratio"
    df_tables.loc[j, "slug"] = f"p90_p50_ratio"
    df_tables.loc[j, "sourceName"] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[
        j, "description"
    ] = f"P90 is the the level of {survey_type.text[survey]} above which 10% of the population lives. P50 is the median – the level of {survey_type.text[survey]} below which 50% of the population lives. This variable gives the ratio of the two. It is a measure of inequality within the top half of the distribution. It tells you how many times richer someone in the middle of the distribution would need to be in order to be counted in the richest tenth."
    df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
    df_tables.loc[
        j, "dataPublishedBy"
    ] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
    df_tables.loc[j, "unit"] = np.nan
    df_tables.loc[j, "shortUnit"] = np.nan
    df_tables.loc[j, "tolerance"] = 5
    df_tables.loc[j, "type"] = "Numeric"
    df_tables.loc[j, "colorScaleNumericMinValue"] = 0
    df_tables.loc[j, "colorScaleNumericBins"] = "0;1;2;3;4;5"
    df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables.loc[j, "colorScaleScheme"] = "Purples"
    df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # P50/P10
    df_tables.loc[j, "name"] = f"P50/P10 ratio"
    df_tables.loc[j, "slug"] = f"p50_p10_ratio"
    df_tables.loc[j, "sourceName"] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[
        j, "description"
    ] = f"P50 is the median – the level of {survey_type.text[survey]} below which 50% of the population lives. P10 is the the level of {survey_type.text[survey]} below which 10% of the population lives. This variable gives the ratio of the two. It is a measure of inequality within the bottom half of the distribution. It tells you how many times richer someone just in the the poorest tenth would need to be in order to be reach the median."
    df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
    df_tables.loc[
        j, "dataPublishedBy"
    ] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
    df_tables.loc[j, "unit"] = np.nan
    df_tables.loc[j, "shortUnit"] = np.nan
    df_tables.loc[j, "tolerance"] = 5
    df_tables.loc[j, "type"] = "Numeric"
    df_tables.loc[j, "colorScaleNumericMinValue"] = 0
    df_tables.loc[j, "colorScaleNumericBins"] = "0;0.5;1;1.5;2;2.5;3;3.5;4"
    df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables.loc[j, "colorScaleScheme"] = "YlOrRd"
    df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # Palma ratio
    df_tables.loc[j, "name"] = f"Palma ratio"
    df_tables.loc[j, "slug"] = f"palma_ratio"
    df_tables.loc[j, "sourceName"] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[
        j, "description"
    ] = f"The Palma ratio is a measure of inequality: it is the share of total {survey_type.text[survey]} of the top 10% divided by the share of the bottom 40%."
    df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
    df_tables.loc[
        j, "dataPublishedBy"
    ] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
    df_tables.loc[j, "unit"] = np.nan
    df_tables.loc[j, "shortUnit"] = np.nan
    df_tables.loc[j, "tolerance"] = 5
    df_tables.loc[j, "type"] = "Numeric"
    df_tables.loc[j, "colorScaleNumericMinValue"] = 0
    df_tables.loc[j, "colorScaleNumericBins"] = "0;0.5;1;1.5;2;2.5;3;3.5;4;4.5;5"
    df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables.loc[j, "colorScaleScheme"] = "Oranges"
    df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # Headcount ratio (rel)
    for pct in range(len(povlines_rel)):
        df_tables.loc[
            j, "name"
        ] = f"{povlines_rel.percent[pct]} of median - share of population below poverty line"
        df_tables.loc[j, "slug"] = f"headcount_ratio_{povlines_rel.slug_suffix[pct]}"
        df_tables.loc[j, "sourceName"] = "World Bank Poverty and Inequality Platform"
        df_tables.loc[
            j, "description"
        ] = f"% of population living in households with an {survey_type.text[survey]} per person below {povlines_rel.percent[pct]} of the median."
        df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
        df_tables.loc[
            j, "dataPublishedBy"
        ] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
        df_tables.loc[j, "unit"] = "%"
        df_tables.loc[j, "shortUnit"] = "%"
        df_tables.loc[j, "tolerance"] = 5
        df_tables.loc[j, "type"] = "Numeric"
        df_tables.loc[j, "colorScaleNumericMinValue"] = 0
        df_tables.loc[j, "colorScaleNumericBins"] = "5;10;15;20;25;30;30.0001"
        df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables.loc[j, "colorScaleScheme"] = "YlOrBr"
        df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
        j += 1

    # MLD
    df_tables.loc[j, "name"] = f"Mean Log Deviation"
    df_tables.loc[j, "slug"] = f"mld"
    df_tables.loc[j, "sourceName"] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[
        j, "description"
    ] = f"The mean log deviation (MLD) is a measure of inequality. An MLD of zero indicates perfect equality and it takes on larger positive values as incomes become more unequal. The measure is also referred to as 'Theil L' or 'GE(0)', in reference to the wider families of inequality measures to which the MLD belongs."
    df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
    df_tables.loc[
        j, "dataPublishedBy"
    ] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, "unit"] = np.nan
    df_tables.loc[j, "shortUnit"] = np.nan
    df_tables.loc[j, "tolerance"] = 5
    df_tables.loc[j, "type"] = "Numeric"
    df_tables.loc[j, "colorScaleNumericMinValue"] = 0
    df_tables.loc[
        j, "colorScaleNumericBins"
    ] = "0;0.1;0.2;0.3;0.4;0.5;0.6;0.7;0.8;0.9;1"
    df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables.loc[j, "colorScaleScheme"] = "RdPu"
    df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # Polarization
    df_tables.loc[j, "name"] = f"Polarization index"
    df_tables.loc[j, "slug"] = f"polarization"
    df_tables.loc[j, "sourceName"] = "World Bank Poverty and Inequality Platform"
    df_tables.loc[
        j, "description"
    ] = f"The polarization index, also known as the Wolfson polarization index, measures the extent to which the distribution of {survey_type.text[survey]} is “spread out” and bi-modal. Like the Gini coefficient, the polarization index ranges from 0 (no polarization) to 1 (complete polarization). The polarization index is based on Wolfson (1994) and Ravallion and Chen (1997). See Wolfson, Michael C. 1994. “When Inequalities Diverge.” The American Economic Review 84 (2): 353–58. https://www.jstor.org/stable/2117858 and Ravallion, Martin, and Shaohua Chen. 1997. “What Can New Survey Data Tell Us about Recent Changes in Distribution and Poverty?” The World Bank Economic Review 11 (2): 357–82. https://www.jstor.org/stable/3990232."
    df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
    df_tables.loc[
        j, "dataPublishedBy"
    ] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, "unit"] = np.nan
    df_tables.loc[j, "shortUnit"] = np.nan
    df_tables.loc[j, "tolerance"] = 5
    df_tables.loc[j, "type"] = "Numeric"
    df_tables.loc[j, "colorScaleNumericMinValue"] = 0
    df_tables.loc[j, "colorScaleNumericBins"] = "0;0.1;0.2;0.3;0.4;0.5;0.6;0.7"
    df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables.loc[j, "colorScaleScheme"] = "Reds"
    df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

# Make tolerance integer (to not break the parameter in the platform)
df_tables["tolerance"] = df_tables["tolerance"].astype("Int64")

# %% [markdown]
# ### Tables for variables showing breaks between surveys
# These variables consider a breaks in the series due to changes in surveys' methodology.

# %%
# Create master table for line breaks
df_spells = pd.DataFrame()
j = 0

for i in range(len(df_tables)):
    for c_spell in range(1, 7):
        df_spells.loc[j, "master_var"] = df_tables.slug[i]
        df_spells.loc[j, "name"] = "Consumption surveys"
        df_spells.loc[j, "slug"] = f"consumption_spell_{c_spell}"
        df_spells.loc[j, "sourceName"] = df_tables.sourceName[i]
        df_spells.loc[j, "description"] = df_tables.description[i]
        df_spells.loc[j, "sourceLink"] = df_tables.sourceLink[i]
        df_spells.loc[j, "dataPublishedBy"] = df_tables.dataPublishedBy[i]
        df_spells.loc[j, "unit"] = df_tables.unit[i]
        df_spells.loc[j, "shortUnit"] = df_tables.shortUnit[i]
        df_spells.loc[j, "tolerance"] = df_tables.tolerance[i]
        df_spells.loc[j, "type"] = df_tables.type[i]
        df_spells.loc[
            j, "colorScaleNumericMinValue"
        ] = df_tables.colorScaleNumericMinValue[i]
        df_spells.loc[j, "colorScaleNumericBins"] = df_tables.colorScaleNumericBins[i]
        df_spells.loc[j, "colorScaleEqualSizeBins"] = df_tables.colorScaleEqualSizeBins[
            i
        ]
        df_spells.loc[j, "colorScaleScheme"] = df_tables.colorScaleScheme[i]
        df_spells.loc[j, "survey_type"] = df_tables.survey_type[i]
        j += 1

    for i_spell in range(1, 8):
        df_spells.loc[j, "master_var"] = df_tables.slug[i]
        df_spells.loc[j, "name"] = "Income surveys"
        df_spells.loc[j, "slug"] = f"income_spell_{i_spell}"
        df_spells.loc[j, "sourceName"] = df_tables.sourceName[i]
        df_spells.loc[j, "description"] = df_tables.description[i]
        df_spells.loc[j, "sourceLink"] = df_tables.sourceLink[i]
        df_spells.loc[j, "dataPublishedBy"] = df_tables.dataPublishedBy[i]
        df_spells.loc[j, "unit"] = df_tables.unit[i]
        df_spells.loc[j, "shortUnit"] = df_tables.shortUnit[i]
        df_spells.loc[j, "tolerance"] = df_tables.tolerance[i]
        df_spells.loc[j, "type"] = df_tables.type[i]
        df_spells.loc[
            j, "colorScaleNumericMinValue"
        ] = df_tables.colorScaleNumericMinValue[i]
        df_spells.loc[j, "colorScaleNumericBins"] = df_tables.colorScaleNumericBins[i]
        df_spells.loc[j, "colorScaleEqualSizeBins"] = df_tables.colorScaleEqualSizeBins[
            i
        ]
        df_spells.loc[j, "colorScaleScheme"] = df_tables.colorScaleScheme[i]
        df_spells.loc[j, "survey_type"] = df_tables.survey_type[i]
        j += 1

# Make tolerance integer (to not break the parameter in the platform)
df_spells["tolerance"] = df_spells["tolerance"].astype("Int64")

# %% [markdown]
# ### Grapher views
# Similar to the tables, this creates the grapher views by grouping by types of variables and then running by survey type.

# %%
# Grapher table generation

df_graphers = pd.DataFrame()

j = 0

for survey in range(len(survey_type)):
    # Gini coefficient
    df_graphers.loc[j, "title"] = f"Income inequality: Gini coefficient"
    df_graphers.loc[j, "ySlugs"] = f"gini"
    df_graphers.loc[j, "Metric Dropdown"] = "Gini coefficient"
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = f"The Gini coefficient is a measure of the inequality of the income distribution in a population. Higher values indicate a higher level of inequality."
    df_graphers.loc[
        j, "note"
    ] = f"Depending on the country and year, the data relates to disposable {survey_type.text[survey]} per capita."
    df_graphers.loc[j, "sourceDesc"] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers.loc[j, "hasMapTab"] = "true"
    df_graphers.loc[j, "tab"] = "map"
    df_graphers.loc[j, "mapTargetTime"] = 2019
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # Share of the top 10%
    df_graphers.loc[
        j, "title"
    ] = f"{survey_type.text[survey].capitalize()} share of the top 10%"
    df_graphers.loc[j, "ySlugs"] = f"decile10_share"
    df_graphers.loc[j, "Metric Dropdown"] = "Top 10% share"
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = f"This is the {survey_type.text[survey]} of the richest decile (tenth of the population) as a share of total {survey_type.text[survey]}."
    df_graphers.loc[
        j, "note"
    ] = f"Depending on the country and year, the data relates to disposable {survey_type.text[survey]} per capita."
    df_graphers.loc[j, "sourceDesc"] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers.loc[j, "hasMapTab"] = "true"
    df_graphers.loc[j, "tab"] = "map"
    df_graphers.loc[j, "mapTargetTime"] = 2019
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # P90/P10
    df_graphers.loc[j, "title"] = f"Income inequality: P90/P10 ratio"
    df_graphers.loc[j, "ySlugs"] = f"p90_p10_ratio"
    df_graphers.loc[j, "Metric Dropdown"] = "P90/P10"
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = f"P90 and P10 are the levels of {survey_type.text[survey]} below which 90% and 10% of the population live, respectively. This variable gives the ratio of the two. It is a measure of inequality that indicates the gap between the richest and poorest tenth of the population."
    df_graphers.loc[
        j, "note"
    ] = f"Depending on the country and year, the data relates to disposable {survey_type.text[survey]} per capita."
    df_graphers.loc[j, "sourceDesc"] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers.loc[j, "hasMapTab"] = "true"
    df_graphers.loc[j, "tab"] = "map"
    df_graphers.loc[j, "mapTargetTime"] = 2019
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # P90/P50
    df_graphers.loc[j, "title"] = f"Income inequality: P90/P50 ratio"
    df_graphers.loc[j, "ySlugs"] = f"p90_p50_ratio"
    df_graphers.loc[j, "Metric Dropdown"] = "P90/P50"
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = f"The P90/P50 ratio measures the degree of inequality within the richest half of the population. A ratio of 2 means that someone just falling in the richest tenth of the population has twice the median {survey_type.text[survey]}."
    df_graphers.loc[
        j, "note"
    ] = f"Depending on the country and year, the data relates to disposable {survey_type.text[survey]} per capita."
    df_graphers.loc[j, "sourceDesc"] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers.loc[j, "hasMapTab"] = "true"
    df_graphers.loc[j, "tab"] = "map"
    df_graphers.loc[j, "mapTargetTime"] = 2019
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # P50/P10
    df_graphers.loc[j, "title"] = f"Income inequality: P50/P10 ratio"
    df_graphers.loc[j, "ySlugs"] = f"p50_p10_ratio"
    df_graphers.loc[j, "Metric Dropdown"] = "P50/P10"
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = f"The P50/P10 ratio measures the degree of inequality within the poorest half of the population. A ratio of 2 means that the median {survey_type.text[survey]} is two times higher than that of someone just falling in the poorest tenth of the population."
    df_graphers.loc[
        j, "note"
    ] = f"Depending on the country and year, the data relates to disposable {survey_type.text[survey]} per capita."
    df_graphers.loc[j, "sourceDesc"] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers.loc[j, "hasMapTab"] = "true"
    df_graphers.loc[j, "tab"] = "map"
    df_graphers.loc[j, "mapTargetTime"] = 2019
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # Palma ratio
    df_graphers.loc[j, "title"] = f"Income inequality: Palma ratio"
    df_graphers.loc[j, "ySlugs"] = f"palma_ratio"
    df_graphers.loc[j, "Metric Dropdown"] = "Palma ratio"
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = f"The Palma ratio is the share of total {survey_type.text[survey]} of the top 10% divided by the share of the bottom 40%."
    df_graphers.loc[
        j, "note"
    ] = f"Depending on the country and year, the data relates to disposable {survey_type.text[survey]} per capita."
    df_graphers.loc[j, "sourceDesc"] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers.loc[j, "hasMapTab"] = "true"
    df_graphers.loc[j, "tab"] = "map"
    df_graphers.loc[j, "mapTargetTime"] = 2019
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # Headcount ratio (rel)
    for pct in range(len(povlines_rel)):
        df_graphers.loc[j, "title"] = f"{povlines_rel.title_share[pct]}"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"headcount_ratio_{povlines_rel.slug_suffix[pct]}"
        df_graphers.loc[
            j, "Metric Dropdown"
        ] = f"Share in relative poverty (< {povlines_rel.text[pct]})"
        df_graphers.loc[
            j, "Household survey data type Dropdown"
        ] = f"{survey_type.dropdown_option[survey]}"
        df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
        df_graphers.loc[
            j, "subtitle"
        ] = f"Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel.text[pct]} {survey_type.text[survey]}."
        df_graphers.loc[
            j, "note"
        ] = f"Depending on the country and year, the data relates to disposable {survey_type.text[survey]} per capita."
        df_graphers.loc[j, "sourceDesc"] = "World Bank Poverty and Inequality Platform"
        df_graphers.loc[j, "type"] = np.nan
        df_graphers.loc[j, "yAxisMin"] = 0
        df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers.loc[j, "hasMapTab"] = "true"
        df_graphers.loc[j, "tab"] = "map"
        df_graphers.loc[j, "mapTargetTime"] = 2019
        df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
        j += 1

    # MLD
    df_graphers.loc[j, "title"] = f"Income inequality: Mean log deviation"
    df_graphers.loc[j, "ySlugs"] = f"mld"
    df_graphers.loc[j, "Metric Dropdown"] = "Mean log deviation"
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = f"The mean log deviation (MLD) is a measure of inequality. An MLD of zero indicates perfect equality and it takes on larger positive values as incomes become more unequal."
    df_graphers.loc[
        j, "note"
    ] = f"Depending on the country and year, the data relates to disposable {survey_type.text[survey]} per capita."
    df_graphers.loc[j, "sourceDesc"] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers.loc[j, "hasMapTab"] = "true"
    df_graphers.loc[j, "tab"] = "map"
    df_graphers.loc[j, "mapTargetTime"] = 2019
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # Polarization
    df_graphers.loc[j, "title"] = f"Income inequality: Polarization index"
    df_graphers.loc[j, "ySlugs"] = f"polarization"
    df_graphers.loc[j, "Metric Dropdown"] = "Polarization index"
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = f"The polarization index, also known as the Wolfson polarization index, measures the extent to which the distribution of {survey_type.text[survey]} is “spread out” and bi-modal. Like the Gini coefficient, the polarization index ranges from 0 (no polarization) to 1 (complete polarization)."
    df_graphers.loc[
        j, "note"
    ] = f"Depending on the country and year, the data relates to disposable {survey_type.text[survey]} per capita."
    df_graphers.loc[j, "sourceDesc"] = "World Bank Poverty and Inequality Platform"
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers.loc[j, "hasMapTab"] = "true"
    df_graphers.loc[j, "tab"] = "map"
    df_graphers.loc[j, "mapTargetTime"] = 2019
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

df_graphers["Show breaks between less comparable surveys Checkbox"] = "false"
# %% [markdown]
# ### Grapher views to show breaks in the curves

# %%
df_graphers_spells = pd.DataFrame()
j = 0

for i in range(len(df_graphers)):
    df_graphers_spells.loc[j, "title"] = df_graphers["title"][i]
    df_graphers_spells.loc[
        j, "ySlugs"
    ] = "consumption_spell_1 consumption_spell_2 consumption_spell_3 consumption_spell_4 consumption_spell_5 consumption_spell_6 income_spell_1 income_spell_2 income_spell_3 income_spell_4 income_spell_5 income_spell_6 income_spell_7"
    df_graphers_spells.loc[j, "Metric Dropdown"] = df_graphers["Metric Dropdown"][i]
    df_graphers_spells.loc[j, "Household survey data type Dropdown"] = df_graphers[
        "Household survey data type Dropdown"
    ][i]
    df_graphers_spells.loc[j, "tableSlug"] = (
        df_graphers["survey_type"][i] + "_" + df_graphers["ySlugs"][i]
    )
    df_graphers_spells.loc[j, "subtitle"] = " ".join(
        [
            df_graphers["subtitle"][i],
            "The chart shows breaks in the comparability of the underlying household survey data over time within each country individually.",
        ]
    )
    df_graphers_spells.loc[j, "note"] = df_graphers["note"][i]
    df_graphers_spells.loc[j, "sourceDesc"] = df_graphers["sourceDesc"][i]
    df_graphers_spells.loc[j, "type"] = df_graphers["type"][i]
    df_graphers_spells.loc[j, "yAxisMin"] = df_graphers["yAxisMin"][i]
    df_graphers_spells.loc[j, "selectedFacetStrategy"] = "entity"
    df_graphers_spells.loc[j, "hasMapTab"] = "false"
    df_graphers_spells.loc[j, "tab"] = np.nan
    df_graphers_spells.loc[j, "mapTargetTime"] = np.nan
    df_graphers_spells.loc[
        j, "Show breaks between less comparable surveys Checkbox"
    ] = "true"
    j += 1

df_graphers = pd.concat([df_graphers, df_graphers_spells], ignore_index=True)

# %% [markdown]
# Final adjustments to the graphers table: add `relatedQuestion` link and `defaultView`:

# %%
# Add related question link
df_graphers["relatedQuestionText"] = np.nan
df_graphers["relatedQuestionUrl"] = np.nan

# Make mapTargetTime integer (to not break the parameter in the platform)
df_graphers["mapTargetTime"] = df_graphers["mapTargetTime"].astype("Int64")

# When the "Depending on" footnote is introduced, it generates unwanted texts as:
# "Depending on the country and year, the data relates to disposable income per capita."
# "Depending on the country and year, the data relates to disposable consumption per capita."

# When int-$ are not included
df_graphers["note"] = df_graphers["note"].str.replace(
    "Depending on the country and year, the data relates to disposable income per capita.",
    "The data relates to disposable income per capita.",
    regex=False,
)
df_graphers["note"] = df_graphers["note"].str.replace(
    "Depending on the country and year, the data relates to disposable consumption per capita.",
    "The data relates to disposable consumption per capita.",
    regex=False,
)

# When int-$ are included
df_graphers["note"] = df_graphers["note"].str.replace(
    "Depending on the country and year, it relates to disposable income per capita.",
    "It relates to disposable income per capita.",
    regex=False,
)
df_graphers["note"] = df_graphers["note"].str.replace(
    "Depending on the country and year, it relates to disposable consumption per capita.",
    "It relates to disposable consumption per capita.",
    regex=False,
)

# Select one default view
df_graphers.loc[
    (df_graphers["ySlugs"] == "gini")
    & (df_graphers["Show breaks between less comparable surveys Checkbox"] == "false")
    & (df_graphers["tableSlug"] == "inc_or_cons"),
    ["defaultView"],
] = "true"


# %% [markdown]
# ## Explorer generation
# Here, the header, tables and graphers dataframes are combined to be shown in for format required for OWID data explorers.

# %%
# Define list of variables to iterate: survey types and the list of variables (the latter for spell tables)
survey_list = list(survey_type["table_name"].unique())
var_list = list(df_spells["master_var"].unique())

# Header is converted into a tab-separated text
header_tsv = df_header.to_csv(sep="\t", header=False)

# Auxiliar variable `survey_type` is dropped and graphers table is converted into a tab-separated text
graphers_tsv = df_graphers.drop(columns=["survey_type"])
graphers_tsv = graphers_tsv.to_csv(sep="\t", index=False)

# This table is indented, to follow explorers' format
graphers_tsv_indented = textwrap.indent(graphers_tsv, "\t")

# The dataframes are combined, including tables which are filtered by survey type and variable
with open(outfile, "w", newline="\n", encoding="utf-8") as f:
    f.write(header_tsv)
    f.write("\ngraphers\n" + graphers_tsv_indented)

    for i in survey_list:
        table_tsv = (
            df_tables[df_tables["survey_type"] == i].copy().reset_index(drop=True)
        )
        table_tsv = table_tsv.drop(columns=["survey_type"])
        table_tsv = table_tsv.to_csv(sep="\t", index=False)
        table_tsv_indented = textwrap.indent(table_tsv, "\t")
        f.write(
            "\ntable\t"
            + "https://raw.githubusercontent.com/owid/notebooks/main/BetterDataDocs/JoeHasell/PIP/data/ppp_2017/final/OWID_internal_upload/explorer_database/"
            + i
            + "/poverty_"
            + i
            + ".csv\t"
            + i
        )
        f.write("\ncolumns\t" + i + "\n\n" + table_tsv_indented)

    for var in var_list:
        for i in survey_list:
            table_tsv = (
                df_spells[
                    (df_spells["master_var"] == var) & (df_spells["survey_type"] == i)
                ]
                .copy()
                .reset_index(drop=True)
            )
            table_tsv = table_tsv.drop(columns=["master_var", "survey_type"])
            table_tsv = table_tsv.to_csv(sep="\t", index=False)
            table_tsv_indented = textwrap.indent(table_tsv, "\t")
            f.write(
                "\ntable\t"
                + "https://raw.githubusercontent.com/owid/notebooks/main/BetterDataDocs/JoeHasell/PIP/data/ppp_2017/final/OWID_internal_upload/explorer_database/comparability_data/"
                + i
                + "/"
                + var
                + ".csv\t"
                + i
                + "_"
                + var
            )
            f.write("\ncolumns\t" + i + "_" + var + "\n\n" + table_tsv_indented)