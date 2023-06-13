# %% [markdown]
# # Inequality Data Explorer of the Luxembourg Income Study
# This code creates the tsv file for the inequality explorer from the LIS data, available [here](https://owid.cloud/admin/explorers/preview/lis-inequality)

import textwrap
from pathlib import Path

import numpy as np

# %%
import pandas as pd

PARENT_DIR = Path(__file__).parent.parent.parent.parent.absolute()
outfile = PARENT_DIR / "explorers" / "lis-inequality.explorer.tsv"

# %% [markdown]
# ## Google sheets auxiliar data
# These spreadsheets provide with different details depending on each type of welfare measure or tables considered.

# %%
# Read Google sheets
sheet_id = "1UFdwB1iBpP2tEP6GtxCHvW1GGhjsFflh42FWR80rYIg"

# Welfare type sheet
sheet_name = "welfare"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
welfare = pd.read_csv(url, keep_default_na=False)

# Equivalence scales
sheet_name = "equivalence_scales"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
equivalence_scales = pd.read_csv(url, keep_default_na=False, dtype={"checkbox": "str"})

# Relative poverty sheet
sheet_name = "povlines_rel"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
povlines_rel = pd.read_csv(url)

# Tables sheet
sheet_name = "tables"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
tables = pd.read_csv(url, keep_default_na=False)

# %% [markdown]
# ## Header
# General settings of the explorer are defined here, like the title, subtitle, default country selection, publishing status and others.

# %%
# The header is defined as a dictionary first and then it is converted into a index-oriented dataframe
header_dict = {
    "explorerTitle": "Inequality Data Explorer of the Luxembourg Income Study",
    "selection": [
        "Chile",
        "Brazil",
        "South Africa",
        "United States",
        "France",
        "China",
    ],
    "explorerSubtitle": "",
    "isPublished": "true",
    "googleSheet": f"https://docs.google.com/spreadsheets/d/{sheet_id}",
    "wpBlockId": "",
    "entityType": "country or region",
    "pickerColumnSlugs": "gini_mi_eq share_p100_mi_eq palma_ratio_mi_eq headcount_ratio_50_median_mi_eq gini_dhi_eq share_p100_dhi_eq palma_ratio_dhi_eq headcount_ratio_50_median_dhi_eq",
}

# Index-oriented dataframe
df_header = pd.DataFrame.from_dict(header_dict, orient="index", columns=None)
# Assigns a cell for each entity separated by comma (like in `selection`)
df_header = df_header[0].apply(pd.Series)

# %% [markdown]
# ## Tables
# Variables are grouped by type of welfare to iterate by different survey types at the same time. The output is the list of all the variables being used in the explorer, with metadata.
# ### Tables for variables not showing breaks between surveys
# These variables consider a continous series, without breaks due to changes in surveys' methodology

# %%
# Table generation

sourceName = "Luxembourg Income Study (2023)"
dataPublishedBy = "Luxembourg Income Study (LIS) Database, http://www.lisdatacenter.org (multiple countries; 1967-2020). Luxembourg, LIS."
sourceLink = "https://www.lisdatacenter.org/our-data/lis-database/"
colorScaleNumericMinValue = 0
tolerance = 5
colorScaleEqualSizeBins = "true"
new_line = "<br><br>"

df_tables = pd.DataFrame()
j = 0

