# %% [markdown]
# # Expanded poverty explorer of the Luxembourg Income Study
# This code creates the tsv file for the expanded poverty explorer from the LIS data, available [here](https://owid.cloud/admin/explorers/preview/lis-expanded-poverty)


import textwrap
from pathlib import Path

import numpy as np

# %%
import pandas as pd

PARENT_DIR = Path(__file__).parent.parent.parent.parent.absolute()
outfile = PARENT_DIR / "explorers" / "lis-expanded-poverty.explorer.tsv"

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
    "explorerTitle": "Poverty Data Explorer of the Luxembourg Income Study: Expanded metrics",
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
                ] = f"% of population living in households with {welfare['welfare_type'][wel]} below ${povlines_abs['dollars_text'][p]} a day.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}{equivalence_scales['description'][eq]}"
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
                ] = f"Number of people living in households with {welfare['welfare_type'][wel]} below ${povlines_abs['dollars_text'][p]} a day.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}{equivalence_scales['description'][eq]}"
                df_tables.loc[j, "unit"] = np.nan
                df_tables.loc[j, "shortUnit"] = np.nan
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[
                    j, "colorScaleNumericBins"
                ] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000"
                df_tables.loc[j, "colorScaleScheme"] = "Reds"
                j += 1

            # Total shortfall (abs)
            for p in range(len(povlines_abs)):
                df_tables.loc[
                    j, "name"
                ] = f"${povlines_abs['dollars_text'][p]} a day - total shortfall ({equivalence_scales['text'][eq]})"
                df_tables.loc[
                    j, "slug"
                ] = f"total_shortfall_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_{povlines_abs.cents[p]}"
                df_tables.loc[
                    j, "description"
                ] = f"The total shortfall from a poverty line of ${povlines_abs['dollars_text'][p]} a day. This is the amount of money that would be theoretically needed to lift the {welfare['welfare_type'][wel]} of all people in poverty up to the poverty line. However this is not a measure of the actual cost of eliminating poverty, since it does not take into account the costs involved in making the necessary transfers nor any changes in behaviour they would bring about.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}{equivalence_scales['description'][eq]}"
                df_tables.loc[j, "unit"] = "international-$ in 2017 prices"
                df_tables.loc[j, "shortUnit"] = "$"
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[j, "colorScaleNumericBins"] = povlines_abs[
                    "scale_total_shortfall"
                ][p]
                df_tables.loc[j, "colorScaleScheme"] = "Oranges"
                j += 1

            # Average shortfall ($)
            for p in range(len(povlines_abs)):
                df_tables.loc[
                    j, "name"
                ] = f"${povlines_abs['dollars_text'][p]} a day - average shortfall ({equivalence_scales['text'][eq]})"
                df_tables.loc[
                    j, "slug"
                ] = f"avg_shortfall_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_{povlines_abs['cents'][p]}"
                df_tables.loc[
                    j, "description"
                ] = f"The average shortfall from a poverty line of ${povlines_abs['dollars_text'][p]} (averaged across the population in poverty).{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}{equivalence_scales['description'][eq]}"
                df_tables.loc[j, "unit"] = "international-$ in 2017 prices"
                df_tables.loc[j, "shortUnit"] = "$"
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[j, "colorScaleNumericBins"] = povlines_abs[
                    "scale_avg_shortfall"
                ][p]
                df_tables.loc[j, "colorScaleScheme"] = "Purples"
                j += 1

            # Average shortfall (% of poverty line) [this is the income gap ratio]
            for p in range(len(povlines_abs)):
                df_tables.loc[
                    j, "name"
                ] = f"${povlines_abs['dollars_text'][p]} a day - income gap ratio ({equivalence_scales['text'][eq]})"
                df_tables.loc[
                    j, "slug"
                ] = f"income_gap_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_{povlines_abs['cents'][p]}"
                df_tables.loc[
                    j, "description"
                ] = f'The average shortfall from a poverty line of ${povlines_abs.dollars_text[p]} a day (averaged across the population in poverty) expressed as a share of the poverty line. This metric is sometimes called the "income gap ratio". It captures the depth of poverty in which those below the poverty line are living.{new_line}This is {welfare.technical_text[wel]}. {welfare.subtitle[wel]}{new_line}{equivalence_scales.description[eq]}'
                df_tables.loc[j, "unit"] = "%"
                df_tables.loc[j, "shortUnit"] = "%"
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[
                    j, "colorScaleNumericBins"
                ] = "10;20;30;40;50;60;70;80;90;100"
                df_tables.loc[j, "colorScaleScheme"] = "YlOrRd"
                j += 1

            # Poverty gap index
            for p in range(len(povlines_abs)):
                df_tables.loc[
                    j, "name"
                ] = f"${povlines_abs['dollars_text'][p]} a day - poverty gap index ({equivalence_scales['text'][eq]})"
                df_tables.loc[
                    j, "slug"
                ] = f"poverty_gap_index_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_{povlines_abs['cents'][p]}"
                df_tables.loc[
                    j, "description"
                ] = f"The poverty gap index calculated at a poverty line of ${povlines_abs['dollars_text'][p]} a day. The poverty gap index is a measure that reflects both the depth and prevalence of poverty. It is defined as the mean shortfall of the total population from the poverty line counting the non-poor as having zero shortfall and expressed as a percentage of the poverty line. It is worth unpacking that definition a little. For those below the poverty line, the shortfall corresponds to the amount of money required in order to reach the poverty line. For those at or above the poverty line, the shortfall is counted as zero. The average shortfall is then calculated across the total population – both poor and non-poor – and then expressed as a share of the poverty line. Unlike the more commonly-used metric of the headcount ratio, the poverty gap index is thus sensitive not only to whether a person’s income falls below the poverty line or not, but also by how much – i.e. to the depth of poverty they experience.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}{equivalence_scales['description'][eq]}"
                df_tables.loc[j, "unit"] = "%"
                df_tables.loc[j, "shortUnit"] = "%"
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[j, "colorScaleNumericBins"] = "10;20;30;40;50;60"
                df_tables.loc[j, "colorScaleScheme"] = "RdPu"
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
                ] = f"% of population living in households with {welfare['welfare_type'][wel]} below {povlines_rel['percent'][pct]} of the median {welfare['welfare_type'][wel]}.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}{equivalence_scales['description'][eq]}"
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
                ] = f"Number of people living in households with {welfare['welfare_type'][wel]} below {povlines_rel['percent'][pct]} of the median {welfare['welfare_type'][wel]}.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}{equivalence_scales['description'][eq]}"
                df_tables.loc[j, "unit"] = np.nan
                df_tables.loc[j, "shortUnit"] = np.nan
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[
                    j, "colorScaleNumericBins"
                ] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000"
                df_tables.loc[j, "colorScaleScheme"] = "YlOrBr"
                j += 1

            # Total shortfall (rel)
            for pct in range(len(povlines_rel)):
                df_tables.loc[
                    j, "name"
                ] = f"{povlines_rel['percent'][pct]} of median {welfare['welfare_type'][wel]} - total shortfall ({equivalence_scales['text'][eq]})"
                df_tables.loc[
                    j, "slug"
                ] = f"total_shortfall_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
                df_tables.loc[
                    j, "description"
                ] = f"The total shortfall from a poverty line of {povlines_rel['text'][pct]} {welfare['welfare_type'][wel]}. This is the amount of money that would be theoretically needed to lift the {welfare['welfare_type'][wel]} of all people in poverty up to the poverty line. However this is not a measure of the actual cost of eliminating poverty, since it does not take into account the costs involved in making the necessary transfers nor any changes in behaviour they would bring about.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}{equivalence_scales['description'][eq]}"
                df_tables.loc[j, "unit"] = np.nan
                df_tables.loc[j, "shortUnit"] = np.nan
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[j, "colorScaleNumericBins"] = povlines_rel[
                    "scale_total_shortfall"
                ][pct]
                df_tables.loc[j, "colorScaleScheme"] = "YlOrBr"
                j += 1

            # Average shortfall ($)
            for pct in range(len(povlines_rel)):
                df_tables.loc[
                    j, "name"
                ] = f"{povlines_rel['percent'][pct]} of median {welfare['welfare_type'][wel]} - average shortfall ({equivalence_scales['text'][eq]})"
                df_tables.loc[
                    j, "slug"
                ] = f"avg_shortfall_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
                df_tables.loc[
                    j, "description"
                ] = f"The average shortfall from a poverty line of of {povlines_rel['text'][pct]} {welfare['welfare_type'][wel]} (averaged across the population in poverty).{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}{equivalence_scales['description'][eq]}"
                df_tables.loc[j, "unit"] = "international-$ in 2017 prices"
                df_tables.loc[j, "shortUnit"] = "$"
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[j, "colorScaleNumericBins"] = "1000;2000;3000;4000;5000"
                df_tables.loc[j, "colorScaleScheme"] = "YlOrBr"
                j += 1

            # Average shortfall (% of poverty line) [this is the income gap ratio]
            for pct in range(len(povlines_rel)):
                df_tables.loc[
                    j, "name"
                ] = f"{povlines_rel['percent'][pct]} of median {welfare['welfare_type'][wel]} - income gap ratio ({equivalence_scales['text'][eq]})"
                df_tables.loc[
                    j, "slug"
                ] = f"income_gap_ratio_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
                df_tables.loc[
                    j, "description"
                ] = f'The average shortfall from a poverty line of of {povlines_rel.text[pct]} {welfare.welfare_type[wel]} (averaged across the population in poverty) expressed as a share of the poverty line. This metric is sometimes called the "income gap ratio". It captures the depth of poverty in which those below the poverty line are living.{new_line}This is {welfare.technical_text[wel]}. {welfare.subtitle[wel]}{new_line}{equivalence_scales.description[eq]}'
                df_tables.loc[j, "unit"] = "%"
                df_tables.loc[j, "shortUnit"] = "%"
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[j, "colorScaleNumericBins"] = "5;10;15;20;25;30;35;40"
                df_tables.loc[j, "colorScaleScheme"] = "YlOrBr"
                j += 1

            # Poverty gap index
            for pct in range(len(povlines_rel)):
                df_tables.loc[
                    j, "name"
                ] = f"{povlines_rel['percent'][pct]} of median {welfare['welfare_type'][wel]} - poverty gap index ({equivalence_scales['text'][eq]})"
                df_tables.loc[
                    j, "slug"
                ] = f"poverty_gap_index_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
                df_tables.loc[
                    j, "description"
                ] = f"The poverty gap index calculated at a poverty line of {povlines_rel['text'][pct]} {welfare['welfare_type'][wel]}. The poverty gap index is a measure that reflects both the depth and prevalence of poverty. It is defined as the mean shortfall of the total population from the poverty line counting the non-poor as having zero shortfall and expressed as a percentage of the poverty line. It is worth unpacking that definition a little. For those below the poverty line, the shortfall corresponds to the amount of money required in order to reach the poverty line. For those at or above the poverty line, the shortfall is counted as zero. The average shortfall is then calculated across the total population – both poor and non-poor – and then expressed as a share of the poverty line. Unlike the more commonly-used metric of the headcount ratio, the poverty gap index is thus sensitive not only to whether a person’s income falls below the poverty line or not, but also by how much – i.e. to the depth of poverty they experience.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]}{new_line}{equivalence_scales['description'][eq]}"
                df_tables.loc[j, "unit"] = "%"
                df_tables.loc[j, "shortUnit"] = "%"
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[j, "colorScaleNumericBins"] = "2;4;6;8;10;12"
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
    for wel in range(len(welfare)):
        for eq in range(len(equivalence_scales)):
            # Headcount ratio (abs)
            for p in range(len(povlines_abs)):
                df_graphers.loc[
                    j, "title"
                ] = f"{povlines_abs['title_share'][p]} ({welfare['title'][wel]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"headcount_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_{povlines_abs['cents'][p]}"
                df_graphers.loc[j, "Metric Dropdown"] = "Share in poverty"
                df_graphers.loc[
                    j, "Poverty line Dropdown"
                ] = f"{povlines_abs['povline_dropdown'][p]}"
                df_graphers.loc[
                    j, "Income type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                    "text"
                ][eq].capitalize()
                df_graphers.loc[
                    j, "subtitle"
                ] = f"{povlines_abs['subtitle'][p]} {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2017 prices. {equivalence_scales['note'][eq]}"
                df_graphers.loc[j, "type"] = np.nan
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                j += 1

            # Headcount (abs)
            for p in range(len(povlines_abs)):
                df_graphers.loc[
                    j, "title"
                ] = f"{povlines_abs.title_number[p]} ({welfare['title'][wel]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"headcount_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_{povlines_abs['cents'][p]}"
                df_graphers.loc[j, "Metric Dropdown"] = "Number in poverty"
                df_graphers.loc[
                    j, "Poverty line Dropdown"
                ] = f"{povlines_abs['povline_dropdown'][p]}"
                df_graphers.loc[
                    j, "Income type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                    "text"
                ][eq].capitalize()
                df_graphers.loc[
                    j, "subtitle"
                ] = f"{povlines_abs['subtitle'][p]} {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2017 prices. {equivalence_scales['note'][eq]}"
                df_graphers.loc[j, "type"] = np.nan
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                j += 1

            # Headcount ratio (abs) - Multiple lines
            df_graphers.loc[
                j, "title"
            ] = f"Share of population living below a range of poverty lines ({welfare['title'][wel]})"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"headcount_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_100 headcount_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_215 headcount_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_365 headcount_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_685 headcount_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_1000 headcount_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_2000 headcount_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_3000 headcount_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_4000"
            df_graphers.loc[j, "Metric Dropdown"] = "Share in poverty"
            df_graphers.loc[j, "Poverty line Dropdown"] = "Multiple lines"
            df_graphers.loc[
                j, "Income type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                "text"
            ][eq].capitalize()
            df_graphers.loc[
                j, "subtitle"
            ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. {welfare['subtitle'][wel]}"
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2017 prices. {equivalence_scales['note'][eq]}"
            df_graphers.loc[j, "type"] = np.nan
            df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
            df_graphers.loc[j, "hasMapTab"] = "false"
            df_graphers.loc[j, "tab"] = "chart"
            j += 1

            # Headcount (abs) - Multiple lines
            df_graphers.loc[
                j, "title"
            ] = f"Number of people living below a range of poverty lines ({welfare['title'][wel]})"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"headcount_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_100 headcount_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_215 headcount_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_365 headcount_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_685 headcount_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_1000 headcount_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_2000 headcount_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_3000 headcount_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_4000"
            df_graphers.loc[j, "Metric Dropdown"] = "Number in poverty"
            df_graphers.loc[j, "Poverty line Dropdown"] = "Multiple lines"
            df_graphers.loc[
                j, "Income type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                "text"
            ][eq].capitalize()
            df_graphers.loc[
                j, "subtitle"
            ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. {welfare['subtitle'][wel]}"
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2017 prices. {equivalence_scales['note'][eq]}"
            df_graphers.loc[j, "type"] = np.nan
            df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
            df_graphers.loc[j, "hasMapTab"] = "false"
            df_graphers.loc[j, "tab"] = "chart"
            j += 1

            # Total shortfall (abs)
            for p in range(len(povlines_abs)):
                df_graphers.loc[
                    j, "title"
                ] = f"{povlines_abs['title_total_shortfall'][p]} ({welfare['title'][wel]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"total_shortfall_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_{povlines_abs.cents[p]}"
                df_graphers.loc[
                    j, "Metric Dropdown"
                ] = "Total shortfall from poverty line"
                df_graphers.loc[
                    j, "Poverty line Dropdown"
                ] = f"{povlines_abs['povline_dropdown'][p]}"
                df_graphers.loc[
                    j, "Income type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                    "text"
                ][eq].capitalize()
                df_graphers.loc[
                    j, "subtitle"
                ] = f"{povlines_abs['subtitle_total_shortfall'][p]} {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = "This data is expressed in international-$ at 2017 prices. The cost of closing the poverty gap does not take into account costs and inefficiencies from making the necessary transfers."
                df_graphers.loc[j, "type"] = np.nan
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                j += 1

            # Average shortfall ($)
            for p in range(len(povlines_abs)):
                df_graphers.loc[
                    j, "title"
                ] = f"{povlines_abs['title_avg_shortfall'][p]} ({welfare['title'][wel]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"avg_shortfall_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_{povlines_abs['cents'][p]}"
                df_graphers.loc[j, "Metric Dropdown"] = "Average shortfall ($)"
                df_graphers.loc[
                    j, "Poverty line Dropdown"
                ] = f"{povlines_abs['povline_dropdown'][p]}"
                df_graphers.loc[
                    j, "Income type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                    "text"
                ][eq].capitalize()
                df_graphers.loc[
                    j, "subtitle"
                ] = f"{povlines_abs['subtitle_avg_shortfall'][p]} {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. {equivalence_scales['note'][eq]}"
                df_graphers.loc[j, "type"] = np.nan
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                j += 1

            # Average shortfall (% of poverty line)
            for p in range(len(povlines_abs)):
                df_graphers.loc[
                    j, "title"
                ] = f"{povlines_abs['title_income_gap_ratio'][p]} ({welfare['title'][wel]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"income_gap_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_{povlines_abs['cents'][p]}"
                df_graphers.loc[
                    j, "Metric Dropdown"
                ] = "Average shortfall (% of poverty line)"
                df_graphers.loc[
                    j, "Poverty line Dropdown"
                ] = f"{povlines_abs.povline_dropdown[p]}"
                df_graphers.loc[
                    j, "Income type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                    "text"
                ][eq].capitalize()
                df_graphers.loc[
                    j, "subtitle"
                ] = f"{povlines_abs['subtitle_income_gap_ratio'][p]} {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. {equivalence_scales['note'][eq]}"
                df_graphers.loc[j, "type"] = np.nan
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                j += 1

            # Poverty gap index
            for p in range(len(povlines_abs)):
                df_graphers.loc[
                    j, "title"
                ] = f"Poverty gap index at ${povlines_abs['dollars_text'][p]} a day ({welfare['title'][wel]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"poverty_gap_index_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}_{povlines_abs['cents'][p]}"
                df_graphers.loc[j, "Metric Dropdown"] = "Poverty gap index"
                df_graphers.loc[
                    j, "Poverty line Dropdown"
                ] = f"{povlines_abs['povline_dropdown'][p]}"
                df_graphers.loc[
                    j, "Income type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                    "text"
                ][eq].capitalize()
                df_graphers.loc[
                    j, "subtitle"
                ] = f"The poverty gap index is a poverty measure that reflects both the prevalence and the depth of poverty. It is calculated as the share of population in poverty multiplied by the average shortfall from the poverty line (expressed as a % of the poverty line). {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. {equivalence_scales['note'][eq]}"
                df_graphers.loc[j, "type"] = np.nan
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                j += 1

            # Headcount ratio (rel)
            for pct in range(len(povlines_rel)):
                df_graphers.loc[
                    j, "title"
                ] = f"{povlines_rel['title_share'][pct]} ({welfare['title'][wel]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"headcount_ratio_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
                df_graphers.loc[j, "Metric Dropdown"] = "Share in poverty"
                df_graphers.loc[
                    j, "Poverty line Dropdown"
                ] = f"{povlines_rel['dropdown'][pct]}"
                df_graphers.loc[
                    j, "Income type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                    "text"
                ][eq].capitalize()
                df_graphers.loc[
                    j, "subtitle"
                ] = f"Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel['text'][pct]} {welfare['welfare_type'][wel]}. {welfare['subtitle'][wel]}"
                df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
                df_graphers.loc[j, "type"] = np.nan
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                j += 1

            # Headcount (rel)
            for pct in range(len(povlines_rel)):
                df_graphers.loc[
                    j, "title"
                ] = f"{povlines_rel['title_number'][pct]} ({welfare['title'][wel]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"headcount_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
                df_graphers.loc[j, "Metric Dropdown"] = "Number in poverty"
                df_graphers.loc[
                    j, "Poverty line Dropdown"
                ] = f"{povlines_rel['dropdown'][pct]}"
                df_graphers.loc[
                    j, "Income type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                    "text"
                ][eq].capitalize()
                df_graphers.loc[
                    j, "subtitle"
                ] = f"Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel['text'][pct]} {welfare['welfare_type'][wel]}. {welfare['subtitle'][wel]}"
                df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
                df_graphers.loc[j, "type"] = np.nan
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                j += 1

            # Total shortfall (rel)
            for pct in range(len(povlines_rel)):
                df_graphers.loc[
                    j, "title"
                ] = f"Total shortfall from a poverty line of {povlines_rel['text'][pct]} {welfare['welfare_type'][wel]} ({welfare['title'][wel]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"total_shortfall_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
                df_graphers.loc[
                    j, "Metric Dropdown"
                ] = "Total shortfall from poverty line"
                df_graphers.loc[
                    j, "Poverty line Dropdown"
                ] = f"{povlines_rel['dropdown'][pct]}"
                df_graphers.loc[
                    j, "Income type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                    "text"
                ][eq].capitalize()
                df_graphers.loc[
                    j, "subtitle"
                ] = f"This is the amount of money that would be theoretically needed to lift the incomes of all people in poverty up to {povlines_rel.text[pct]} {welfare['welfare_type'][wel]}. {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. {equivalence_scales['note'][eq]}"
                df_graphers.loc[j, "type"] = np.nan
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                j += 1

            # Average shortfall ($) (rel)
            for pct in range(len(povlines_rel)):
                df_graphers.loc[
                    j, "title"
                ] = f"Average shortfall from a poverty line of {povlines_rel['text'][pct]} {welfare['welfare_type'][wel]} ({welfare['title'][wel]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"avg_shortfall_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
                df_graphers.loc[j, "Metric Dropdown"] = "Average shortfall ($)"
                df_graphers.loc[
                    j, "Poverty line Dropdown"
                ] = f"{povlines_rel['dropdown'][pct]}"
                df_graphers.loc[
                    j, "Income type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                    "text"
                ][eq].capitalize()
                df_graphers.loc[
                    j, "subtitle"
                ] = f"This is the amount of money that would be theoretically needed to lift the incomes of all people in poverty up to {povlines_rel['text'][pct]} {welfare['welfare_type'][wel]}, averaged across the population in poverty. {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. {equivalence_scales['note'][eq]}"
                df_graphers.loc[j, "type"] = np.nan
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                j += 1

            # Average shortfall (% of poverty line) (rel)
            for pct in range(len(povlines_rel)):
                df_graphers.loc[
                    j, "title"
                ] = f"Average shortfall from a poverty line of {povlines_rel['text'][pct]} {welfare['welfare_type'][wel]} (as a share of the poverty line) ({welfare['title'][wel]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"income_gap_ratio_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
                df_graphers.loc[
                    j, "Metric Dropdown"
                ] = "Average shortfall (% of poverty line)"
                df_graphers.loc[
                    j, "Poverty line Dropdown"
                ] = f"{povlines_rel['dropdown'][pct]}"
                df_graphers.loc[
                    j, "Income type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                    "text"
                ][eq].capitalize()
                df_graphers.loc[
                    j, "subtitle"
                ] = f'This is the average shortfall expressed as a share of the poverty line, sometimes called the "income gap ratio". It captures the depth of poverty in which those below {povlines_rel.text[pct]} {welfare.welfare_type[wel]} are living. {welfare.subtitle[wel]}'
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. {equivalence_scales['note'][eq]}"
                df_graphers.loc[j, "type"] = np.nan
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                j += 1

            # Poverty gap index (rel)
            for pct in range(len(povlines_rel)):
                df_graphers.loc[
                    j, "title"
                ] = f"Poverty gap index at {povlines_rel['text'][pct]} {welfare['welfare_type'][wel]} ({welfare['title'][wel]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"poverty_gap_index_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
                df_graphers.loc[j, "Metric Dropdown"] = "Poverty gap index"
                df_graphers.loc[
                    j, "Poverty line Dropdown"
                ] = f"{povlines_rel['dropdown'][pct]}"
                df_graphers.loc[
                    j, "Income type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
                    "text"
                ][eq].capitalize()
                df_graphers.loc[
                    j, "subtitle"
                ] = f"The poverty gap index is a poverty measure that reflects both the prevalence and the depth of poverty. It is calculated as the share of population in poverty multiplied by the average shortfall from the poverty line (expressed as a % of the poverty line). {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. {equivalence_scales['note'][eq]}"
                df_graphers.loc[j, "type"] = np.nan
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                j += 1

        # Compare equivalized and per capita values
        # Headcount ratio (abs)
        for p in range(len(povlines_abs)):
            df_graphers.loc[
                j, "title"
            ] = f"{povlines_abs['title_share'][p]} ({welfare['title'][wel]}, equivalized vs. per capita)"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"headcount_ratio_{welfare['slug'][wel]}_eq_{povlines_abs['cents'][p]} headcount_ratio_{welfare['slug'][wel]}_pc_{povlines_abs['cents'][p]}"
            df_graphers.loc[j, "Metric Dropdown"] = "Share in poverty"
            df_graphers.loc[
                j, "Poverty line Dropdown"
            ] = f"{povlines_abs['povline_dropdown'][p]}"
            df_graphers.loc[
                j, "Income type Dropdown"
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
            ] = f"{povlines_abs.title_number[p]} ({welfare['title'][wel]}, equivalized vs. per capita)"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"headcount_{welfare['slug'][wel]}_eq_{povlines_abs['cents'][p]} headcount_{welfare['slug'][wel]}_pc_{povlines_abs['cents'][p]}"
            df_graphers.loc[j, "Metric Dropdown"] = "Number in poverty"
            df_graphers.loc[
                j, "Poverty line Dropdown"
            ] = f"{povlines_abs['povline_dropdown'][p]}"
            df_graphers.loc[
                j, "Income type Dropdown"
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

        # Total shortfall (abs)
        for p in range(len(povlines_abs)):
            df_graphers.loc[
                j, "title"
            ] = f"{povlines_abs['title_total_shortfall'][p]} ({welfare['title'][wel]}, equivalized vs. per capita)"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"total_shortfall_{welfare['slug'][wel]}_eq_{povlines_abs.cents[p]} total_shortfall_{welfare['slug'][wel]}_pc_{povlines_abs.cents[p]}"
            df_graphers.loc[j, "Metric Dropdown"] = "Total shortfall from poverty line"
            df_graphers.loc[
                j, "Poverty line Dropdown"
            ] = f"{povlines_abs['povline_dropdown'][p]}"
            df_graphers.loc[
                j, "Income type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[
                j, "Equivalence scale Dropdown"
            ] = "Equivalized vs. per capita"
            df_graphers.loc[
                j, "subtitle"
            ] = f"{povlines_abs['subtitle_total_shortfall'][p]} {welfare['subtitle'][wel]}"
            df_graphers.loc[
                j, "note"
            ] = "This data is expressed in international-$ at 2017 prices. The cost of closing the poverty gap does not take into account costs and inefficiencies from making the necessary transfers."
            df_graphers.loc[j, "type"] = np.nan
            df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
            df_graphers.loc[j, "hasMapTab"] = "false"
            df_graphers.loc[j, "tab"] = "chart"
            j += 1

        # Average shortfall ($)
        for p in range(len(povlines_abs)):
            df_graphers.loc[
                j, "title"
            ] = f"{povlines_abs['title_avg_shortfall'][p]} ({welfare['title'][wel]}, equivalized vs. per capita)"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"avg_shortfall_{welfare['slug'][wel]}_eq_{povlines_abs['cents'][p]} avg_shortfall_{welfare['slug'][wel]}_pc_{povlines_abs['cents'][p]}"
            df_graphers.loc[j, "Metric Dropdown"] = "Average shortfall ($)"
            df_graphers.loc[
                j, "Poverty line Dropdown"
            ] = f"{povlines_abs['povline_dropdown'][p]}"
            df_graphers.loc[
                j, "Income type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[
                j, "Equivalence scale Dropdown"
            ] = "Equivalized vs. per capita"
            df_graphers.loc[
                j, "subtitle"
            ] = f"{povlines_abs['subtitle_avg_shortfall'][p]} {welfare['subtitle'][wel]}"
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries."
            df_graphers.loc[j, "type"] = np.nan
            df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
            df_graphers.loc[j, "hasMapTab"] = "false"
            df_graphers.loc[j, "tab"] = "chart"
            j += 1

        # Average shortfall (% of poverty line)
        for p in range(len(povlines_abs)):
            df_graphers.loc[
                j, "title"
            ] = f"{povlines_abs['title_income_gap_ratio'][p]} ({welfare['title'][wel]}, equivalized vs. per capita)"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"income_gap_ratio_{welfare['slug'][wel]}_eq_{povlines_abs['cents'][p]} income_gap_ratio_{welfare['slug'][wel]}_pc_{povlines_abs['cents'][p]}"
            df_graphers.loc[
                j, "Metric Dropdown"
            ] = "Average shortfall (% of poverty line)"
            df_graphers.loc[
                j, "Poverty line Dropdown"
            ] = f"{povlines_abs.povline_dropdown[p]}"
            df_graphers.loc[
                j, "Income type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[
                j, "Equivalence scale Dropdown"
            ] = "Equivalized vs. per capita"
            df_graphers.loc[
                j, "subtitle"
            ] = f"{povlines_abs['subtitle_income_gap_ratio'][p]} {welfare['subtitle'][wel]}"
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries."
            df_graphers.loc[j, "type"] = np.nan
            df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
            df_graphers.loc[j, "hasMapTab"] = "false"
            df_graphers.loc[j, "tab"] = "chart"
            j += 1

        # Poverty gap index
        for p in range(len(povlines_abs)):
            df_graphers.loc[
                j, "title"
            ] = f"Poverty gap index at ${povlines_abs['dollars_text'][p]} a day ({welfare['title'][wel]}, equivalized vs. per capita)"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"poverty_gap_index_{welfare['slug'][wel]}_eq_{povlines_abs['cents'][p]} poverty_gap_index_{welfare['slug'][wel]}_pc_{povlines_abs['cents'][p]}"
            df_graphers.loc[j, "Metric Dropdown"] = "Poverty gap index"
            df_graphers.loc[
                j, "Poverty line Dropdown"
            ] = f"{povlines_abs['povline_dropdown'][p]}"
            df_graphers.loc[
                j, "Income type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[
                j, "Equivalence scale Dropdown"
            ] = "Equivalized vs. per capita"
            df_graphers.loc[
                j, "subtitle"
            ] = f"The poverty gap index is a poverty measure that reflects both the prevalence and the depth of poverty. It is calculated as the share of population in poverty multiplied by the average shortfall from the poverty line (expressed as a % of the poverty line). {welfare['subtitle'][wel]}"
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries."
            df_graphers.loc[j, "type"] = np.nan
            df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
            df_graphers.loc[j, "hasMapTab"] = "false"
            df_graphers.loc[j, "tab"] = "chart"
            j += 1

        # Headcount ratio (rel)
        for pct in range(len(povlines_rel)):
            df_graphers.loc[
                j, "title"
            ] = f"{povlines_rel['title_share'][pct]} ({welfare['title'][wel]}, equivalized vs. per capita)"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"headcount_ratio_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_eq headcount_ratio_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_pc"
            df_graphers.loc[j, "Metric Dropdown"] = "Share in poverty"
            df_graphers.loc[
                j, "Poverty line Dropdown"
            ] = f"{povlines_rel['dropdown'][pct]}"
            df_graphers.loc[
                j, "Income type Dropdown"
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
            ] = f"{povlines_rel['title_number'][pct]} ({welfare['title'][wel]}, equivalized vs. per capita)"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"headcount_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_eq headcount_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_pc"
            df_graphers.loc[j, "Metric Dropdown"] = "Number in poverty"
            df_graphers.loc[
                j, "Poverty line Dropdown"
            ] = f"{povlines_rel['dropdown'][pct]}"
            df_graphers.loc[
                j, "Income type Dropdown"
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

        # Total shortfall (rel)
        for pct in range(len(povlines_rel)):
            df_graphers.loc[
                j, "title"
            ] = f"Total shortfall from a poverty line of {povlines_rel['text'][pct]} {welfare['welfare_type'][wel]} ({welfare['title'][wel]}, equivalized vs. per capita)"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"total_shortfall_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_eq total_shortfall_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_pc"
            df_graphers.loc[j, "Metric Dropdown"] = "Total shortfall from poverty line"
            df_graphers.loc[
                j, "Poverty line Dropdown"
            ] = f"{povlines_rel['dropdown'][pct]}"
            df_graphers.loc[
                j, "Income type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[
                j, "Equivalence scale Dropdown"
            ] = "Equivalized vs. per capita"
            df_graphers.loc[
                j, "subtitle"
            ] = f"This is the amount of money that would be theoretically needed to lift the incomes of all people in poverty up to {povlines_rel.text[pct]} {welfare['welfare_type'][wel]}. {welfare['subtitle'][wel]}"
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries."
            df_graphers.loc[j, "type"] = np.nan
            df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
            df_graphers.loc[j, "hasMapTab"] = "false"
            df_graphers.loc[j, "tab"] = "chart"
            j += 1

        # Average shortfall ($) (rel)
        for pct in range(len(povlines_rel)):
            df_graphers.loc[
                j, "title"
            ] = f"Average shortfall from a poverty line of {povlines_rel['text'][pct]} {welfare['welfare_type'][wel]} ({welfare['title'][wel]}, equivalized vs. per capita)"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"avg_shortfall_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_eq avg_shortfall_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_pc"
            df_graphers.loc[j, "Metric Dropdown"] = "Average shortfall ($)"
            df_graphers.loc[
                j, "Poverty line Dropdown"
            ] = f"{povlines_rel['dropdown'][pct]}"
            df_graphers.loc[
                j, "Income type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[
                j, "Equivalence scale Dropdown"
            ] = "Equivalized vs. per capita"
            df_graphers.loc[
                j, "subtitle"
            ] = f"This is the amount of money that would be theoretically needed to lift the incomes of all people in poverty up to {povlines_rel['text'][pct]} {welfare['welfare_type'][wel]}, averaged across the population in poverty. {welfare['subtitle'][wel]}"
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries."
            df_graphers.loc[j, "type"] = np.nan
            df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
            df_graphers.loc[j, "hasMapTab"] = "false"
            df_graphers.loc[j, "tab"] = "chart"
            j += 1

        # Average shortfall (% of poverty line) (rel)
        for pct in range(len(povlines_rel)):
            df_graphers.loc[
                j, "title"
            ] = f"Average shortfall from a poverty line of {povlines_rel['text'][pct]} {welfare['welfare_type'][wel]} (as a share of the poverty line) ({welfare['title'][wel]}, equivalized vs. per capita)"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"income_gap_ratio_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_eq income_gap_ratio_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_pc"
            df_graphers.loc[
                j, "Metric Dropdown"
            ] = "Average shortfall (% of poverty line)"
            df_graphers.loc[
                j, "Poverty line Dropdown"
            ] = f"{povlines_rel['dropdown'][pct]}"
            df_graphers.loc[
                j, "Income type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[
                j, "Equivalence scale Dropdown"
            ] = "Equivalized vs. per capita"
            df_graphers.loc[
                j, "subtitle"
            ] = f'This is the average shortfall expressed as a share of the poverty line, sometimes called the "income gap ratio". It captures the depth of poverty in which those below {povlines_rel.text[pct]} {welfare.welfare_type[wel]} are living. {welfare.subtitle[wel]}'
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries."
            df_graphers.loc[j, "type"] = np.nan
            df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
            df_graphers.loc[j, "hasMapTab"] = "false"
            df_graphers.loc[j, "tab"] = "chart"
            j += 1

        # Poverty gap index (rel)
        for pct in range(len(povlines_rel)):
            df_graphers.loc[
                j, "title"
            ] = f"Poverty gap index at {povlines_rel['text'][pct]} {welfare['welfare_type'][wel]} ({welfare['title'][wel]}, equivalized vs. per capita)"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"poverty_gap_index_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_eq poverty_gap_index_{povlines_rel['slug_suffix'][pct]}_{welfare['slug'][wel]}_pc"
            df_graphers.loc[j, "Metric Dropdown"] = "Poverty gap index"
            df_graphers.loc[
                j, "Poverty line Dropdown"
            ] = f"{povlines_rel['dropdown'][pct]}"
            df_graphers.loc[
                j, "Income type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[
                j, "Equivalence scale Dropdown"
            ] = "Equivalized vs. per capita"
            df_graphers.loc[
                j, "subtitle"
            ] = f"The poverty gap index is a poverty measure that reflects both the prevalence and the depth of poverty. It is calculated as the share of population in poverty multiplied by the average shortfall from the poverty line (expressed as a % of the poverty line). {welfare['subtitle'][wel]}"
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries."
            df_graphers.loc[j, "type"] = np.nan
            df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
            df_graphers.loc[j, "hasMapTab"] = "false"
            df_graphers.loc[j, "tab"] = "chart"
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
    & (df_graphers["Income type Dropdown"] == "Before tax")
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
