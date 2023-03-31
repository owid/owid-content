# %% [markdown]
# # Key Metrics Explorer of the Luxembourg Income Study
# This code creates the tsv file for the key metrics explorer from the LIS data, available [here](https://owid.cloud/admin/explorers/preview/lis-keymetrics)

import textwrap
from pathlib import Path

import numpy as np

# %%
import pandas as pd

PARENT_DIR = Path(__file__).parent.parent.parent.parent.absolute()
outfile = PARENT_DIR / "explorers" / "lis-keymetrics.explorer.tsv"

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
equivalence_scales = pd.read_csv(url, keep_default_na=False)

# Absolute povlines
sheet_name = "povlines_abs"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
povlines_abs = pd.read_csv(url, keep_default_na=False, dtype={"dollars_text": "str"})

# Relative povlines
sheet_name = "povlines_rel"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
povlines_rel = pd.read_csv(url, keep_default_na=False)

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
    "explorerTitle": "Key Metrics Explorer of the Luxembourg Income Study",
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

sourceName = "Luxembourg Income Study (LIS) (2023)"
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
            # Headcount ratio (abs)
            for p in range(len(povlines_abs)):
                df_tables.loc[
                    j, "name"
                ] = f"Share below ${povlines_abs['dollars_text'][p]} a day ({equivalence_scales['text'][eq]})"
                df_tables.loc[
                    j, "slug"
                ] = f"headcount_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_{povlines_abs['cents'][p]}"
                df_tables.loc[
                    j, "description"
                ] = f"% of population living in households with {welfare['welfare_type'][wel]} below ${povlines_abs['dollars_text'][p]} a day.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}Household {welfare['welfare_type'][wel]} {equivalence_scales['note'][eq]}"
                df_tables.loc[j, "unit"] = "%"
                df_tables.loc[j, "shortUnit"] = "%"
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[
                    j, "colorScaleNumericBins"
                ] = "3;10;20;30;40;50;60;70;80;90;100"
                df_tables.loc[j, "colorScaleScheme"] = "OrRd"
                j += 1

            # Headcount (abs)
            for p in range(len(povlines_abs)):
                df_tables.loc[
                    j, "name"
                ] = f"Number below ${povlines_abs['dollars_text'][p]} a day ({equivalence_scales['text'][eq]})"
                df_tables.loc[
                    j, "slug"
                ] = f"headcount_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_{povlines_abs['cents'][p]}"
                df_tables.loc[
                    j, "description"
                ] = f"Number of people living in households with {welfare['welfare_type'][wel]} below ${povlines_abs['dollars_text'][p]} a day.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}Household {welfare['welfare_type'][wel]} {equivalence_scales['note'][eq]}"
                df_tables.loc[j, "unit"] = np.nan
                df_tables.loc[j, "shortUnit"] = np.nan
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[
                    j, "colorScaleNumericBins"
                ] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000"
                df_tables.loc[j, "colorScaleScheme"] = "Reds"
                j += 1

            # Headcount ratio (rel)
            for pct in range(len(povlines_rel)):
                df_tables.loc[
                    j, "name"
                ] = f"{povlines_rel['percent'][pct]} of median {welfare['welfare_type'][wel]} - share of population below poverty line ({welfare['technical_text'][wel].capitalize()}, {equivalence_scales['text'][eq]})"
                df_tables.loc[
                    j, "slug"
                ] = f"headcount_ratio_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
                df_tables.loc[
                    j, "description"
                ] = f"% of population living in households with {welfare['welfare_type'][wel]} below {povlines_rel['percent'][pct]} of the median {welfare['welfare_type'][wel]}.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}Household {welfare['welfare_type'][wel]} {equivalence_scales['note'][eq]}"
                df_tables.loc[j, "unit"] = "%"
                df_tables.loc[j, "shortUnit"] = "%"
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[j, "colorScaleNumericBins"] = "5;10;15;20;25;30"
                df_tables.loc[j, "colorScaleScheme"] = "YlOrBr"
                j += 1

            # Headcount (rel)
            for pct in range(len(povlines_rel)):
                df_tables.loc[
                    j, "name"
                ] = f"{povlines_rel['percent'][pct]} of median {welfare['welfare_type'][wel]} - total number of people below poverty line ({welfare['technical_text'][wel].capitalize()}, {equivalence_scales['text'][eq]})"
                df_tables.loc[
                    j, "slug"
                ] = f"headcount_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
                df_tables.loc[
                    j, "description"
                ] = f"Number of people living in households with {welfare['welfare_type'][wel]} below {povlines_rel['percent'][pct]} of the median {welfare['welfare_type'][wel]}.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}Household {welfare['welfare_type'][wel]} {equivalence_scales['note'][eq]}"
                df_tables.loc[j, "unit"] = np.nan
                df_tables.loc[j, "shortUnit"] = np.nan
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[
                    j, "colorScaleNumericBins"
                ] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000"
                df_tables.loc[j, "colorScaleScheme"] = "YlOrBr"
                j += 1

            # Mean
            df_tables.loc[
                j, "name"
            ] = f"Mean {welfare['welfare_type'][wel]}  ({welfare['technical_text'][wel].capitalize()}, {equivalence_scales['text'][eq]})"
            df_tables.loc[
                j, "slug"
            ] = f"mean_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_tables.loc[
                j, "description"
            ] = f"Mean {welfare['welfare_type'][wel]}.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}Household {welfare['welfare_type'][wel]} {equivalence_scales['note'][eq]}"
            df_tables.loc[j, "unit"] = "international-$ in 2017 prices"
            df_tables.loc[j, "shortUnit"] = "$"
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_mean"][wel]
            df_tables.loc[j, "colorScaleScheme"] = "BuGn"
            j += 1

            # Median
            df_tables.loc[
                j, "name"
            ] = f"Median {welfare['welfare_type'][wel]}  ({welfare['technical_text'][wel].capitalize()}, {equivalence_scales['text'][eq]})"
            df_tables.loc[
                j, "slug"
            ] = f"median_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_tables.loc[
                j, "description"
            ] = f"This is the level of {welfare['welfare_type'][wel]} below which 50% of the population falls.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}Household {welfare['welfare_type'][wel]} {equivalence_scales['note'][eq]}"
            df_tables.loc[j, "unit"] = "international-$ in 2017 prices"
            df_tables.loc[j, "shortUnit"] = "$"
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_median"][wel]
            df_tables.loc[j, "colorScaleScheme"] = "Blues"
            j += 1

            # P10
            df_tables.loc[
                j, "name"
            ] = f"Threshold {welfare['welfare_type'][wel]} marking the poorest decile ({welfare['technical_text'][wel].capitalize()}, {equivalence_scales['text'][eq]})"
            df_tables.loc[
                j, "slug"
            ] = f"thr_p10_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_tables.loc[
                j, "description"
            ] = f"The level of {welfare['welfare_type'][wel]} below which 10% of the population falls.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}Household {welfare['welfare_type'][wel]} {equivalence_scales['note'][eq]}"
            df_tables.loc[j, "unit"] = "international-$ in 2017 prices"
            df_tables.loc[j, "shortUnit"] = "$"
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[
                j, "colorScaleNumericBins"
            ] = "1000;2000;5000;10000;20000;50000;100000"
            df_tables.loc[j, "colorScaleScheme"] = "Purples"
            j += 1

            # P90
            df_tables.loc[
                j, "name"
            ] = f"Threshold {welfare['welfare_type'][wel]} marking the richest decile ({welfare['technical_text'][wel].capitalize()}, {equivalence_scales['text'][eq]})"
            df_tables.loc[
                j, "slug"
            ] = f"thr_p90_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_tables.loc[
                j, "description"
            ] = f"The level of {welfare['welfare_type'][wel]} below which 90% of the population falls.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}Household {welfare['welfare_type'][wel]} {equivalence_scales['note'][eq]}"
            df_tables.loc[j, "unit"] = "international-$ in 2017 prices"
            df_tables.loc[j, "shortUnit"] = "$"
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[
                j, "colorScaleNumericBins"
            ] = "1000;2000;5000;10000;20000;50000;100000"
            df_tables.loc[j, "colorScaleScheme"] = "Purples"
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
    for wel in range(len(welfare)):
        for eq in range(len(equivalence_scales)):
            # Headcount ratio (abs)
            for p in range(len(povlines_abs)):
                df_graphers.loc[
                    j, "title"
                ] = f"{povlines_abs['title_share'][p]} ({welfare['title'][wel].capitalize()}, {equivalence_scales['text'][eq]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"headcount_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_{povlines_abs['cents'][p]}"
                df_graphers.loc[j, "Metric Dropdown"] = "Share in poverty"
                df_graphers.loc[
                    j, "Poverty line Dropdown"
                ] = f"{povlines_abs['povline_dropdown'][p]}"
                df_graphers.loc[
                    j, "Welfare type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                    "text"
                ][eq].capitalize()
                df_graphers.loc[
                    j, "subtitle"
                ] = f"{povlines_abs['subtitle'][p]} {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2017 prices."
                df_graphers.loc[j, "type"] = np.nan
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                j += 1

            # Headcount (abs)
            for p in range(len(povlines_abs)):
                df_graphers.loc[
                    j, "title"
                ] = f"{povlines_abs['title_number'][p]} ({welfare['title'][wel].capitalize()}, {equivalence_scales['text'][eq]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"headcount_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_{povlines_abs['cents'][p]}"
                df_graphers.loc[j, "Metric Dropdown"] = "Number in poverty"
                df_graphers.loc[
                    j, "Poverty line Dropdown"
                ] = f"{povlines_abs['povline_dropdown'][p]}"
                df_graphers.loc[
                    j, "Welfare type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                    "text"
                ][eq].capitalize()
                df_graphers.loc[
                    j, "subtitle"
                ] = f"{povlines_abs['subtitle'][p]} {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2017 prices."
                df_graphers.loc[j, "type"] = np.nan
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                j += 1

            # Headcount ratio (abs) - Multiple lines
            df_graphers.loc[
                j, "title"
            ] = f"Share of population living below a range of poverty lines ({welfare['title'][wel].capitalize()}, {equivalence_scales['text'][eq]})"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"headcount_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_100 headcount_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_215 headcount_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_365 headcount_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_685 headcount_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_1000 headcount_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_2000 headcount_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_3000 headcount_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_4000"
            df_graphers.loc[j, "Metric Dropdown"] = "Share in poverty"
            df_graphers.loc[j, "Poverty line Dropdown"] = "Multiple lines"
            df_graphers.loc[
                j, "Welfare type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                "text"
            ][eq].capitalize()
            df_graphers.loc[
                j, "subtitle"
            ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. {welfare['subtitle'][wel]}"
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2017 prices."
            df_graphers.loc[j, "type"] = np.nan
            df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
            df_graphers.loc[j, "hasMapTab"] = "false"
            df_graphers.loc[j, "tab"] = "chart"
            j += 1

            # Headcount (abs) - Multiple lines
            df_graphers.loc[
                j, "title"
            ] = f"Number of people living below a range of poverty lines ({welfare['title'][wel].capitalize()}, {equivalence_scales['text'][eq]})"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"headcount_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_100 headcount_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_215 headcount_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_365 headcount_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_685 headcount_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_1000 headcount_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_2000 headcount_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_3000 headcount_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_4000"
            df_graphers.loc[j, "Metric Dropdown"] = "Number in poverty"
            df_graphers.loc[j, "Poverty line Dropdown"] = "Multiple lines"
            df_graphers.loc[
                j, "Welfare type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                "text"
            ][eq].capitalize()
            df_graphers.loc[
                j, "subtitle"
            ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. {welfare['subtitle'][wel]}"
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2017 prices."
            df_graphers.loc[j, "type"] = np.nan
            df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
            df_graphers.loc[j, "hasMapTab"] = "false"
            df_graphers.loc[j, "tab"] = "chart"
            j += 1

            # Headcount ratio (rel)
            for pct in range(len(povlines_rel)):
                df_graphers.loc[
                    j, "title"
                ] = f"{povlines_rel['title_share'][pct]} ({welfare['title'][wel].capitalize()}, {equivalence_scales['text'][eq]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"headcount_ratio_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
                df_graphers.loc[j, "Metric Dropdown"] = "Share in poverty"
                df_graphers.loc[
                    j, "Poverty line Dropdown"
                ] = f"{povlines_rel['dropdown'][pct]}"
                df_graphers.loc[
                    j, "Welfare type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                    "text"
                ][eq].capitalize()
                df_graphers.loc[
                    j, "subtitle"
                ] = f"Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel['text'][pct]} {welfare['welfare_type'][wel]}. {welfare['subtitle'][wel]}"
                df_graphers.loc[j, "note"] = np.nan
                df_graphers.loc[j, "type"] = np.nan
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                j += 1

            # Headcount (rel)
            for pct in range(len(povlines_rel)):
                df_graphers.loc[
                    j, "title"
                ] = f"{povlines_rel['title_number'][pct]} ({welfare['title'][wel].capitalize()}, {equivalence_scales['text'][eq]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"headcount_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
                df_graphers.loc[j, "Metric Dropdown"] = "Number in poverty"
                df_graphers.loc[
                    j, "Poverty line Dropdown"
                ] = f"{povlines_rel['dropdown'][pct]}"
                df_graphers.loc[
                    j, "Welfare type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                    "text"
                ][eq].capitalize()
                df_graphers.loc[
                    j, "subtitle"
                ] = f"Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel['text'][pct]} {welfare['welfare_type'][wel]}. {welfare['subtitle'][wel]}"
                df_graphers.loc[j, "note"] = np.nan
                df_graphers.loc[j, "type"] = np.nan
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                j += 1

            # Mean
            df_graphers.loc[
                j, "title"
            ] = f"Mean {welfare['welfare_type'][wel]} ({welfare['title'][wel].capitalize()}, {equivalence_scales['text'][eq]})"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"mean_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_graphers.loc[j, "Metric Dropdown"] = "Mean income or consumption"
            df_graphers.loc[
                j, "Welfare type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                "text"
            ][eq].capitalize()
            df_graphers.loc[
                j, "subtitle"
            ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. {welfare['subtitle'][wel]}"
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2017 prices."
            df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers.loc[j, "hasMapTab"] = "true"
            df_graphers.loc[j, "tab"] = "map"
            df_graphers.loc[j, "yScaleToggle"] = "true"
            j += 1

            # Median
            df_graphers.loc[
                j, "title"
            ] = f"Median {welfare['welfare_type'][wel]} ({welfare['title'][wel].capitalize()}, {equivalence_scales['text'][eq]})"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"median_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_graphers.loc[j, "Metric Dropdown"] = "Median income or consumption"
            df_graphers.loc[
                j, "Welfare type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                "text"
            ][eq].capitalize()
            df_graphers.loc[
                j, "subtitle"
            ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. {welfare['subtitle'][wel]}"
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2017 prices."
            df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers.loc[j, "hasMapTab"] = "true"
            df_graphers.loc[j, "tab"] = "map"
            df_graphers.loc[j, "yScaleToggle"] = "true"
            j += 1

            # P10
            df_graphers.loc[
                j, "title"
            ] = f"Threshold {welfare['welfare_type'][wel]} marking the poorest decile ({welfare['title'][wel].capitalize()}, {equivalence_scales['text'][eq]})"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"thr_p10_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_graphers.loc[
                j, "Metric Dropdown"
            ] = "Income or consumption of the poorest 10%"
            df_graphers.loc[
                j, "Welfare type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                "text"
            ][eq].capitalize()
            df_graphers.loc[
                j, "subtitle"
            ] = f"This is the level of {welfare['welfare_type'][wel]} below which 10% of the population falls. {welfare['subtitle'][wel]}"
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries."
            df_graphers.loc[j, "type"] = np.nan
            df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers.loc[j, "hasMapTab"] = "true"
            df_graphers.loc[j, "tab"] = "map"
            df_graphers.loc[j, "yScaleToggle"] = "true"
            j += 1

            # P90
            df_graphers.loc[
                j, "title"
            ] = f"Threshold {welfare['welfare_type'][wel]} marking the richest decile ({welfare['title'][wel].capitalize()}, {equivalence_scales['text'][eq]})"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"thr_p90_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_graphers.loc[
                j, "Metric Dropdown"
            ] = "Income or consumption of the richest 10%"
            df_graphers.loc[
                j, "Welfare type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                "text"
            ][eq].capitalize()
            df_graphers.loc[
                j, "subtitle"
            ] = f"This is the level of {welfare['welfare_type'][wel]} below which 90% of the population falls. {welfare['subtitle'][wel]}"
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries."
            df_graphers.loc[j, "type"] = np.nan
            df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers.loc[j, "hasMapTab"] = "true"
            df_graphers.loc[j, "tab"] = "map"
            df_graphers.loc[j, "yScaleToggle"] = "true"
            j += 1

        # Comparisons between equivalized and per capita measures
        # Headcount ratio (abs)
        for p in range(len(povlines_abs)):
            df_graphers.loc[
                j, "title"
            ] = f"{povlines_abs['title_share'][p]} ({welfare['title'][wel].capitalize()}, equivalized vs. per capita)"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"headcount_ratio_{welfare['slug'][wel]}_eq_{povlines_abs['cents'][p]} headcount_ratio_{welfare['slug'][wel]}_pc_{povlines_abs['cents'][p]}"
            df_graphers.loc[j, "Metric Dropdown"] = "Share in poverty"
            df_graphers.loc[
                j, "Poverty line Dropdown"
            ] = f"{povlines_abs['povline_dropdown'][p]}"
            df_graphers.loc[
                j, "Welfare type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[
                j, "Equivalence scale Dropdown"
            ] = "Equivalized vs. per capita"
            df_graphers.loc[
                j, "subtitle"
            ] = f"{povlines_abs['subtitle'][p]} {welfare['subtitle'][wel]}"
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2017 prices."
            df_graphers.loc[j, "type"] = np.nan
            df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
            df_graphers.loc[j, "hasMapTab"] = "false"
            df_graphers.loc[j, "tab"] = "chart"
            j += 1

        # Headcount (abs)
        for p in range(len(povlines_abs)):
            df_graphers.loc[
                j, "title"
            ] = f"{povlines_abs['title_number'][p]} ({welfare['title'][wel].capitalize()}, equivalized vs. per capita"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"headcount_{welfare['slug'][wel]}_eq_{povlines_abs['cents'][p]} headcount_{welfare['slug'][wel]}_pc_{povlines_abs['cents'][p]}"
            df_graphers.loc[j, "Metric Dropdown"] = "Number in poverty"
            df_graphers.loc[
                j, "Poverty line Dropdown"
            ] = f"{povlines_abs['povline_dropdown'][p]}"
            df_graphers.loc[
                j, "Welfare type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[
                j, "Equivalence scale Dropdown"
            ] = "Equivalized vs. per capita"
            df_graphers.loc[
                j, "subtitle"
            ] = f"{povlines_abs['subtitle'][p]} {welfare['subtitle'][wel]}"
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2017 prices."
            df_graphers.loc[j, "type"] = np.nan
            df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
            df_graphers.loc[j, "hasMapTab"] = "false"
            df_graphers.loc[j, "tab"] = "chart"
            j += 1

        # Headcount ratio (rel)
        for pct in range(len(povlines_rel)):
            df_graphers.loc[
                j, "title"
            ] = f"{povlines_rel['title_share'][pct]} ({welfare['title'][wel].capitalize()}, equivalized vs. per capita)"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"headcount_ratio_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_eq headcount_ratio_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_pc"
            df_graphers.loc[j, "Metric Dropdown"] = "Share in poverty"
            df_graphers.loc[
                j, "Poverty line Dropdown"
            ] = f"{povlines_rel['dropdown'][pct]}"
            df_graphers.loc[
                j, "Welfare type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[
                j, "Equivalence scale Dropdown"
            ] = "Equivalized vs. per capita"
            df_graphers.loc[
                j, "subtitle"
            ] = f"Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel['text'][pct]} {welfare['welfare_type'][wel]}. {welfare['subtitle'][wel]}"
            df_graphers.loc[j, "note"] = np.nan
            df_graphers.loc[j, "type"] = np.nan
            df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
            df_graphers.loc[j, "hasMapTab"] = "false"
            df_graphers.loc[j, "tab"] = "chart"
            j += 1

        # Headcount (rel)
        for pct in range(len(povlines_rel)):
            df_graphers.loc[
                j, "title"
            ] = f"{povlines_rel['title_number'][pct]} ({welfare['title'][wel].capitalize()}, equivalized vs. per capita)"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"headcount_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_eq headcount_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_pc"
            df_graphers.loc[j, "Metric Dropdown"] = "Number in poverty"
            df_graphers.loc[
                j, "Poverty line Dropdown"
            ] = f"{povlines_rel['dropdown'][pct]}"
            df_graphers.loc[
                j, "Welfare type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[
                j, "Equivalence scale Dropdown"
            ] = "Equivalized vs. per capita"
            df_graphers.loc[
                j, "subtitle"
            ] = f"Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel['text'][pct]} {welfare['welfare_type'][wel]}. {welfare['subtitle'][wel]}"
            df_graphers.loc[j, "note"] = np.nan
            df_graphers.loc[j, "type"] = np.nan
            df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
            df_graphers.loc[j, "hasMapTab"] = "false"
            df_graphers.loc[j, "tab"] = "chart"
            j += 1

        # Mean
        df_graphers.loc[
            j, "title"
        ] = f"Mean {welfare['welfare_type'][wel]} ({welfare['title'][wel].capitalize()}, equivalized vs. per capita)"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"mean_{welfare['slug'][wel]}_eq mean_{welfare['slug'][wel]}_pc"
        df_graphers.loc[j, "Metric Dropdown"] = "Mean income or consumption"
        df_graphers.loc[
            j, "Welfare type Dropdown"
        ] = f"{welfare['dropdown_option'][wel]}"
        df_graphers.loc[j, "Equivalence scale Dropdown"] = "Equivalized vs. per capita"
        df_graphers.loc[
            j, "subtitle"
        ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. {welfare['subtitle'][wel]}"
        df_graphers.loc[
            j, "note"
        ] = f"This data is measured in international-$ at 2017 prices."
        df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        df_graphers.loc[j, "hasMapTab"] = "false"
        df_graphers.loc[j, "tab"] = "chart"
        df_graphers.loc[j, "yScaleToggle"] = "true"
        j += 1

        # Median
        df_graphers.loc[
            j, "title"
        ] = f"Median {welfare['welfare_type'][wel]} ({welfare['title'][wel].capitalize()}, equivalized vs. per capita)"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"median_{welfare['slug'][wel]}_eq median_{welfare['slug'][wel]}_pc"
        df_graphers.loc[j, "Metric Dropdown"] = "Median income or consumption"
        df_graphers.loc[
            j, "Welfare type Dropdown"
        ] = f"{welfare['dropdown_option'][wel]}"
        df_graphers.loc[j, "Equivalence scale Dropdown"] = "Equivalized vs. per capita"
        df_graphers.loc[
            j, "subtitle"
        ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. {welfare['subtitle'][wel]}"
        df_graphers.loc[
            j, "note"
        ] = f"This data is measured in international-$ at 2017 prices."
        df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        df_graphers.loc[j, "hasMapTab"] = "false"
        df_graphers.loc[j, "tab"] = "chart"
        df_graphers.loc[j, "yScaleToggle"] = "true"
        j += 1

        # P10
        df_graphers.loc[
            j, "title"
        ] = f"Threshold {welfare['welfare_type'][wel]} marking the poorest decile ({welfare['title'][wel].capitalize()}, equivalized vs. per capita)"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"thr_p10_{welfare['slug'][wel]}_eq thr_p10_{welfare['slug'][wel]}_pc"
        df_graphers.loc[
            j, "Metric Dropdown"
        ] = "Income or consumption of the poorest 10%"
        df_graphers.loc[
            j, "Welfare type Dropdown"
        ] = f"{welfare['dropdown_option'][wel]}"
        df_graphers.loc[j, "Equivalence scale Dropdown"] = "Equivalized vs. per capita"
        df_graphers.loc[
            j, "subtitle"
        ] = f"This is the level of {welfare['welfare_type'][wel]} below which 10% of the population falls. {welfare['subtitle'][wel]}"
        df_graphers.loc[
            j, "note"
        ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries."
        df_graphers.loc[j, "type"] = np.nan
        df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        df_graphers.loc[j, "hasMapTab"] = "false"
        df_graphers.loc[j, "tab"] = "chart"
        df_graphers.loc[j, "yScaleToggle"] = "true"
        j += 1

        # P90
        df_graphers.loc[
            j, "title"
        ] = f"Threshold {welfare['welfare_type'][wel]} marking the richest decile ({welfare['title'][wel].capitalize()}, equivalized vs. per capita)"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"thr_p90_{welfare['slug'][wel]}_eq thr_p90_{welfare['slug'][wel]}_pc"
        df_graphers.loc[
            j, "Metric Dropdown"
        ] = "Income or consumption of the richest 10%"
        df_graphers.loc[
            j, "Welfare type Dropdown"
        ] = f"{welfare['dropdown_option'][wel]}"
        df_graphers.loc[j, "Equivalence scale Dropdown"] = "Equivalized vs. per capita"
        df_graphers.loc[
            j, "subtitle"
        ] = f"This is the level of {welfare['welfare_type'][wel]} below which 90% of the population falls. {welfare['subtitle'][wel]}"
        df_graphers.loc[
            j, "note"
        ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries."
        df_graphers.loc[j, "type"] = np.nan
        df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        df_graphers.loc[j, "hasMapTab"] = "false"
        df_graphers.loc[j, "tab"] = "chart"
        df_graphers.loc[j, "yScaleToggle"] = "true"
        j += 1

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
    (df_graphers["Metric Dropdown"] == "Share in poverty")
    & (
        df_graphers["Poverty line Dropdown"]
        == "$2.15 per day: International Poverty Line"
    )
    & (df_graphers["Welfare type Dropdown"] == "Income before tax")
    & (df_graphers["Equivalence scale Dropdown"] == "Equivalized"),
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
        f.write("\ncolumns\t" + tables["name"][tab] + "\n\n" + table_tsv_indented)