for tab in range(len(tables)):
    # Define country as entityName
    df_tables.loc[j, "name"] = "Country"
    df_tables.loc[j, "slug"] = "country"
    df_tables.loc[j, "type"] = "EntityName"
    j += 1

    # Define year as Year
    df_tables.loc[j, "name"] = "Year"
    df_tables.loc[j, "slug"] = "year"
    df_tables.loc[j, "type"] = "Year"
    j += 1

    for wel in range(len(welfare)):
        for eq in range(len(equivalence_scales)):
            # Gini coefficient
            df_tables.loc[j, "name"] = f"Gini coefficient ({welfare['title'][wel]})"
            df_tables.loc[
                j, "slug"
            ] = f"gini_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_tables.loc[
                j, "description"
            ] = f"The Gini coefficient is a measure of the inequality of the {welfare['welfare_type'][wel]} distribution in a population. Higher values indicate a higher level of inequality.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}{equivalence_scales['description'][eq]}"
            df_tables.loc[j, "unit"] = np.nan
            df_tables.loc[j, "shortUnit"] = np.nan
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_gini"][wel]
            df_tables.loc[j, "colorScaleScheme"] = "Oranges"
            j += 1

            # Share of the top 10%
            df_tables.loc[
                j, "name"
            ] = f"{welfare['welfare_type'][wel].capitalize()} share of the richest 10% ({welfare['title'][wel]})"
            df_tables.loc[
                j, "slug"
            ] = f"share_p100_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_tables.loc[
                j, "description"
            ] = f"This is the {welfare['welfare_type'][wel]} of the richest 10% as a share of total {welfare['welfare_type'][wel]}.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}{equivalence_scales['description'][eq]}"
            df_tables.loc[j, "unit"] = "%"
            df_tables.loc[j, "shortUnit"] = "%"
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_top10"][wel]
            df_tables.loc[j, "colorScaleScheme"] = "OrRd"
            j += 1

            # Share of the bottom 50%
            df_tables.loc[
                j, "name"
            ] = f"{welfare['welfare_type'][wel].capitalize()} share of the poorest 50% ({welfare['title'][wel]})"
            df_tables.loc[
                j, "slug"
            ] = f"share_bottom50_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_tables.loc[
                j, "description"
            ] = f"This is the {welfare['welfare_type'][wel]} of the poorest 50% as a share of total {welfare['welfare_type'][wel]}.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}{equivalence_scales['description'][eq]}"
            df_tables.loc[j, "unit"] = "%"
            df_tables.loc[j, "shortUnit"] = "%"
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_bottom50"][wel]
            df_tables.loc[j, "colorScaleScheme"] = "Blues"
            j += 1

            # # P90/P10
            # df_tables.loc[j, "name"] = f"P90/P10 ratio ({welfare['title'][wel]})"
            # df_tables.loc[
            #     j, "slug"
            # ] = f"p90_p10_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            # df_tables.loc[
            #     j, "description"
            # ] = f"P90 is the the level of {welfare['welfare_type'][wel]} below which 90% of the population lives. P10 is the level of {welfare['welfare_type'][wel]} below which 10% of the population lives. This variable gives the ratio of the two. It is a measure of inequality that indicates the gap between the richest and poorest tenth of the population. It tells you how many times richer someone just in the the poorest tenth would need to be in order to be counted in the richest tenth.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}{equivalence_scales['description'][eq]}"
            # df_tables.loc[j, "unit"] = np.nan
            # df_tables.loc[j, "shortUnit"] = np.nan
            # df_tables.loc[j, "type"] = "Numeric"
            # df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_p90_p10_ratio"][
            #     wel
            # ]
            # df_tables.loc[j, "colorScaleScheme"] = "OrRd"
            # j += 1

            # # P90/P50
            # df_tables.loc[j, "name"] = f"P90/P50 ratio ({welfare['title'][wel]})"
            # df_tables.loc[
            #     j, "slug"
            # ] = f"p90_p50_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            # df_tables.loc[
            #     j, "description"
            # ] = f"P90 is the the level of {welfare['welfare_type'][wel]} above which 10% of the population lives. P50 is the median – the level of {welfare['welfare_type'][wel]} below which 50% of the population lives. This variable gives the ratio of the two. It is a measure of inequality within the top half of the distribution. It tells you how many times richer someone in the middle of the distribution would need to be in order to be counted in the richest tenth.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}{equivalence_scales['description'][eq]}"
            # df_tables.loc[j, "unit"] = np.nan
            # df_tables.loc[j, "shortUnit"] = np.nan
            # df_tables.loc[j, "type"] = "Numeric"
            # df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_p90_p50_ratio"][
            #     wel
            # ]
            # df_tables.loc[j, "colorScaleScheme"] = "Purples"
            # j += 1

            # # P50/P10
            # df_tables.loc[j, "name"] = f"P50/P10 ratio ({welfare['title'][wel]})"
            # df_tables.loc[
            #     j, "slug"
            # ] = f"p50_p10_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            # df_tables.loc[
            #     j, "description"
            # ] = f"P50 is the median – the level of {welfare['welfare_type'][wel]} below which 50% of the population lives. P10 is the the level of {welfare['welfare_type'][wel]} below which 10% of the population lives. This variable gives the ratio of the two. It is a measure of inequality within the bottom half of the distribution. It tells you how many times richer someone just in the the poorest tenth would need to be in order to be reach the median.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}{equivalence_scales['description'][eq]}"
            # df_tables.loc[j, "unit"] = np.nan
            # df_tables.loc[j, "shortUnit"] = np.nan
            # df_tables.loc[j, "type"] = "Numeric"
            # df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_p50_p10_ratio"][
            #     wel
            # ]
            # df_tables.loc[j, "colorScaleScheme"] = "YlOrRd"
            # j += 1

            # Palma ratio
            df_tables.loc[j, "name"] = f"Palma ratio ({welfare['title'][wel]})"
            df_tables.loc[
                j, "slug"
            ] = f"palma_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_tables.loc[
                j, "description"
            ] = f"The Palma ratio is a measure of inequality: it is the share of total {welfare['welfare_type'][wel]} of the top 10% divided by the share of the bottom 40%.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}{equivalence_scales['description'][eq]}"
            df_tables.loc[j, "unit"] = np.nan
            df_tables.loc[j, "shortUnit"] = np.nan
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_palma_ratio"][
                wel
            ]
            df_tables.loc[j, "colorScaleScheme"] = "YlOrBr"
            j += 1

            # Headcount ratio (rel)
            df_tables.loc[
                j, "name"
            ] = f"Share in relative poverty ({welfare['title'][wel]})"
            df_tables.loc[
                j, "slug"
            ] = f"headcount_ratio_50_median_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_tables.loc[
                j, "description"
            ] = f"% of population living in households with {welfare['welfare_type'][wel]} below 50% of the median {welfare['welfare_type'][wel]}.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}{equivalence_scales['description'][eq]}"
            df_tables.loc[j, "unit"] = "%"
            df_tables.loc[j, "shortUnit"] = "%"
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[j, "colorScaleNumericBins"] = welfare[
                "scale_relative_poverty"
            ][wel]
            df_tables.loc[j, "colorScaleScheme"] = "YlOrBr"
            j += 1

    df_tables["tableSlug"] = tables["name"][tab]

