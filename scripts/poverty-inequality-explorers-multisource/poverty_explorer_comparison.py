# %% [markdown]
# # Inequality Data Explorer - Source Comparison
# This code creates the tsv file for the comparison poverty explorer, available [here](https://owid.cloud/admin/explorers/preview/poverty_comparison)

import textwrap
from pathlib import Path

import numpy as np

# %%
import pandas as pd

PARENT_DIR = Path(__file__).parent.parent.parent.absolute()
outfile = PARENT_DIR / "explorers" / "poverty_comparison.explorer.tsv"

# %% [markdown]
# ## Google sheets auxiliar data
# These spreadsheets provide with different details depending on each type of welfare measure or tables considered.

# %%
# MULTI-SOURCE
# Read Google sheets
sheet_id = "1wcFsNZCEn_6SJ05BFkXKLUyvCrnigfR8eeemGKgAYsI"

# Merged sheet (this contains PIP, WID and LIS dataset information together in one file)
sheet_name = "merged_tables"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
merged_tables = pd.read_csv(url, keep_default_na=False)

# Source checkbox covers all the possible combinations to get for the multi-source selector
sheet_name = "source_checkbox"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
source_checkbox = pd.read_csv(
    url, keep_default_na=False, dtype={"pip": "str", "wid": "str", "lis": "str"}
)

# LUXEMBOURG INCOME STUDY
# Read Google sheets
sheet_id = "1UFdwB1iBpP2tEP6GtxCHvW1GGhjsFflh42FWR80rYIg"

# Welfare type sheet
sheet_name = "welfare"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
lis_welfare = pd.read_csv(url, keep_default_na=False)

# Equivalence scales
sheet_name = "equivalence_scales"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
lis_equivalence_scales = pd.read_csv(url, keep_default_na=False)

# Absolute poverty sheet
sheet_name = "povlines_abs"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
lis_povlines_abs = pd.read_csv(url, dtype={"dollars_text": "str"})

# Relative poverty sheet
sheet_name = "povlines_rel"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
lis_povlines_rel = pd.read_csv(url)

# WORLD BANK POVERTY AND INEQUALITY PLATFORM
# Read Google sheets
sheet_id = "17KJ9YcvfdmO_7-Sv2Ij0vmzAQI6rXSIqHfJtgFHN-a8"

# Survey type sheet
sheet_name = "table"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
pip_tables = pd.read_csv(url)

# Absolute poverty sheet
sheet_name = "povlines_abs"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
pip_povlines_abs = pd.read_csv(url, dtype={"dollars_text": "str"})

# Relative poverty sheet
sheet_name = "povlines_rel"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
pip_povlines_rel = pd.read_csv(url)

# %% [markdown]
# ## Header
# General settings of the explorer are defined here, like the title, subtitle, default country selection, publishing status and others.