df_tables["sourceName"] = sourceName
df_tables["dataPublishedBy"] = dataPublishedBy
df_tables["sourceLink"] = sourceLink
df_tables["colorScaleNumericMinValue"] = colorScaleNumericMinValue
df_tables["tolerance"] = tolerance
df_tables["colorScaleEqualSizeBins"] = colorScaleEqualSizeBins

# Make tolerance integer (to not break the parameter in the platform)
df_tables["tolerance"] = df_tables["tolerance"].astype("Int64")

# %% [markdown]
# ### Grapher views
# Similar to the tables, this creates the grapher views by grouping by types of variables and then running by welfare type.

# %%
# Grapher table generation

yAxisMin = 0
mapTargetTime = 2019

df_graphers = pd.DataFrame()

j = 0

for tab in range(len(tables)):
    for eq in range(len(equivalence_scales)):
        for wel in range(len(welfare)):
            # Gini coefficient
            df_graphers.loc[j, "title"] = f"Gini coefficient ({welfare['title'][wel]})"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"gini_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_graphers.loc[j, "Indicator Dropdown"] = "Gini coefficient"
            df_graphers.loc[
                j, "Income measure Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[
                j,
                "Adjust for cost sharing within households (equivalized income) Checkbox",
            ] = equivalence_scales["checkbox"][eq]
            df_graphers.loc[
                j, "subtitle"
            ] = f"The Gini coefficient is a measure of the inequality of the {welfare['welfare_type'][wel]} distribution in a population. Higher values indicate a higher level of inequality. {welfare['subtitle'][wel]}"
            df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
            df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers.loc[j, "hasMapTab"] = "true"
            df_graphers.loc[j, "tab"] = "map"
            j += 1

            # Share of the top 10%
            df_graphers.loc[
                j, "title"
            ] = f"{welfare['welfare_type'][wel].capitalize()} share of the richest 10% ({welfare['title'][wel]})"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"share_p100_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_graphers.loc[j, "Indicator Dropdown"] = "Share of the richest 10%"
            df_graphers.loc[
                j, "Income measure Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[
                j,
                "Adjust for cost sharing within households (equivalized income) Checkbox",
            ] = equivalence_scales["checkbox"][eq]
            df_graphers.loc[
                j, "subtitle"
            ] = f"The share of {welfare['welfare_type'][wel]} received by the richest 10% of the population. {welfare['subtitle'][wel]}"
            df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
            df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers.loc[j, "hasMapTab"] = "true"
            df_graphers.loc[j, "tab"] = "map"
            j += 1

            # Share of the bottom 50%
            df_graphers.loc[
                j, "title"
            ] = f"{welfare['welfare_type'][wel].capitalize()} share of the poorest 50% ({welfare['title'][wel]})"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"share_bottom50_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_graphers.loc[j, "Indicator Dropdown"] = "Share of the poorest 50%"
            df_graphers.loc[
                j, "Income measure Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[
                j,
                "Adjust for cost sharing within households (equivalized income) Checkbox",
            ] = equivalence_scales["checkbox"][eq]
            df_graphers.loc[
                j, "subtitle"
            ] = f"The share of {welfare['welfare_type'][wel]} received by the poorest 50% of the population. {welfare['subtitle'][wel]}"
            df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
            df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers.loc[j, "hasMapTab"] = "true"
            df_graphers.loc[j, "tab"] = "map"
            j += 1

            # # P90/P10
            # df_graphers.loc[
            #     j, "title"
            # ] = f"{welfare['welfare_type'][wel].capitalize()} inequality: P90/P10 ratio ({welfare['title'][wel]})"
            # df_graphers.loc[
            #     j, "ySlugs"
            # ] = f"p90_p10_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            # df_graphers.loc[j, "Indicator Dropdown"] = "P90/P10"
            # df_graphers.loc[
            #     j, "Income measure Dropdown"
            # ] = f"{welfare['dropdown_option'][wel]}"
            # df_graphers.loc[
            #     j, "Adjust for cost sharing within households (equivalized income) Checkbox"
            # ] = equivalence_scales["checkbox"][eq]
            # df_graphers.loc[
            #     j, "subtitle"
            # ] = f"P90 and P10 are the levels of {welfare['welfare_type'][wel]} below which 90% and 10% of the population live, respectively. This variable gives the ratio of the two. It is a measure of inequality that indicates the gap between the richest and poorest tenth of the population. {welfare['subtitle'][wel]}"
            # df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
            # df_graphers.loc[j, "type"] = np.nan
            # df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
            # df_graphers.loc[j, "hasMapTab"] = "true"
            # df_graphers.loc[j, "tab"] = "map"
            # j += 1

            # # P90/P50
            # df_graphers.loc[
            #     j, "title"
            # ] = f"{welfare['welfare_type'][wel].capitalize()} inequality: P90/P50 ratio ({welfare['title'][wel]})"
            # df_graphers.loc[
            #     j, "ySlugs"
            # ] = f"p90_p50_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            # df_graphers.loc[j, "Indicator Dropdown"] = "P90/P50"
            # df_graphers.loc[
            #     j, "Income measure Dropdown"
            # ] = f"{welfare['dropdown_option'][wel]}"
            # df_graphers.loc[
            #     j, "Adjust for cost sharing within households (equivalized income) Checkbox"
            # ] = equivalence_scales["checkbox"][eq]
            # df_graphers.loc[
            #     j, "subtitle"
            # ] = f"The P90/P50 ratio measures the degree of inequality within the richest half of the population. A ratio of 2 means that someone just falling in the richest tenth of the population has twice the median {welfare['welfare_type'][wel]}. {welfare['subtitle'][wel]}"
            # df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
            # df_graphers.loc[j, "type"] = np.nan
            # df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
            # df_graphers.loc[j, "hasMapTab"] = "true"
            # df_graphers.loc[j, "tab"] = "map"
            # j += 1

            # # P50/P10
            # df_graphers.loc[
            #     j, "title"
            # ] = f"{welfare['welfare_type'][wel].capitalize()} inequality: P50/P10 ratio ({welfare['title'][wel]})"
            # df_graphers.loc[
            #     j, "ySlugs"
            # ] = f"p50_p10_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            # df_graphers.loc[j, "Indicator Dropdown"] = "P50/P10"
            # df_graphers.loc[
            #     j, "Income measure Dropdown"
            # ] = f"{welfare['dropdown_option'][wel]}"
            # df_graphers.loc[
            #     j, "Adjust for cost sharing within households (equivalized income) Checkbox"
            # ] = equivalence_scales["checkbox"][eq]
            # df_graphers.loc[
            #     j, "subtitle"
            # ] = f"The P50/P10 ratio measures the degree of inequality within the poorest half of the population. A ratio of 2 means that the median {welfare['welfare_type'][wel]} is two times higher than that of someone just falling in the poorest tenth of the population. {welfare['subtitle'][wel]}"
            # df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
            # df_graphers.loc[j, "type"] = np.nan
            # df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
            # df_graphers.loc[j, "hasMapTab"] = "true"
            # df_graphers.loc[j, "tab"] = "map"
            # j += 1

            # # Palma ratio
            df_graphers.loc[j, "title"] = f"Palma ratio ({welfare['title'][wel]})"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"palma_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_graphers.loc[j, "Indicator Dropdown"] = "Palma ratio"
            df_graphers.loc[
                j, "Income measure Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[
                j,
                "Adjust for cost sharing within households (equivalized income) Checkbox",
            ] = equivalence_scales["checkbox"][eq]
            df_graphers.loc[
                j, "subtitle"
            ] = f"The share of {welfare['welfare_type'][wel]} of the richest 10% divided by the share of the poorest 40%. {welfare['subtitle'][wel]}"
            df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
            df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers.loc[j, "hasMapTab"] = "true"
            df_graphers.loc[j, "tab"] = "map"
            j += 1

            # Headcount ratio (rel)
            df_graphers.loc[
                j, "title"
            ] = f"Share in relative poverty ({welfare['title'][wel]})"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"headcount_ratio_50_median_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_graphers.loc[j, "Indicator Dropdown"] = f"Share in relative poverty"
            df_graphers.loc[
                j, "Income measure Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[
                j,
                "Adjust for cost sharing within households (equivalized income) Checkbox",
            ] = equivalence_scales["checkbox"][eq]
            df_graphers.loc[
                j, "subtitle"
            ] = f"The share of the population with {welfare['welfare_type'][wel]} below 50% of the median. Relative poverty is a measure of the extent of inequality within the bottom of the distribution. {welfare['subtitle'][wel]}"
            df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
            df_graphers.loc[j, "type"] = np.nan
            df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers.loc[j, "hasMapTab"] = "true"
            df_graphers.loc[j, "tab"] = "map"
            j += 1

        # COMPARE BEFORE AND AFTER TAX
        # Gini coefficient
        df_graphers.loc[j, "title"] = f"Gini coefficient (after tax vs. before tax)"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"gini_mi_{equivalence_scales['slug'][eq]} gini_dhi_{equivalence_scales['slug'][eq]}"
        df_graphers.loc[j, "Indicator Dropdown"] = "Gini coefficient"
        df_graphers.loc[j, "Income measure Dropdown"] = "After tax vs. before tax"
        df_graphers.loc[
            j, "Adjust for cost sharing within households (equivalized income) Checkbox"
        ] = equivalence_scales["checkbox"][eq]
        df_graphers.loc[
            j, "subtitle"
        ] = f"The Gini coefficient is a measure of the inequality of the income distribution in a population. Higher values indicate a higher level of inequality."
        df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
        df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        df_graphers.loc[j, "hasMapTab"] = "false"
        df_graphers.loc[j, "tab"] = "chart"
        j += 1

        # Share of the top 10%
        df_graphers.loc[
            j, "title"
        ] = f"Income share of the richest 10% (after tax vs. before tax)"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"share_p100_mi_{equivalence_scales['slug'][eq]} share_p100_dhi_{equivalence_scales['slug'][eq]}"
        df_graphers.loc[j, "Indicator Dropdown"] = "Share of the richest 10%"
        df_graphers.loc[j, "Income measure Dropdown"] = "After tax vs. before tax"
        df_graphers.loc[
            j, "Adjust for cost sharing within households (equivalized income) Checkbox"
        ] = equivalence_scales["checkbox"][eq]
        df_graphers.loc[
            j, "subtitle"
        ] = f"The share of income received by the richest 10% of the population."
        df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
        df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        df_graphers.loc[j, "hasMapTab"] = "false"
        df_graphers.loc[j, "tab"] = "chart"
        j += 1

        # Share of the bottom 50%
        df_graphers.loc[
            j, "title"
        ] = f"Income share of the poorest 50% (after tax vs. before tax)"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"share_bottom50_mi_{equivalence_scales['slug'][eq]} share_bottom50_dhi_{equivalence_scales['slug'][eq]}"
        df_graphers.loc[j, "Indicator Dropdown"] = "Share of the poorest 50%"
        df_graphers.loc[j, "Income measure Dropdown"] = "After tax vs. before tax"
        df_graphers.loc[
            j, "Adjust for cost sharing within households (equivalized income) Checkbox"
        ] = equivalence_scales["checkbox"][eq]
        df_graphers.loc[
            j, "subtitle"
        ] = f"The share of income received by the poorest 50% of the population."
        df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
        df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        df_graphers.loc[j, "hasMapTab"] = "false"
        df_graphers.loc[j, "tab"] = "chart"
        j += 1

        # # P90/P10
        # df_graphers.loc[
        #     j, "title"
        # ] = f"Income inequality: P90/P10 ratio (after tax vs. before tax)"
        # df_graphers.loc[
        #     j, "ySlugs"
        # ] = f"p90_p10_ratio_mi_{equivalence_scales['slug'][eq]} p90_p10_ratio_dhi_{equivalence_scales['slug'][eq]}"
        # df_graphers.loc[j, "Indicator Dropdown"] = "P90/P10"
        # df_graphers.loc[j, "Income measure Dropdown"] = "After tax vs. before tax"
        # df_graphers.loc[
        #     j, "Adjust for cost sharing within households (equivalized income) Checkbox"
        # ] = equivalence_scales["checkbox"][eq]
        # df_graphers.loc[
        #     j, "subtitle"
        # ] = f"P90 and P10 are the levels of income below which 90% and 10% of the population live, respectively. This variable gives the ratio of the two. It is a measure of inequality that indicates the gap between the richest and poorest tenth of the population."
        # df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
        # df_graphers.loc[j, "type"] = np.nan
        # df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        # df_graphers.loc[j, "hasMapTab"] = "false"
        # df_graphers.loc[j, "tab"] = "chart"
        # j += 1

        # # P90/P50
        # df_graphers.loc[
        #     j, "title"
        # ] = f"Income inequality: P90/P50 ratio (after tax vs. before tax)"
        # df_graphers.loc[
        #     j, "ySlugs"
        # ] = f"p90_p50_ratio_mi_{equivalence_scales['slug'][eq]} p90_p50_ratio_dhi_{equivalence_scales['slug'][eq]}"
        # df_graphers.loc[j, "Indicator Dropdown"] = "P90/P50"
        # df_graphers.loc[j, "Income measure Dropdown"] = "After tax vs. before tax"
        # df_graphers.loc[
        #     j, "Adjust for cost sharing within households (equivalized income) Checkbox"
        # ] = equivalence_scales["checkbox"][eq]
        # df_graphers.loc[
        #     j, "subtitle"
        # ] = f"The P90/P50 ratio measures the degree of inequality within the richest half of the population. A ratio of 2 means that someone just falling in the richest tenth of the population has twice the median income."
        # df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
        # df_graphers.loc[j, "type"] = np.nan
        # df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        # df_graphers.loc[j, "hasMapTab"] = "false"
        # df_graphers.loc[j, "tab"] = "chart"
        # j += 1

        # # P50/P10
        # df_graphers.loc[
        #     j, "title"
        # ] = f"Income inequality: P50/P10 ratio (after tax vs. before tax)"
        # df_graphers.loc[
        #     j, "ySlugs"
        # ] = f"p50_p10_ratio_mi_{equivalence_scales['slug'][eq]} p50_p10_ratio_dhi_{equivalence_scales['slug'][eq]}"
        # df_graphers.loc[j, "Indicator Dropdown"] = "P50/P10"
        # df_graphers.loc[j, "Income measure Dropdown"] = "After tax vs. before tax"
        # df_graphers.loc[
        #     j, "Adjust for cost sharing within households (equivalized income) Checkbox"
        # ] = equivalence_scales["checkbox"][eq]
        # df_graphers.loc[
        #     j, "subtitle"
        # ] = f"The P50/P10 ratio measures the degree of inequality within the poorest half of the population. A ratio of 2 means that the median income is two times higher than that of someone just falling in the poorest tenth of the population."
        # df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
        # df_graphers.loc[j, "type"] = np.nan
        # df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        # df_graphers.loc[j, "hasMapTab"] = "false"
        # df_graphers.loc[j, "tab"] = "chart"
        # j += 1

        # # Palma ratio
        df_graphers.loc[j, "title"] = f"Palma ratio (after tax vs. before tax)"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"palma_ratio_mi_{equivalence_scales['slug'][eq]} palma_ratio_dhi_{equivalence_scales['slug'][eq]}"
        df_graphers.loc[j, "Indicator Dropdown"] = "Palma ratio"
        df_graphers.loc[j, "Income measure Dropdown"] = "After tax vs. before tax"
        df_graphers.loc[
            j, "Adjust for cost sharing within households (equivalized income) Checkbox"
        ] = equivalence_scales["checkbox"][eq]
        df_graphers.loc[
            j, "subtitle"
        ] = f"The share of income of the richest 10% divided by the share of the poorest 40%."
        df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
        df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        df_graphers.loc[j, "hasMapTab"] = "false"
        df_graphers.loc[j, "tab"] = "chart"
        j += 1

        # Headcount ratio (rel)
        df_graphers.loc[
            j, "title"
        ] = f"Share in relative poverty (after tax vs. before tax)"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"headcount_ratio_50_median_mi_{equivalence_scales['slug'][eq]} headcount_ratio_50_median_dhi_{equivalence_scales['slug'][eq]}"
        df_graphers.loc[j, "Indicator Dropdown"] = f"Share in relative poverty"
        df_graphers.loc[j, "Income measure Dropdown"] = "After tax vs. before tax"
        df_graphers.loc[
            j,
            "Adjust for cost sharing within households (equivalized income) Checkbox",
        ] = equivalence_scales["checkbox"][eq]
        df_graphers.loc[
            j, "subtitle"
        ] = f"The share of the population with {welfare['welfare_type'][wel]} below 50% of the median. Relative poverty is a measure of the extent of inequality within the bottom of the distribution."
        df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
        df_graphers.loc[j, "type"] = np.nan
        df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        df_graphers.loc[j, "hasMapTab"] = "false"
        df_graphers.loc[j, "tab"] = "chart"
        j += 1

        # # Compare equivalized and per capita values
        # # Gini coefficient
        # df_graphers.loc[
        #     j, "title"
        # ] = f"{welfare['welfare_type'][wel].capitalize()} inequality: Gini coefficient ({welfare['title'][wel]}, equivalized vs. per capita)"
        # df_graphers.loc[
        #     j, "ySlugs"
        # ] = f"gini_{welfare['slug'][wel]}_eq gini_{welfare['slug'][wel]}_pc"
        # df_graphers.loc[j, "Indicator Dropdown"] = "Gini coefficient"
        # df_graphers.loc[
        #     j, "Income measure Dropdown"
        # ] = f"{welfare['dropdown_option'][wel]}"
        # df_graphers.loc[j, "Equivalence scale Dropdown"] = "Equivalized vs. per capita"
        # df_graphers.loc[
        #     j, "subtitle"
        # ] = f"The Gini coefficient is a measure of the inequality of the {welfare['welfare_type'][wel]} distribution in a population. Higher values indicate a higher level of inequality. {welfare['subtitle'][wel]}"
        # df_graphers.loc[j, "note"] = np.nan
        # df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        # df_graphers.loc[j, "hasMapTab"] = "false"
        # df_graphers.loc[j, "tab"] = "chart"
        # j += 1

        # # Share of the top 10%
        # df_graphers.loc[
        #     j, "title"
        # ] = f"{welfare['welfare_type'][wel].capitalize()} share of the top 10% ({welfare['title'][wel]}, equivalized vs. per capita)"
        # df_graphers.loc[
        #     j, "ySlugs"
        # ] = f"share_p100_{welfare['slug'][wel]}_eq share_p100_{welfare['slug'][wel]}_pc"
        # df_graphers.loc[j, "Indicator Dropdown"] = "Share of the richest 10%"
        # df_graphers.loc[
        #     j, "Income measure Dropdown"
        # ] = f"{welfare['dropdown_option'][wel]}"
        # df_graphers.loc[j, "Equivalence scale Dropdown"] = "Equivalized vs. per capita"
        # df_graphers.loc[
        #     j, "subtitle"
        # ] = f"This is the {welfare['welfare_type'][wel]} of the richest 10% as a share of total {welfare['welfare_type'][wel]}. {welfare['subtitle'][wel]}"
        # df_graphers.loc[j, "note"] = np.nan
        # df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        # df_graphers.loc[j, "hasMapTab"] = "false"
        # df_graphers.loc[j, "tab"] = "chart"
        # j += 1

        # # P90/P10
        # df_graphers.loc[
        #     j, "title"
        # ] = f"{welfare['welfare_type'][wel].capitalize()} inequality: P90/P10 ratio ({welfare['title'][wel]}, equivalized vs. per capita)"
        # df_graphers.loc[
        #     j, "ySlugs"
        # ] = f"p90_p10_ratio_{welfare['slug'][wel]}_eq p90_p10_ratio_{welfare['slug'][wel]}_pc"
        # df_graphers.loc[j, "Indicator Dropdown"] = "P90/P10"
        # df_graphers.loc[
        #     j, "Income measure Dropdown"
        # ] = f"{welfare['dropdown_option'][wel]}"
        # df_graphers.loc[j, "Equivalence scale Dropdown"] = "Equivalized vs. per capita"
        # df_graphers.loc[
        #     j, "subtitle"
        # ] = f"P90 and P10 are the levels of {welfare['welfare_type'][wel]} below which 90% and 10% of the population live, respectively. This variable gives the ratio of the two. It is a measure of inequality that indicates the gap between the richest and poorest tenth of the population. {welfare['subtitle'][wel]}"
        # df_graphers.loc[j, "note"] = np.nan
        # df_graphers.loc[j, "type"] = np.nan
        # df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        # df_graphers.loc[j, "hasMapTab"] = "false"
        # df_graphers.loc[j, "tab"] = "chart"
        # j += 1

        # # P90/P50
        # df_graphers.loc[
        #     j, "title"
        # ] = f"{welfare['welfare_type'][wel].capitalize()} inequality: P90/P50 ratio ({welfare['title'][wel]}, equivalized vs. per capita)"
        # df_graphers.loc[
        #     j, "ySlugs"
        # ] = f"p90_p50_ratio_{welfare['slug'][wel]}_eq p90_p50_ratio_{welfare['slug'][wel]}_pc"
        # df_graphers.loc[j, "Indicator Dropdown"] = "P90/P50"
        # df_graphers.loc[
        #     j, "Income measure Dropdown"
        # ] = f"{welfare['dropdown_option'][wel]}"
        # df_graphers.loc[j, "Equivalence scale Dropdown"] = "Equivalized vs. per capita"
        # df_graphers.loc[
        #     j, "subtitle"
        # ] = f"The P90/P50 ratio measures the degree of inequality within the richest half of the population. A ratio of 2 means that someone just falling in the richest tenth of the population has twice the median {welfare['welfare_type'][wel]}. {welfare['subtitle'][wel]}"
        # df_graphers.loc[j, "note"] = np.nan
        # df_graphers.loc[j, "type"] = np.nan
        # df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        # df_graphers.loc[j, "hasMapTab"] = "false"
        # df_graphers.loc[j, "tab"] = "chart"
        # j += 1

        # # P50/P10
        # df_graphers.loc[
        #     j, "title"
        # ] = f"{welfare['welfare_type'][wel].capitalize()} inequality: P50/P10 ratio ({welfare['title'][wel]}, equivalized vs. per capita)"
        # df_graphers.loc[
        #     j, "ySlugs"
        # ] = f"p50_p10_ratio_{welfare['slug'][wel]}_eq p50_p10_ratio_{welfare['slug'][wel]}_pc"
        # df_graphers.loc[j, "Indicator Dropdown"] = "P50/P10"
        # df_graphers.loc[
        #     j, "Income measure Dropdown"
        # ] = f"{welfare['dropdown_option'][wel]}"
        # df_graphers.loc[j, "Equivalence scale Dropdown"] = "Equivalized vs. per capita"
        # df_graphers.loc[
        #     j, "subtitle"
        # ] = f"The P50/P10 ratio measures the degree of inequality within the poorest half of the population. A ratio of 2 means that the median {welfare['welfare_type'][wel]} is two times higher than that of someone just falling in the poorest tenth of the population. {welfare['subtitle'][wel]}"
        # df_graphers.loc[j, "note"] = np.nan
        # df_graphers.loc[j, "type"] = np.nan
        # df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        # df_graphers.loc[j, "hasMapTab"] = "false"
        # df_graphers.loc[j, "tab"] = "chart"
        # j += 1

        # # # Palma ratio
        # df_graphers.loc[
        #     j, "title"
        # ] = f"{welfare['welfare_type'][wel].capitalize()} inequality: Palma ratio ({welfare['title'][wel]}, equivalized vs. per capita)"
        # df_graphers.loc[
        #     j, "ySlugs"
        # ] = f"palma_ratio_{welfare['slug'][wel]}_eq palma_ratio_{welfare['slug'][wel]}_pc"
        # df_graphers.loc[j, "Indicator Dropdown"] = "Palma ratio"
        # df_graphers.loc[
        #     j, "Income measure Dropdown"
        # ] = f"{welfare['dropdown_option'][wel]}"
        # df_graphers.loc[j, "Equivalence scale Dropdown"] = "Equivalized vs. per capita"
        # df_graphers.loc[
        #     j, "subtitle"
        # ] = f"The Palma ratio is the share of total {welfare['welfare_type'][wel]} of the top 10% divided by the share of the bottom 40%. {welfare['subtitle'][wel]}"
        # df_graphers.loc[j, "note"] = np.nan
        # df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        # df_graphers.loc[j, "hasMapTab"] = "false"
        # df_graphers.loc[j, "tab"] = "chart"
        # j += 1

        # # Headcount ratio (rel)
        # for pct in range(len(povlines_rel)):
        #     df_graphers.loc[
        #         j, "title"
        #     ] = f"{povlines_rel['title_share'][pct]} ({welfare['title'][wel]}, equivalized vs. per capita)"
        #     df_graphers.loc[
        #         j, "ySlugs"
        #     ] = f"headcount_ratio_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_eq headcount_ratio_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_pc"
        #     df_graphers.loc[
        #         j, "Indicator Dropdown"
        #     ] = f"Share in relative poverty (< {povlines_rel['text'][pct]})"
        #     df_graphers.loc[
        #         j, "Income measure Dropdown"
        #     ] = f"{welfare['dropdown_option'][wel]}"
        #     df_graphers.loc[
        #         j, "Equivalence scale Dropdown"
        #     ] = "Equivalized vs. per capita"
        #     df_graphers.loc[
        #         j, "subtitle"
        #     ] = f"Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel['text'][pct]} {welfare['welfare_type'][wel]}. {welfare['subtitle'][wel]}"
        #     df_graphers.loc[j, "note"] = np.nan
        #     df_graphers.loc[j, "type"] = np.nan
        #     df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        #     df_graphers.loc[j, "hasMapTab"] = "false"
        #     df_graphers.loc[j, "tab"] = "chart"
        #     j += 1

    df_graphers["tableSlug"] = tables["name"][tab]