# %%
# The header is defined as a dictionary first and then it is converted into a index-oriented dataframe
header_dict = {
    "explorerTitle": "Poverty Data Explorer - Source comparison",
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
    "googleSheet": "",
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

###########################################################################################
# WORLD BANK POVERTY AND INEQUALITY PLATFORM
###########################################################################################
sourceName = "World Bank Poverty and Inequality Platform (PIP) (2022)"
dataPublishedBy = "World Bank. (2022). Poverty and Inequality Platform (version 20220909_2017_01_02_PROD) [Data set]. World Bank Group. https://pip.worldbank.org/. Accessed  2022-10-03."
sourceLink = "https://pip.worldbank.org/"
colorScaleNumericMinValue = 0
tolerance = 5
colorScaleEqualSizeBins = "true"
tableSlug = "poverty_inequality"
new_line = "<br><br>"

# Table generation
df_tables_pip = pd.DataFrame()
j = 0

for tab in range(len(pip_tables)):
    # Define country as entityName
    df_tables_pip.loc[j, "name"] = "Country"
    df_tables_pip.loc[j, "slug"] = "country"
    df_tables_pip.loc[j, "type"] = "EntityName"
    j += 1

    # Define year as Year
    df_tables_pip.loc[j, "name"] = "Year"
    df_tables_pip.loc[j, "slug"] = "year"
    df_tables_pip.loc[j, "type"] = "Year"
    j += 1

    # Headcount ratio (abs)
    for p in range(len(pip_povlines_abs)):
        df_tables_pip.loc[
            j, "name"
        ] = f"Share below ${pip_povlines_abs.dollars_text[p]} a day (PIP)"
        df_tables_pip.loc[j, "slug"] = f"headcount_ratio_{pip_povlines_abs.cents[p]}"
        df_tables_pip.loc[
            j, "description"
        ] = f"% of population living in households with an {pip_tables.text[tab]} per person below ${pip_povlines_abs.dollars_text[p]} a day."
        df_tables_pip.loc[j, "unit"] = "%"
        df_tables_pip.loc[j, "shortUnit"] = "%"
        df_tables_pip.loc[j, "type"] = "Numeric"
        df_tables_pip.loc[
            j, "colorScaleNumericBins"
        ] = "3;10;20;30;40;50;60;70;80;90;100"
        df_tables_pip.loc[j, "colorScaleScheme"] = "OrRd"
        j += 1

    # Headcount (abs)
    for p in range(len(pip_povlines_abs)):
        df_tables_pip.loc[
            j, "name"
        ] = f"Number below ${pip_povlines_abs.dollars_text[p]} a day (PIP)"
        df_tables_pip.loc[j, "slug"] = f"headcount_{pip_povlines_abs.cents[p]}"
        df_tables_pip.loc[
            j, "description"
        ] = f"Number of people living in households with an {pip_tables.text[tab]} per person below ${pip_povlines_abs.dollars_text[p]} a day."
        df_tables_pip.loc[j, "unit"] = np.nan
        df_tables_pip.loc[j, "shortUnit"] = np.nan
        df_tables_pip.loc[j, "type"] = "Numeric"
        df_tables_pip.loc[
            j, "colorScaleNumericBins"
        ] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df_tables_pip.loc[j, "colorScaleScheme"] = "Reds"
        j += 1

    # Total shortfall (abs)
    for p in range(len(pip_povlines_abs)):
        df_tables_pip.loc[
            j, "name"
        ] = f"${pip_povlines_abs.dollars_text[p]} a day - total daily shortfall (PIP)"
        df_tables_pip.loc[j, "slug"] = f"total_shortfall_{pip_povlines_abs.cents[p]}"
        df_tables_pip.loc[
            j, "description"
        ] = f"The total shortfall from a poverty line of ${pip_povlines_abs.dollars_text[p]} a day. This is the amount of money that would be theoretically needed to lift the {pip_tables.text[tab]} of all people in poverty up to the poverty line. However this is not a measure of the actual cost of eliminating poverty, since it does not take into account the costs involved in making the necessary transfers nor any changes in behaviour they would bring about."
        df_tables_pip.loc[j, "unit"] = "international-$ in 2017 prices"
        df_tables_pip.loc[j, "shortUnit"] = "$"
        df_tables_pip.loc[j, "type"] = "Numeric"
        df_tables_pip.loc[
            j, "colorScaleNumericBins"
        ] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df_tables_pip.loc[j, "colorScaleScheme"] = "Oranges"
        j += 1

    # Average shortfall ($ per day)
    for p in range(len(pip_povlines_abs)):
        df_tables_pip.loc[
            j, "name"
        ] = f"${pip_povlines_abs.dollars_text[p]} a day - average daily shortfall (PIP)"
        df_tables_pip.loc[j, "slug"] = f"avg_shortfall_{pip_povlines_abs.cents[p]}"
        df_tables_pip.loc[
            j, "description"
        ] = f"The average shortfall from a poverty line of ${pip_povlines_abs.dollars_text[p]} a day (averaged across the population in poverty)."
        df_tables_pip.loc[j, "unit"] = "international-$ in 2017 prices"
        df_tables_pip.loc[j, "shortUnit"] = "$"
        df_tables_pip.loc[j, "type"] = "Numeric"
        df_tables_pip.loc[
            j, "colorScaleNumericBins"
        ] = pip_povlines_abs.scale_avg_shortfall[p]
        df_tables_pip.loc[j, "colorScaleScheme"] = "Purples"
        j += 1

    # Average shortfall (% of poverty line) [this is the income gap ratio]
    for p in range(len(pip_povlines_abs)):
        df_tables_pip.loc[
            j, "name"
        ] = f"${pip_povlines_abs.dollars_text[p]} a day - income gap ratio (PIP)"
        df_tables_pip.loc[j, "slug"] = f"income_gap_ratio_{pip_povlines_abs.cents[p]}"
        df_tables_pip.loc[
            j, "description"
        ] = f'The average shortfall from a poverty line of ${pip_povlines_abs.dollars_text[p]} a day (averaged across the population in poverty) expressed as a share of the poverty line. This metric is sometimes called the "income gap ratio". It captures the depth of poverty in which those below the poverty line are living.'
        df_tables_pip.loc[j, "unit"] = "%"
        df_tables_pip.loc[j, "shortUnit"] = "%"
        df_tables_pip.loc[j, "type"] = "Numeric"
        df_tables_pip.loc[j, "colorScaleNumericBins"] = "10;20;30;40;50;60;70;80;90;100"
        df_tables_pip.loc[j, "colorScaleScheme"] = "YlOrRd"
        j += 1

    # Poverty gap index
    for p in range(len(pip_povlines_abs)):
        df_tables_pip.loc[
            j, "name"
        ] = f"${pip_povlines_abs.dollars_text[p]} a day - poverty gap index (PIP)"
        df_tables_pip.loc[j, "slug"] = f"poverty_gap_index_{pip_povlines_abs.cents[p]}"
        df_tables_pip.loc[
            j, "description"
        ] = f"The poverty gap index calculated at a poverty line of ${pip_povlines_abs.dollars_text[p]} a day. The poverty gap index is a measure that reflects both the depth and prevalence of poverty. It is defined as the mean shortfall of the total population from the poverty line counting the non-poor as having zero shortfall and expressed as a percentage of the poverty line. It is worth unpacking that definition a little. For those below the poverty line, the shortfall corresponds to the amount of money required in order to reach the poverty line. For those at or above the poverty line, the shortfall is counted as zero. The average shortfall is then calculated across the total population – both poor and non-poor – and then expressed as a share of the poverty line. Unlike the more commonly-used metric of the headcount ratio, the poverty gap index is thus sensitive not only to whether a person’s income falls below the poverty line or not, but also by how much – i.e. to the depth of poverty they experience."
        df_tables_pip.loc[j, "unit"] = "%"
        df_tables_pip.loc[j, "shortUnit"] = "%"
        df_tables_pip.loc[j, "type"] = "Numeric"
        df_tables_pip.loc[j, "colorScaleNumericBins"] = "10;20;30;40;50;60;70;80;90;100"
        df_tables_pip.loc[j, "colorScaleScheme"] = "RdPu"
        j += 1

    # Headcount ratio (rel)
    for pct in range(len(pip_povlines_rel)):
        df_tables_pip.loc[
            j, "name"
        ] = f"{pip_povlines_rel.percent[pct]} of median - share of population below poverty line (PIP)"
        df_tables_pip.loc[
            j, "slug"
        ] = f"headcount_ratio_{pip_povlines_rel.slug_suffix[pct]}"
        df_tables_pip.loc[
            j, "description"
        ] = f"% of population living in households with an {pip_tables.text[tab]} per person below {pip_povlines_rel.percent[pct]} of the median."
        df_tables_pip.loc[j, "unit"] = "%"
        df_tables_pip.loc[j, "shortUnit"] = "%"
        df_tables_pip.loc[j, "type"] = "Numeric"
        df_tables_pip.loc[j, "colorScaleNumericBins"] = "5;10;15;20;25;30;30.0001"
        df_tables_pip.loc[j, "colorScaleScheme"] = "YlOrBr"
        j += 1

    # Headcount (rel)
    for pct in range(len(pip_povlines_rel)):
        df_tables_pip.loc[
            j, "name"
        ] = f"{pip_povlines_rel.percent[pct]} of median - total number of people below poverty line (PIP)"
        df_tables_pip.loc[j, "slug"] = f"headcount_{pip_povlines_rel.slug_suffix[pct]}"
        df_tables_pip.loc[
            j, "description"
        ] = f"Number of people living in households with an {pip_tables.text[tab]} per person below {pip_povlines_rel.percent[pct]} of the median."
        df_tables_pip.loc[j, "unit"] = np.nan
        df_tables_pip.loc[j, "shortUnit"] = np.nan
        df_tables_pip.loc[j, "type"] = "Numeric"
        df_tables_pip.loc[
            j, "colorScaleNumericBins"
        ] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df_tables_pip.loc[j, "colorScaleScheme"] = "YlOrBr"
        j += 1

    # Total shortfall (rel)
    for pct in range(len(pip_povlines_rel)):
        df_tables_pip.loc[
            j, "name"
        ] = f"{pip_povlines_rel.percent[pct]} of median - total daily shortfall (PIP)"
        df_tables_pip.loc[
            j, "slug"
        ] = f"total_shortfall_{pip_povlines_rel.slug_suffix[pct]}"
        df_tables_pip.loc[
            j, "description"
        ] = f"The total shortfall from a poverty line of {pip_povlines_rel.text[pct]} {pip_tables.text[tab]}. This is the amount of money that would be theoretically needed to lift the {pip_tables.text[tab]} of all people in poverty up to the poverty line. However this is not a measure of the actual cost of eliminating poverty, since it does not take into account the costs involved in making the necessary transfers nor any changes in behaviour they would bring about."
        df_tables_pip.loc[j, "unit"] = np.nan
        df_tables_pip.loc[j, "shortUnit"] = np.nan
        df_tables_pip.loc[j, "type"] = "Numeric"
        df_tables_pip.loc[
            j, "colorScaleNumericBins"
        ] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df_tables_pip.loc[j, "colorScaleScheme"] = "YlOrBr"
        j += 1

    # Average shortfall ($ per day)
    for pct in range(len(pip_povlines_rel)):
        df_tables_pip.loc[
            j, "name"
        ] = f"{pip_povlines_rel.percent[pct]} of median - average daily shortfall (PIP)"
        df_tables_pip.loc[
            j, "slug"
        ] = f"avg_shortfall_{pip_povlines_rel.slug_suffix[pct]}"
        df_tables_pip.loc[
            j, "description"
        ] = f"The average shortfall from a poverty line of of {pip_povlines_rel.text[pct]} {pip_tables.text[tab]} (averaged across the population in poverty)."
        df_tables_pip.loc[j, "unit"] = "international-$ in 2017 prices"
        df_tables_pip.loc[j, "shortUnit"] = "$"
        df_tables_pip.loc[j, "type"] = "Numeric"
        df_tables_pip.loc[j, "colorScaleNumericBins"] = "1;2;5;10;20;20.0001"
        df_tables_pip.loc[j, "colorScaleScheme"] = "YlOrBr"
        j += 1

    # Average shortfall (% of poverty line) [this is the income gap ratio]
    for pct in range(len(pip_povlines_rel)):
        df_tables_pip.loc[
            j, "name"
        ] = f"{pip_povlines_rel.percent[pct]} of median - income gap ratio (PIP)"
        df_tables_pip.loc[
            j, "slug"
        ] = f"income_gap_ratio_{pip_povlines_rel.slug_suffix[pct]}"
        df_tables_pip.loc[
            j, "description"
        ] = f'The average shortfall from a poverty line of of {pip_povlines_rel.text[pct]} {pip_tables.text[tab]} (averaged across the population in poverty) expressed as a share of the poverty line. This metric is sometimes called the "income gap ratio". It captures the depth of poverty in which those below the poverty line are living.'
        df_tables_pip.loc[j, "unit"] = "%"
        df_tables_pip.loc[j, "shortUnit"] = "%"
        df_tables_pip.loc[j, "type"] = "Numeric"
        df_tables_pip.loc[j, "colorScaleNumericBins"] = "10;20;30;40;50;60;70;80;90;100"
        df_tables_pip.loc[j, "colorScaleScheme"] = "YlOrBr"
        j += 1

    # Poverty gap index
    for pct in range(len(pip_povlines_rel)):
        df_tables_pip.loc[
            j, "name"
        ] = f"{pip_povlines_rel.percent[pct]} of median - poverty gap index (PIP)"
        df_tables_pip.loc[
            j, "slug"
        ] = f"poverty_gap_index_{pip_povlines_rel.slug_suffix[pct]}"
        df_tables_pip.loc[
            j, "description"
        ] = f"The poverty gap index calculated at a poverty line of {pip_povlines_rel.text[pct]} {pip_tables.text[tab]}. The poverty gap index is a measure that reflects both the depth and prevalence of poverty. It is defined as the mean shortfall of the total population from the poverty line counting the non-poor as having zero shortfall and expressed as a percentage of the poverty line. It is worth unpacking that definition a little. For those below the poverty line, the shortfall corresponds to the amount of money required in order to reach the poverty line. For those at or above the poverty line, the shortfall is counted as zero. The average shortfall is then calculated across the total population – both poor and non-poor – and then expressed as a share of the poverty line. Unlike the more commonly-used metric of the headcount ratio, the poverty gap index is thus sensitive not only to whether a person’s income falls below the poverty line or not, but also by how much – i.e. to the depth of poverty they experience."
        df_tables_pip.loc[j, "unit"] = "%"
        df_tables_pip.loc[j, "shortUnit"] = "%"
        df_tables_pip.loc[j, "type"] = "Numeric"
        df_tables_pip.loc[j, "colorScaleNumericBins"] = "3;6;9;12;15;18;21"
        df_tables_pip.loc[j, "colorScaleScheme"] = "YlOrBr"
        j += 1

df_tables_pip["tableSlug"] = tableSlug
df_tables_pip["sourceName"] = sourceName
df_tables_pip["dataPublishedBy"] = dataPublishedBy
df_tables_pip["sourceLink"] = sourceLink
df_tables_pip["colorScaleNumericMinValue"] = colorScaleNumericMinValue
df_tables_pip["tolerance"] = tolerance

###########################################################################################
# LUXEMBOURG INCOME STUDY (LIS)
###########################################################################################
sourceName = "Luxembourg Income Study (LIS) (2023)"
dataPublishedBy = "Luxembourg Income Study (LIS) Database, http://www.lisdatacenter.org (multiple countries; 1967-2020). Luxembourg, LIS."
sourceLink = "https://www.lisdatacenter.org/our-data/lis-database/"
colorScaleNumericMinValue = 0
tolerance = 5
colorScaleEqualSizeBins = "true"
new_line = "<br><br>"

df_tables_lis = pd.DataFrame()
j = 0

for tab in range(len(merged_tables)):
    for wel in range(len(lis_welfare)):
        for eq in range(len(lis_equivalence_scales)):
            # Headcount ratio (abs)
            for p in range(len(lis_povlines_abs)):
                df_tables_lis.loc[
                    j, "name"
                ] = f"Share below ${lis_povlines_abs['dollars_text'][p]} a day (LIS)"
                df_tables_lis.loc[
                    j, "slug"
                ] = f"headcount_ratio_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}_{lis_povlines_abs['cents'][p]}"
                df_tables_lis.loc[
                    j, "description"
                ] = f"% of population living in households with {lis_welfare['welfare_type'][wel]} below ${lis_povlines_abs['dollars_text'][p]} a day.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
                df_tables_lis.loc[j, "unit"] = "%"
                df_tables_lis.loc[j, "shortUnit"] = "%"
                df_tables_lis.loc[j, "type"] = "Numeric"
                df_tables_lis.loc[
                    j, "colorScaleNumericBins"
                ] = "3;10;20;30;40;50;60;70;80;90;100"
                df_tables_lis.loc[j, "colorScaleScheme"] = "OrRd"
                j += 1

            # Headcount (abs)
            for p in range(len(lis_povlines_abs)):
                df_tables_lis.loc[
                    j, "name"
                ] = f"Number below ${lis_povlines_abs['dollars_text'][p]} a day (LIS)"
                df_tables_lis.loc[
                    j, "slug"
                ] = f"headcount_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}_{lis_povlines_abs['cents'][p]}"
                df_tables_lis.loc[
                    j, "description"
                ] = f"Number of people living in households with {lis_welfare['welfare_type'][wel]} below ${lis_povlines_abs['dollars_text'][p]} a day.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
                df_tables_lis.loc[j, "unit"] = np.nan
                df_tables_lis.loc[j, "shortUnit"] = np.nan
                df_tables_lis.loc[j, "type"] = "Numeric"
                df_tables_lis.loc[
                    j, "colorScaleNumericBins"
                ] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000"
                df_tables_lis.loc[j, "colorScaleScheme"] = "Reds"
                j += 1

            # Total shortfall (abs)
            for p in range(len(lis_povlines_abs)):
                df_tables_lis.loc[
                    j, "name"
                ] = f"${lis_povlines_abs['dollars_text'][p]} a day - total shortfall (LIS)"
                df_tables_lis.loc[
                    j, "slug"
                ] = f"total_shortfall_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}_{lis_povlines_abs.cents[p]}"
                df_tables_lis.loc[
                    j, "description"
                ] = f"The total shortfall from a poverty line of ${lis_povlines_abs['dollars_text'][p]} a day. This is the amount of money that would be theoretically needed to lift the {lis_welfare['welfare_type'][wel]} of all people in poverty up to the poverty line. However this is not a measure of the actual cost of eliminating poverty, since it does not take into account the costs involved in making the necessary transfers nor any changes in behaviour they would bring about.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
                df_tables_lis.loc[j, "unit"] = "international-$ in 2017 prices"
                df_tables_lis.loc[j, "shortUnit"] = "$"
                df_tables_lis.loc[j, "type"] = "Numeric"
                df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_povlines_abs[
                    "scale_total_shortfall"
                ][p]
                df_tables_lis.loc[j, "colorScaleScheme"] = "Oranges"
                j += 1

            # Average shortfall ($)
            for p in range(len(lis_povlines_abs)):
                df_tables_lis.loc[
                    j, "name"
                ] = f"${lis_povlines_abs['dollars_text'][p]} a day - average shortfall (LIS)"
                df_tables_lis.loc[
                    j, "slug"
                ] = f"avg_shortfall_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}_{lis_povlines_abs['cents'][p]}"
                df_tables_lis.loc[
                    j, "description"
                ] = f"The average shortfall from a poverty line of ${lis_povlines_abs['dollars_text'][p]} (averaged across the population in poverty).{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
                df_tables_lis.loc[j, "unit"] = "international-$ in 2017 prices"
                df_tables_lis.loc[j, "shortUnit"] = "$"
                df_tables_lis.loc[j, "type"] = "Numeric"
                df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_povlines_abs[
                    "scale_avg_shortfall"
                ][p]
                df_tables_lis.loc[j, "colorScaleScheme"] = "Purples"
                j += 1

            # Average shortfall (% of poverty line) [this is the income gap ratio]
            for p in range(len(lis_povlines_abs)):
                df_tables_lis.loc[
                    j, "name"
                ] = f"${lis_povlines_abs['dollars_text'][p]} a day - income gap ratio (LIS)"
                df_tables_lis.loc[
                    j, "slug"
                ] = f"income_gap_ratio_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}_{lis_povlines_abs['cents'][p]}"
                df_tables_lis.loc[
                    j, "description"
                ] = f'The average shortfall from a poverty line of ${lis_povlines_abs.dollars_text[p]} a day (averaged across the population in poverty) expressed as a share of the poverty line. This metric is sometimes called the "income gap ratio". It captures the depth of poverty in which those below the poverty line are living.{new_line}This is {lis_welfare.technical_text[wel]}. {lis_welfare.subtitle[wel]}{new_line}Household {lis_welfare.welfare_type[wel]} {lis_equivalence_scales.note[eq]}'
                df_tables_lis.loc[j, "unit"] = "%"
                df_tables_lis.loc[j, "shortUnit"] = "%"
                df_tables_lis.loc[j, "type"] = "Numeric"
                df_tables_lis.loc[
                    j, "colorScaleNumericBins"
                ] = "10;20;30;40;50;60;70;80;90;100"
                df_tables_lis.loc[j, "colorScaleScheme"] = "YlOrRd"
                j += 1

            # Poverty gap index
            for p in range(len(lis_povlines_abs)):
                df_tables_lis.loc[
                    j, "name"
                ] = f"${lis_povlines_abs['dollars_text'][p]} a day - poverty gap index (LIS)"
                df_tables_lis.loc[
                    j, "slug"
                ] = f"poverty_gap_index_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}_{lis_povlines_abs['cents'][p]}"
                df_tables_lis.loc[
                    j, "description"
                ] = f"The poverty gap index calculated at a poverty line of ${lis_povlines_abs['dollars_text'][p]} a day. The poverty gap index is a measure that reflects both the depth and prevalence of poverty. It is defined as the mean shortfall of the total population from the poverty line counting the non-poor as having zero shortfall and expressed as a percentage of the poverty line. It is worth unpacking that definition a little. For those below the poverty line, the shortfall corresponds to the amount of money required in order to reach the poverty line. For those at or above the poverty line, the shortfall is counted as zero. The average shortfall is then calculated across the total population – both poor and non-poor – and then expressed as a share of the poverty line. Unlike the more commonly-used metric of the headcount ratio, the poverty gap index is thus sensitive not only to whether a person’s income falls below the poverty line or not, but also by how much – i.e. to the depth of poverty they experience.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
                df_tables_lis.loc[j, "unit"] = "%"
                df_tables_lis.loc[j, "shortUnit"] = "%"
                df_tables_lis.loc[j, "type"] = "Numeric"
                df_tables_lis.loc[j, "colorScaleNumericBins"] = "10;20;30;40;50;60"
                df_tables_lis.loc[j, "colorScaleScheme"] = "RdPu"
                j += 1

            # Headcount ratio (rel)
            for pct in range(len(lis_povlines_rel)):
                df_tables_lis.loc[
                    j, "name"
                ] = f"{lis_povlines_rel['percent'][pct]} of median {lis_welfare['welfare_type'][wel]} - share of population below poverty line (LIS)"
                df_tables_lis.loc[
                    j, "slug"
                ] = f"headcount_ratio_{lis_povlines_rel['slug_suffix'][pct]}_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
                df_tables_lis.loc[
                    j, "description"
                ] = f"% of population living in households with {lis_welfare['welfare_type'][wel]} below {lis_povlines_rel['percent'][pct]} of the median {lis_welfare['welfare_type'][wel]}.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
                df_tables_lis.loc[j, "unit"] = "%"
                df_tables_lis.loc[j, "shortUnit"] = "%"
                df_tables_lis.loc[j, "type"] = "Numeric"
                df_tables_lis.loc[j, "colorScaleNumericBins"] = "5;10;15;20;25;30"
                df_tables_lis.loc[j, "colorScaleScheme"] = "YlOrBr"
                j += 1

            # Headcount (rel)
            for pct in range(len(lis_povlines_rel)):
                df_tables_lis.loc[
                    j, "name"
                ] = f"{lis_povlines_rel['percent'][pct]} of median {lis_welfare['welfare_type'][wel]} - total number of people below poverty line (LIS)"
                df_tables_lis.loc[
                    j, "slug"
                ] = f"headcount_{lis_povlines_rel['slug_suffix'][pct]}_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
                df_tables_lis.loc[
                    j, "description"
                ] = f"Number of people living in households with {lis_welfare['welfare_type'][wel]} below {lis_povlines_rel['percent'][pct]} of the median {lis_welfare['welfare_type'][wel]}.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
                df_tables_lis.loc[j, "unit"] = np.nan
                df_tables_lis.loc[j, "shortUnit"] = np.nan
                df_tables_lis.loc[j, "type"] = "Numeric"
                df_tables_lis.loc[
                    j, "colorScaleNumericBins"
                ] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000"
                df_tables_lis.loc[j, "colorScaleScheme"] = "YlOrBr"
                j += 1

            # Total shortfall (rel)
            for pct in range(len(lis_povlines_rel)):
                df_tables_lis.loc[
                    j, "name"
                ] = f"{lis_povlines_rel['percent'][pct]} of median {lis_welfare['welfare_type'][wel]} - total shortfall (LIS)"
                df_tables_lis.loc[
                    j, "slug"
                ] = f"total_shortfall_{lis_povlines_rel['slug_suffix'][pct]}_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
                df_tables_lis.loc[
                    j, "description"
                ] = f"The total shortfall from a poverty line of {lis_povlines_rel['text'][pct]} {lis_welfare['welfare_type'][wel]}. This is the amount of money that would be theoretically needed to lift the {lis_welfare['welfare_type'][wel]} of all people in poverty up to the poverty line. However this is not a measure of the actual cost of eliminating poverty, since it does not take into account the costs involved in making the necessary transfers nor any changes in behaviour they would bring about.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
                df_tables_lis.loc[j, "unit"] = np.nan
                df_tables_lis.loc[j, "shortUnit"] = np.nan
                df_tables_lis.loc[j, "type"] = "Numeric"
                df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_povlines_rel[
                    "scale_total_shortfall"
                ][pct]
                df_tables_lis.loc[j, "colorScaleScheme"] = "YlOrBr"
                j += 1

            # Average shortfall ($)
            for pct in range(len(lis_povlines_rel)):
                df_tables_lis.loc[
                    j, "name"
                ] = f"{lis_povlines_rel['percent'][pct]} of median {lis_welfare['welfare_type'][wel]} - average shortfall (LIS)"
                df_tables_lis.loc[
                    j, "slug"
                ] = f"avg_shortfall_{lis_povlines_rel['slug_suffix'][pct]}_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
                df_tables_lis.loc[
                    j, "description"
                ] = f"The average shortfall from a poverty line of of {lis_povlines_rel['text'][pct]} {lis_welfare['welfare_type'][wel]} (averaged across the population in poverty).{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
                df_tables_lis.loc[j, "unit"] = "international-$ in 2017 prices"
                df_tables_lis.loc[j, "shortUnit"] = "$"
                df_tables_lis.loc[j, "type"] = "Numeric"
                df_tables_lis.loc[
                    j, "colorScaleNumericBins"
                ] = "1000;2000;3000;4000;5000"
                df_tables_lis.loc[j, "colorScaleScheme"] = "YlOrBr"
                j += 1

            # Average shortfall (% of poverty line) [this is the income gap ratio]
            for pct in range(len(lis_povlines_rel)):
                df_tables_lis.loc[
                    j, "name"
                ] = f"{lis_povlines_rel['percent'][pct]} of median {lis_welfare['welfare_type'][wel]} - income gap ratio (LIS)"
                df_tables_lis.loc[
                    j, "slug"
                ] = f"income_gap_ratio_{lis_povlines_rel['slug_suffix'][pct]}_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
                df_tables_lis.loc[
                    j, "description"
                ] = f'The average shortfall from a poverty line of of {lis_povlines_rel.text[pct]} {lis_welfare.welfare_type[wel]} (averaged across the population in poverty) expressed as a share of the poverty line. This metric is sometimes called the "income gap ratio". It captures the depth of poverty in which those below the poverty line are living.{new_line}This is {lis_welfare.technical_text[wel]}. {lis_welfare.subtitle[wel]}{new_line}Household {lis_welfare.welfare_type[wel]} {lis_equivalence_scales.note[eq]}'
                df_tables_lis.loc[j, "unit"] = "%"
                df_tables_lis.loc[j, "shortUnit"] = "%"
                df_tables_lis.loc[j, "type"] = "Numeric"
                df_tables_lis.loc[j, "colorScaleNumericBins"] = "5;10;15;20;25;30;35;40"
                df_tables_lis.loc[j, "colorScaleScheme"] = "YlOrBr"
                j += 1

            # Poverty gap index
            for pct in range(len(lis_povlines_rel)):
                df_tables_lis.loc[
                    j, "name"
                ] = f"{lis_povlines_rel['percent'][pct]} of median {lis_welfare['welfare_type'][wel]} - poverty gap index (LIS)"
                df_tables_lis.loc[
                    j, "slug"
                ] = f"poverty_gap_index_{lis_povlines_rel['slug_suffix'][pct]}_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
                df_tables_lis.loc[
                    j, "description"
                ] = f"The poverty gap index calculated at a poverty line of {lis_povlines_rel['text'][pct]} {lis_welfare['welfare_type'][wel]}. The poverty gap index is a measure that reflects both the depth and prevalence of poverty. It is defined as the mean shortfall of the total population from the poverty line counting the non-poor as having zero shortfall and expressed as a percentage of the poverty line. It is worth unpacking that definition a little. For those below the poverty line, the shortfall corresponds to the amount of money required in order to reach the poverty line. For those at or above the poverty line, the shortfall is counted as zero. The average shortfall is then calculated across the total population – both poor and non-poor – and then expressed as a share of the poverty line. Unlike the more commonly-used metric of the headcount ratio, the poverty gap index is thus sensitive not only to whether a person’s income falls below the poverty line or not, but also by how much – i.e. to the depth of poverty they experience.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
                df_tables_lis.loc[j, "unit"] = "%"
                df_tables_lis.loc[j, "shortUnit"] = "%"
                df_tables_lis.loc[j, "type"] = "Numeric"
                df_tables_lis.loc[j, "colorScaleNumericBins"] = "2;4;6;8;10;12"
                df_tables_lis.loc[j, "colorScaleScheme"] = "YlOrBr"
                j += 1

    df_tables_lis["tableSlug"] = merged_tables["name"][tab]

df_tables_lis["sourceName"] = sourceName
df_tables_lis["dataPublishedBy"] = dataPublishedBy
df_tables_lis["sourceLink"] = sourceLink
df_tables_lis["colorScaleNumericMinValue"] = colorScaleNumericMinValue
df_tables_lis["tolerance"] = tolerance
df_tables_lis["colorScaleEqualSizeBins"] = colorScaleEqualSizeBins

# Concatenate all the tables into one
df_tables = pd.concat([df_tables_pip, df_tables_lis], ignore_index=True)
# Make tolerance integer (to not break the parameter in the platform)
df_tables["tolerance"] = df_tables["tolerance"].astype("Int64")

# %% [markdown]
# ### Grapher views
# Similar to the tables, this creates the grapher views by grouping by types of variables and then running by welfare type.

# %%
# Grapher table generation

yAxisMin = 0
mapTargetTime = 2019
selectedFacetStrategy = "entity"
hasMapTab = "false"
tab_parameter = "chart"

df_graphers = pd.DataFrame()

j = 0

for tab in range(len(merged_tables)):
    for view in range(len(source_checkbox)):
        # Gini coefficient
        df_graphers.loc[
            j, "title"
        ] = f"Income inequality: Gini coefficient ({source_checkbox['type_title'][view]})"
        df_graphers.loc[j, "ySlugs"] = source_checkbox["gini"][view]
        df_graphers.loc[j, "Income type Dropdown"] = source_checkbox["type_title"][
            view
        ].capitalize()
        df_graphers.loc[j, "Metric Dropdown"] = "Gini coefficient"
        df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][view]
        df_graphers.loc[j, "World Inequality Database Checkbox"] = source_checkbox[
            "wid"
        ][view]
        df_graphers.loc[j, "Luxembourg Income Study Checkbox"] = source_checkbox["lis"][
            view
        ]
        df_graphers.loc[
            j, "subtitle"
        ] = f"The Gini coefficient is a measure of the inequality of the income distribution in a population. Higher values indicate a higher level of inequality."
        df_graphers.loc[j, "note"] = ""
        df_graphers.loc[j, "type"] = np.nan
        j += 1

    for view in range(len(source_checkbox)):
        # Share of the top 10%
        df_graphers.loc[
            j, "title"
        ] = f"Income share of the top 10% ({source_checkbox['type_title'][view]})"
        df_graphers.loc[j, "ySlugs"] = source_checkbox["top10"][view]
        df_graphers.loc[j, "Income type Dropdown"] = source_checkbox["type_title"][
            view
        ].capitalize()
        df_graphers.loc[j, "Metric Dropdown"] = "Top 10% share"
        df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][view]
        df_graphers.loc[j, "World Inequality Database Checkbox"] = source_checkbox[
            "wid"
        ][view]
        df_graphers.loc[j, "Luxembourg Income Study Checkbox"] = source_checkbox["lis"][
            view
        ]
        df_graphers.loc[
            j, "subtitle"
        ] = f"This is the income of the richest 10% as a share of total income."
        df_graphers.loc[j, "note"] = ""
        df_graphers.loc[j, "type"] = np.nan
        j += 1

    for view in range(len(source_checkbox)):
        # Share of the bottom 50%
        df_graphers.loc[
            j, "title"
        ] = f"Income share of the bottom 50% ({source_checkbox['type_title'][view]})"
        df_graphers.loc[j, "ySlugs"] = source_checkbox["bottom50"][view]
        df_graphers.loc[j, "Income type Dropdown"] = source_checkbox["type_title"][
            view
        ].capitalize()
        df_graphers.loc[j, "Metric Dropdown"] = "Bottom 50% share"
        df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][view]
        df_graphers.loc[j, "World Inequality Database Checkbox"] = source_checkbox[
            "wid"
        ][view]
        df_graphers.loc[j, "Luxembourg Income Study Checkbox"] = source_checkbox["lis"][
            view
        ]
        df_graphers.loc[
            j, "subtitle"
        ] = f"This is the income of the poorest 50% as a share of total income."
        df_graphers.loc[j, "note"] = ""
        j += 1

    for view in range(len(source_checkbox)):
        # P90/P10
        df_graphers.loc[
            j, "title"
        ] = f"Income inequality: P90/P10 ratio ({source_checkbox['type_title'][view]})"
        df_graphers.loc[j, "ySlugs"] = source_checkbox["p90_p10"][view]
        df_graphers.loc[j, "Income type Dropdown"] = source_checkbox["type_title"][
            view
        ].capitalize()
        df_graphers.loc[j, "Metric Dropdown"] = "P90/P10"
        df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][view]
        df_graphers.loc[j, "World Inequality Database Checkbox"] = source_checkbox[
            "wid"
        ][view]
        df_graphers.loc[j, "Luxembourg Income Study Checkbox"] = source_checkbox["lis"][
            view
        ]
        df_graphers.loc[
            j, "subtitle"
        ] = f"P90 and P10 are the levels of income below which 90% and 10% of the population live, respectively. This variable gives the ratio of the two. It is a measure of inequality that indicates the gap between the richest and poorest tenth of the population."
        df_graphers.loc[j, "note"] = ""
        df_graphers.loc[j, "type"] = np.nan
        j += 1

    for view in range(len(source_checkbox)):
        # P90/P50
        df_graphers.loc[
            j, "title"
        ] = f"Income inequality: P90/P50 ratio ({source_checkbox['type_title'][view]})"
        df_graphers.loc[j, "ySlugs"] = source_checkbox["p90_p50"][view]
        df_graphers.loc[j, "Income type Dropdown"] = source_checkbox["type_title"][
            view
        ].capitalize()
        df_graphers.loc[j, "Metric Dropdown"] = "P90/P50"
        df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][view]
        df_graphers.loc[j, "World Inequality Database Checkbox"] = source_checkbox[
            "wid"
        ][view]
        df_graphers.loc[j, "Luxembourg Income Study Checkbox"] = source_checkbox["lis"][
            view
        ]
        df_graphers.loc[
            j, "subtitle"
        ] = f"The P90/P50 ratio measures the degree of inequality within the richest half of the population. A ratio of 2 means that someone just falling in the richest tenth of the population has twice the median income."
        df_graphers.loc[j, "note"] = ""
        df_graphers.loc[j, "type"] = np.nan
        j += 1

    for view in range(len(source_checkbox)):
        # P50/P10
        df_graphers.loc[
            j, "title"
        ] = f"Income inequality: P50/P10 ratio ({source_checkbox['type_title'][view]})"
        df_graphers.loc[j, "ySlugs"] = source_checkbox["p50_p10"][view]
        df_graphers.loc[j, "Income type Dropdown"] = source_checkbox["type_title"][
            view
        ].capitalize()
        df_graphers.loc[j, "Metric Dropdown"] = "P50/P10"
        df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][view]
        df_graphers.loc[j, "World Inequality Database Checkbox"] = source_checkbox[
            "wid"
        ][view]
        df_graphers.loc[j, "Luxembourg Income Study Checkbox"] = source_checkbox["lis"][
            view
        ]
        df_graphers.loc[
            j, "subtitle"
        ] = f"The P50/P10 ratio measures the degree of inequality within the poorest half of the population. A ratio of 2 means that the median income is two times higher than that of someone just falling in the poorest tenth of the population."
        df_graphers.loc[j, "note"] = ""
        df_graphers.loc[j, "type"] = np.nan
        j += 1

    for view in range(len(source_checkbox)):
        # Palma ratio
        df_graphers.loc[
            j, "title"
        ] = f"Income inequality: Palma ratio ({source_checkbox['type_title'][view]})"
        df_graphers.loc[j, "ySlugs"] = source_checkbox["palma"][view]
        df_graphers.loc[j, "Income type Dropdown"] = source_checkbox["type_title"][
            view
        ].capitalize()
        df_graphers.loc[j, "Metric Dropdown"] = "Palma ratio"
        df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][view]
        df_graphers.loc[j, "World Inequality Database Checkbox"] = source_checkbox[
            "wid"
        ][view]
        df_graphers.loc[j, "Luxembourg Income Study Checkbox"] = source_checkbox["lis"][
            view
        ]
        df_graphers.loc[
            j, "subtitle"
        ] = f"The Palma ratio is the share of total income of the top 10% divided by the share of the bottom 40%."
        df_graphers.loc[j, "note"] = ""
        df_graphers.loc[j, "type"] = np.nan
        j += 1

    for view in range(len(source_checkbox)):
        # Headcount ratio (rel)
        df_graphers.loc[
            j, "title"
        ] = f"Relative poverty: Share of people below 50% of the median income ({source_checkbox['type_title'][view]})"
        df_graphers.loc[j, "ySlugs"] = source_checkbox["relative"][view]
        df_graphers.loc[j, "Income type Dropdown"] = source_checkbox["type_title"][
            view
        ].capitalize()
        df_graphers.loc[
            j, "Metric Dropdown"
        ] = f"Share in relative poverty (< 50% of the median)"
        df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][view]
        df_graphers.loc[j, "World Inequality Database Checkbox"] = source_checkbox[
            "wid"
        ][view]
        df_graphers.loc[j, "Luxembourg Income Study Checkbox"] = source_checkbox["lis"][
            view
        ]
        df_graphers.loc[
            j, "subtitle"
        ] = f"Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at 50% of the median income."
        df_graphers.loc[j, "note"] = ""
        df_graphers.loc[j, "type"] = np.nan
        j += 1

    df_graphers["tableSlug"] = merged_tables["name"][tab]