# %% [markdown]
# Final adjustments to the graphers table: add `relatedQuestion` link and `defaultView`:

# %%
# Add related question link
df_graphers["relatedQuestionText"] = np.nan
df_graphers["relatedQuestionUrl"] = np.nan

# Add yAxisMin and mapTargetTime
df_graphers["yAxisMin"] = yAxisMin
df_graphers["mapTargetTime"] = mapTargetTime

# Make mapTargetTime integer (to not break the parameter in the platform)
df_graphers["mapTargetTime"] = df_graphers["mapTargetTime"].astype("Int64")

# Select one default view
df_graphers.loc[
    (df_graphers["Indicator Dropdown"] == "Gini coefficient")
    & (df_graphers["Income measure Dropdown"] == "After tax")
    & (
        df_graphers[
            "Adjust for cost sharing within households (equivalized income) Checkbox"
        ]
        == "false"
    ),
    ["defaultView"],
] = "true"


# %% [markdown]
# ## Explorer generation
# Here, the header, tables and graphers dataframes are combined to be shown in for format required for OWID data explorers.

# %%
# Define list of variables to iterate: table names
table_list = list(tables["name"].unique())

# Header is converted into a tab-separated text
header_tsv = df_header.to_csv(sep="\t", header=False)

# Graphers table is converted into a tab-separated text
graphers_tsv = df_graphers
graphers_tsv = graphers_tsv.to_csv(sep="\t", index=False)

# This table is indented, to follow explorers' format
graphers_tsv_indented = textwrap.indent(graphers_tsv, "\t")

# The dataframes are combined, including tables and links to the datasets
with open(outfile, "w", newline="\n", encoding="utf-8") as f:
    f.write(header_tsv)
    f.write("\ngraphers\n" + graphers_tsv_indented)

    for tab in range(len(tables)):
        table_tsv = (
            df_tables[df_tables["tableSlug"] == tables["name"][tab]]
            .copy()
            .reset_index(drop=True)
        )
        table_tsv = table_tsv.drop(columns=["tableSlug"])
        table_tsv = table_tsv.to_csv(sep="\t", index=False)
        table_tsv_indented = textwrap.indent(table_tsv, "\t")
        f.write("\ntable\t" + tables["link"][tab] + "\t" + tables["name"][tab])
        f.write("\ncolumns\t" + tables["name"][tab] + "\n" + table_tsv_indented)