# Add yAxisMin and mapTargetTime
df_graphers["yAxisMin"] = yAxisMin
df_graphers["mapTargetTime"] = mapTargetTime
df_graphers["selectedFacetStrategy"] = selectedFacetStrategy
df_graphers["hasMapTab"] = hasMapTab
df_graphers["tab"] = tab_parameter

# Drop rows with empty ySlugs (they make the checkbox system fail)
df_graphers = df_graphers[df_graphers["ySlugs"] != ""].reset_index(drop=True)

# %% [markdown]
# Final adjustments to the graphers table: add `relatedQuestion` link and `defaultView`:

# %%
# Add related question link
df_graphers["relatedQuestionText"] = np.nan
df_graphers["relatedQuestionUrl"] = np.nan

# Make mapTargetTime integer (to not break the parameter in the platform)
df_graphers["mapTargetTime"] = df_graphers["mapTargetTime"].astype("Int64")

# Select one default view
df_graphers.loc[
    (df_graphers["Income type Dropdown"] == "After tax")
    & (df_graphers["Metric Dropdown"] == "Gini coefficient")
    & (df_graphers["World Bank PIP Checkbox"] == "true")
    & (df_graphers["World Inequality Database Checkbox"] == "true")
    & (df_graphers["Luxembourg Income Study Checkbox"] == "true"),
    ["defaultView"],
] = "true"


# %% [markdown]
# ## Explorer generation
# Here, the header, tables and graphers dataframes are combined to be shown in for format required for OWID data explorers.

# %%
# Define list of variables to iterate: table names (from table dataframe)
table_list = list(df_tables["tableSlug"].unique())

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

    for tab in table_list:
        table_tsv = (
            df_tables[df_tables["tableSlug"] == tab].copy().reset_index(drop=True)
        )
        table_tsv = table_tsv.drop(columns=["tableSlug"])
        table_tsv = table_tsv.to_csv(sep="\t", index=False)
        table_tsv_indented = textwrap.indent(table_tsv, "\t")
        f.write(
            "\ntable\t"
            + merged_tables.loc[merged_tables["name"] == tab, "link"].item()
            + "\t"
            + tab
        )
        f.write("\ncolumns\t" + tab + "\n\n" + table_tsv_indented)
