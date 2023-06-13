# %% [markdown]
# # Inequality Data Explorer - Source Comparison
# This code creates the tsv file for the inequality comparison explorer, available [here](https://owid.cloud/admin/explorers/preview/inequality-comparison)

import textwrap
from pathlib import Path

import numpy as np

# %%
import pandas as pd

PARENT_DIR = Path(__file__).parent.parent.parent.parent.absolute()
outfile = PARENT_DIR / "explorers" / "inequality-comparison.explorer.tsv"

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

# Only get the combinations where all the sources are available (pre and post tax)
source_checkbox = source_checkbox[
    (
        (source_checkbox["type"] == "pre")
        & (source_checkbox["wid"] == "true")
        & (source_checkbox["pip"] == "false")
        & (source_checkbox["lis"] == "true")
    )
    | (
        (source_checkbox["type"] == "post")
        & (source_checkbox["wid"] == "true")
        & (source_checkbox["pip"] == "true")
        & (source_checkbox["lis"] == "true")
    )
].reset_index(drop=True)

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

# Relative poverty sheet
sheet_name = "povlines_rel"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
lis_povlines_rel = pd.read_csv(url)

# WORLD INEQUALITY DATABASE
# Read Google sheets
sheet_id = "18T5IGnpyJwb8KL9USYvME6IaLEcYIo26ioHCpkDnwRQ"

# Welfare type sheet
sheet_name = "welfare"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
wid_welfare = pd.read_csv(url, keep_default_na=False)

# WORLD BANK POVERTY AND INEQUALITY PLATFORM
# Read Google sheets
sheet_id = "17KJ9YcvfdmO_7-Sv2Ij0vmzAQI6rXSIqHfJtgFHN-a8"

# Survey type sheet
sheet_name = "table"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
pip_tables = pd.read_csv(url)

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
    "explorerTitle": "Inequality Data Explorer - Source comparison",
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
    "pickerColumnSlugs": "gini decile10_share palma_ratio headcount_ratio_50_median p0p100_gini_posttax_nat p90p100_share_posttax_nat palma_ratio_posttax_nat gini_dhi_pc share_p100_dhi_pc palma_ratio_dhi_pc headcount_ratio_50_median_dhi_pc",
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
sourceName = "World Bank Poverty and Inequality Platform (2022)"
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

    # Gini coefficient
    df_tables_pip.loc[j, "name"] = f"Gini coefficient (PIP data)"
    df_tables_pip.loc[j, "slug"] = f"gini"
    df_tables_pip.loc[
        j, "description"
    ] = f"The Gini coefficient measures inequality on a scale between 0 and 1, where higher values indicate greater inequality."
    df_tables_pip.loc[j, "unit"] = np.nan
    df_tables_pip.loc[j, "shortUnit"] = np.nan
    df_tables_pip.loc[j, "type"] = "Numeric"
    df_tables_pip.loc[
        j, "colorScaleNumericBins"
    ] = "0.25;0.3;0.35;0.4;0.45;0.5;0.55;0.6"
    df_tables_pip.loc[j, "colorScaleScheme"] = "Oranges"
    j += 1

    # Share of the top 10%
    df_tables_pip.loc[
        j, "name"
    ] = f"{pip_tables.text[tab].capitalize()} share of the richest 10% (PIP data)"
    df_tables_pip.loc[j, "slug"] = f"decile10_share"
    df_tables_pip.loc[
        j, "description"
    ] = f"The {pip_tables.text[tab]} of the richest decile (tenth of the population) as a share of total {pip_tables.text[tab]}."
    df_tables_pip.loc[j, "unit"] = "%"
    df_tables_pip.loc[j, "shortUnit"] = "%"
    df_tables_pip.loc[j, "type"] = "Numeric"
    df_tables_pip.loc[j, "colorScaleNumericBins"] = "20;25;30;35;40;45;50"
    df_tables_pip.loc[j, "colorScaleScheme"] = "Reds"
    j += 1

    # Share of the bottom 50%
    df_tables_pip.loc[
        j, "name"
    ] = f"{pip_tables.text[tab].capitalize()} share of the poorest 50% (PIP data)"
    df_tables_pip.loc[j, "slug"] = f"bottom50_share"
    df_tables_pip.loc[
        j, "description"
    ] = f"The {pip_tables.text[tab]} of the poorest 50% as a share of total {pip_tables.text[tab]}."
    df_tables_pip.loc[j, "unit"] = "%"
    df_tables_pip.loc[j, "shortUnit"] = "%"
    df_tables_pip.loc[j, "type"] = "Numeric"
    df_tables_pip.loc[j, "colorScaleNumericBins"] = "10;15;20;25;30;35"
    df_tables_pip.loc[j, "colorScaleScheme"] = "Blues"
    j += 1

    # # P90/P10
    # df_tables_pip.loc[j, "name"] = f"P90/P10 ratio (PIP data)"
    # df_tables_pip.loc[j, "slug"] = f"p90_p10_ratio"
    # df_tables_pip.loc[
    #     j, "description"
    # ] = f"P90 is the the level of {pip_tables.text[tab]} below which 90% of the population lives. P10 is the level of {pip_tables.text[tab]} below which 10% of the population lives. This variable gives the ratio of the two. It is a measure of inequality that indicates the gap between the richest and poorest tenth of the population. It tells you how many times richer someone just in the the poorest tenth would need to be in order to be counted in the richest tenth."
    # df_tables_pip.loc[j, "unit"] = np.nan
    # df_tables_pip.loc[j, "shortUnit"] = np.nan
    # df_tables_pip.loc[j, "type"] = "Numeric"
    # df_tables_pip.loc[j, "colorScaleNumericBins"] = "0;2;4;6;8;10;12;14;16;18"
    # df_tables_pip.loc[j, "colorScaleScheme"] = "OrRd"
    # j += 1

    # # P90/P50
    # df_tables_pip.loc[j, "name"] = f"P90/P50 ratio (PIP data)"
    # df_tables_pip.loc[j, "slug"] = f"p90_p50_ratio"
    # df_tables_pip.loc[
    #     j, "description"
    # ] = f"P90 is the the level of {pip_tables.text[tab]} above which 10% of the population lives. P50 is the median – the level of {pip_tables.text[tab]} below which 50% of the population lives. This variable gives the ratio of the two. It is a measure of inequality within the top half of the distribution. It tells you how many times richer someone in the middle of the distribution would need to be in order to be counted in the richest tenth."
    # df_tables_pip.loc[j, "unit"] = np.nan
    # df_tables_pip.loc[j, "shortUnit"] = np.nan
    # df_tables_pip.loc[j, "type"] = "Numeric"
    # df_tables_pip.loc[j, "colorScaleNumericBins"] = "0;1;2;3;4;5"
    # df_tables_pip.loc[j, "colorScaleScheme"] = "Purples"
    # j += 1

    # # P50/P10
    # df_tables_pip.loc[j, "name"] = f"P50/P10 ratio (PIP data)"
    # df_tables_pip.loc[j, "slug"] = f"p50_p10_ratio"
    # df_tables_pip.loc[
    #     j, "description"
    # ] = f"P50 is the median – the level of {pip_tables.text[tab]} below which 50% of the population lives. P10 is the the level of {pip_tables.text[tab]} below which 10% of the population lives. This variable gives the ratio of the two. It is a measure of inequality within the bottom half of the distribution. It tells you how many times richer someone just in the the poorest tenth would need to be in order to be reach the median."
    # df_tables_pip.loc[j, "unit"] = np.nan
    # df_tables_pip.loc[j, "shortUnit"] = np.nan
    # df_tables_pip.loc[j, "type"] = "Numeric"
    # df_tables_pip.loc[j, "colorScaleNumericBins"] = "0;0.5;1;1.5;2;2.5;3;3.5;4"
    # df_tables_pip.loc[j, "colorScaleScheme"] = "YlOrRd"
    # j += 1

    # Palma ratio
    df_tables_pip.loc[j, "name"] = f"Palma ratio (PIP data)"
    df_tables_pip.loc[j, "slug"] = f"palma_ratio"
    df_tables_pip.loc[
        j, "description"
    ] = f"The Palma ratio is a measure of inequality: it is the share of total {pip_tables.text[tab]} of the top 10% divided by the share of the bottom 40%."
    df_tables_pip.loc[j, "unit"] = np.nan
    df_tables_pip.loc[j, "shortUnit"] = np.nan
    df_tables_pip.loc[j, "type"] = "Numeric"
    df_tables_pip.loc[j, "colorScaleNumericBins"] = "0.5;1;1.5;2;2.5;3;3.5;4;4.5;5;5.5"
    df_tables_pip.loc[j, "colorScaleScheme"] = "YlOrBr"
    j += 1

    # Headcount ratio (rel)
    df_tables_pip.loc[j, "name"] = f"Share in relative poverty (PIP data)"
    df_tables_pip.loc[j, "slug"] = f"headcount_ratio_50_median"
    df_tables_pip.loc[
        j, "description"
    ] = f"% of population living in households with an {pip_tables.text[tab]} per person below 50% of the median."
    df_tables_pip.loc[j, "unit"] = "%"
    df_tables_pip.loc[j, "shortUnit"] = "%"
    df_tables_pip.loc[j, "type"] = "Numeric"
    df_tables_pip.loc[j, "colorScaleNumericBins"] = "5;10;15;20;25;30"
    df_tables_pip.loc[j, "colorScaleScheme"] = "YlOrBr"
    j += 1

df_tables_pip["tableSlug"] = tableSlug
df_tables_pip["sourceName"] = sourceName
df_tables_pip["dataPublishedBy"] = dataPublishedBy
df_tables_pip["sourceLink"] = sourceLink
df_tables_pip["colorScaleNumericMinValue"] = colorScaleNumericMinValue
df_tables_pip["tolerance"] = tolerance
df_tables_pip["colorScaleEqualSizeBins"] = colorScaleEqualSizeBins

###########################################################################################
# WORLD INEQUALITY DATABASE (WID)
###########################################################################################

# Table generation

sourceName = "World Inequality Database (WID.world) (2023)"
dataPublishedBy = "World Inequality Database (WID), https://wid.world"
sourceLink = "https://wid.world"
colorScaleNumericMinValue = 0
tolerance = 5
colorScaleEqualSizeBins = "true"
new_line = "<br><br>"

df_tables_wid = pd.DataFrame()
j = 0

for tab in range(len(merged_tables)):
    for wel in range(len(wid_welfare)):
        # Gini coefficient
        df_tables_wid.loc[j, "name"] = f"Gini coefficient (WID data)"
        df_tables_wid.loc[j, "slug"] = f"p0p100_gini_{wid_welfare['slug'][wel]}"
        df_tables_wid.loc[
            j, "description"
        ] = f"The Gini coefficient is a measure of the inequality of the {wid_welfare['welfare_type'][wel]} distribution in a population. Higher values indicate a higher level of inequality.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
        df_tables_wid.loc[j, "unit"] = np.nan
        df_tables_wid.loc[j, "shortUnit"] = np.nan
        df_tables_wid.loc[j, "type"] = "Numeric"
        df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare["scale_gini"][wel]
        df_tables_wid.loc[j, "colorScaleScheme"] = "Oranges"
        j += 1

        # Share of the top 10%
        df_tables_wid.loc[
            j, "name"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} share of the richest 10% (WID data)"
        df_tables_wid.loc[j, "slug"] = f"p90p100_share_{wid_welfare['slug'][wel]}"
        df_tables_wid.loc[
            j, "description"
        ] = f"This is the {wid_welfare['welfare_type'][wel]} of the richest 10% as a share of total {wid_welfare['welfare_type'][wel]}.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
        df_tables_wid.loc[j, "unit"] = "%"
        df_tables_wid.loc[j, "shortUnit"] = "%"
        df_tables_wid.loc[j, "type"] = "Numeric"
        df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare["scale_top10"][wel]
        df_tables_wid.loc[j, "colorScaleScheme"] = "Reds"
        j += 1

        # Share of the bottom 50%
        df_tables_wid.loc[
            j, "name"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} share of the poorest 50% (WID data)"
        df_tables_wid.loc[j, "slug"] = f"p0p50_share_{wid_welfare['slug'][wel]}"
        df_tables_wid.loc[
            j, "description"
        ] = f"This is the {wid_welfare['welfare_type'][wel]} of the poorest 50% as a share of total {wid_welfare['welfare_type'][wel]}.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
        df_tables_wid.loc[j, "unit"] = "%"
        df_tables_wid.loc[j, "shortUnit"] = "%"
        df_tables_wid.loc[j, "type"] = "Numeric"
        df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare["scale_bottom50"][
            wel
        ]
        df_tables_wid.loc[j, "colorScaleScheme"] = "Blues"
        j += 1

        # # P90/P10
        # df_tables_wid.loc[j, "name"] = f"P90/P10 ratio (WID data)"
        # df_tables_wid.loc[j, "slug"] = f"p90_p10_ratio_{wid_welfare['slug'][wel]}"
        # df_tables_wid.loc[
        #     j, "description"
        # ] = f"P90 is the the level of {wid_welfare['welfare_type'][wel]} below which 90% of the population lives. P10 is the level of {wid_welfare['welfare_type'][wel]} below which 10% of the population lives. This variable gives the ratio of the two. It is a measure of inequality that indicates the gap between the richest and poorest tenth of the population. It tells you how many times richer someone just in the the poorest tenth would need to be in order to be counted in the richest tenth.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
        # df_tables_wid.loc[j, "unit"] = np.nan
        # df_tables_wid.loc[j, "shortUnit"] = np.nan
        # df_tables_wid.loc[j, "type"] = "Numeric"
        # df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare[
        #     "scale_p90_p10_ratio"
        # ][wel]
        # df_tables_wid.loc[j, "colorScaleScheme"] = "OrRd"
        # j += 1

        # # P90/P50
        # df_tables_wid.loc[j, "name"] = f"P90/P50 ratio (WID data)"
        # df_tables_wid.loc[j, "slug"] = f"p90_p50_ratio_{wid_welfare['slug'][wel]}"
        # df_tables_wid.loc[
        #     j, "description"
        # ] = f"P90 is the the level of {wid_welfare['welfare_type'][wel]} above which 10% of the population lives. P50 is the median – the level of {wid_welfare['welfare_type'][wel]} below which 50% of the population lives. This variable gives the ratio of the two. It is a measure of inequality within the top half of the distribution. It tells you how many times richer someone in the middle of the distribution would need to be in order to be counted in the richest tenth.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
        # df_tables_wid.loc[j, "unit"] = np.nan
        # df_tables_wid.loc[j, "shortUnit"] = np.nan
        # df_tables_wid.loc[j, "type"] = "Numeric"
        # df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare[
        #     "scale_p90_p50_ratio"
        # ][wel]
        # df_tables_wid.loc[j, "colorScaleScheme"] = "Purples"
        # j += 1

        # # P50/P10
        # df_tables_wid.loc[j, "name"] = f"P50/P10 ratio (WID data)"
        # df_tables_wid.loc[j, "slug"] = f"p50_p10_ratio_{wid_welfare['slug'][wel]}"
        # df_tables_wid.loc[
        #     j, "description"
        # ] = f"P50 is the median – the level of {wid_welfare['welfare_type'][wel]} below which 50% of the population lives. P10 is the the level of {wid_welfare['welfare_type'][wel]} below which 10% of the population lives. This variable gives the ratio of the two. It is a measure of inequality within the bottom half of the distribution. It tells you how many times richer someone just in the the poorest tenth would need to be in order to be reach the median.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
        # df_tables_wid.loc[j, "unit"] = np.nan
        # df_tables_wid.loc[j, "shortUnit"] = np.nan
        # df_tables_wid.loc[j, "type"] = "Numeric"
        # df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare[
        #     "scale_p50_p10_ratio"
        # ][wel]
        # df_tables_wid.loc[j, "colorScaleScheme"] = "YlOrRd"
        # j += 1

        # Palma ratio
        df_tables_wid.loc[j, "name"] = f"Palma ratio (WID data)"
        df_tables_wid.loc[j, "slug"] = f"palma_ratio_{wid_welfare['slug'][wel]}"
        df_tables_wid.loc[
            j, "description"
        ] = f"The Palma ratio is a measure of inequality: it is the share of total {wid_welfare['welfare_type'][wel]} of the top 10% divided by the share of the bottom 40%.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
        df_tables_wid.loc[j, "unit"] = np.nan
        df_tables_wid.loc[j, "shortUnit"] = np.nan
        df_tables_wid.loc[j, "type"] = "Numeric"
        df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare[
            "scale_palma_ratio"
        ][wel]
        df_tables_wid.loc[j, "colorScaleScheme"] = "YlOrBr"
        j += 1

    df_tables_wid["tableSlug"] = merged_tables["name"][tab]

df_tables_wid["sourceName"] = sourceName
df_tables_wid["dataPublishedBy"] = dataPublishedBy
df_tables_wid["sourceLink"] = sourceLink
df_tables_wid["colorScaleNumericMinValue"] = colorScaleNumericMinValue
df_tables_wid["tolerance"] = tolerance
df_tables_wid["colorScaleEqualSizeBins"] = colorScaleEqualSizeBins

###########################################################################################
# LUXEMBOURG INCOME STUDY (LIS)
###########################################################################################
sourceName = "Luxembourg Income Study (2023)"
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
            # Gini coefficient
            df_tables_lis.loc[j, "name"] = f"Gini coefficient (LIS data)"
            df_tables_lis.loc[
                j, "slug"
            ] = f"gini_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_tables_lis.loc[
                j, "description"
            ] = f"The Gini coefficient is a measure of the inequality of the {lis_welfare['welfare_type'][wel]} distribution in a population. Higher values indicate a higher level of inequality.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}{lis_equivalence_scales['description'][eq]}"
            df_tables_lis.loc[j, "unit"] = np.nan
            df_tables_lis.loc[j, "shortUnit"] = np.nan
            df_tables_lis.loc[j, "type"] = "Numeric"
            df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_welfare["scale_gini"][
                wel
            ]
            df_tables_lis.loc[j, "colorScaleScheme"] = "Oranges"
            df_tables_lis.loc[j, "equivalized"] = lis_equivalence_scales["text"][eq]
            j += 1

            # Share of the top 10%
            df_tables_lis.loc[
                j, "name"
            ] = f"{lis_welfare['welfare_type'][wel].capitalize()} share of the richest 10% (LIS data)"
            df_tables_lis.loc[
                j, "slug"
            ] = f"share_p90_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_tables_lis.loc[
                j, "description"
            ] = f"This is the {lis_welfare['welfare_type'][wel]} of the richest 10% as a share of total {lis_welfare['welfare_type'][wel]}.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}{lis_equivalence_scales['description'][eq]}"
            df_tables_lis.loc[j, "unit"] = "%"
            df_tables_lis.loc[j, "shortUnit"] = "%"
            df_tables_lis.loc[j, "type"] = "Numeric"
            df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_welfare["scale_top10"][
                wel
            ]
            df_tables_lis.loc[j, "colorScaleScheme"] = "Reds"
            df_tables_lis.loc[j, "equivalized"] = lis_equivalence_scales["text"][eq]
            j += 1

            # Share of the bottom 50%
            df_tables_lis.loc[
                j, "name"
            ] = f"{lis_welfare['welfare_type'][wel].capitalize()} share of the poorest 50% (LIS data)"
            df_tables_lis.loc[
                j, "slug"
            ] = f"share_bottom50_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_tables_lis.loc[
                j, "description"
            ] = f"This is the {lis_welfare['welfare_type'][wel]} of the poorest 50% as a share of total {lis_welfare['welfare_type'][wel]}.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}{lis_equivalence_scales['description'][eq]}"
            df_tables_lis.loc[j, "unit"] = "%"
            df_tables_lis.loc[j, "shortUnit"] = "%"
            df_tables_lis.loc[j, "type"] = "Numeric"
            df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_welfare[
                "scale_bottom50"
            ][wel]
            df_tables_lis.loc[j, "colorScaleScheme"] = "Blues"
            df_tables_lis.loc[j, "equivalized"] = lis_equivalence_scales["text"][eq]
            j += 1

            # # P90/P10
            # df_tables_lis.loc[j, "name"] = f"P90/P10 ratio (LIS data)"
            # df_tables_lis.loc[
            #     j, "slug"
            # ] = f"p90_p10_ratio_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            # df_tables_lis.loc[
            #     j, "description"
            # ] = f"P90 is the the level of {lis_welfare['welfare_type'][wel]} below which 90% of the population lives. P10 is the level of {lis_welfare['welfare_type'][wel]} below which 10% of the population lives. This variable gives the ratio of the two. It is a measure of inequality that indicates the gap between the richest and poorest tenth of the population. It tells you how many times richer someone just in the the poorest tenth would need to be in order to be counted in the richest tenth.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}{lis_equivalence_scales['description'][eq]}"
            # df_tables_lis.loc[j, "unit"] = np.nan
            # df_tables_lis.loc[j, "shortUnit"] = np.nan
            # df_tables_lis.loc[j, "type"] = "Numeric"
            # df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_welfare[
            #     "scale_p90_p10_ratio"
            # ][wel]
            # df_tables_lis.loc[j, "colorScaleScheme"] = "OrRd"
            # df_tables_lis.loc[j, "equivalized"] = lis_equivalence_scales["text"][eq]
            # j += 1

            # # P90/P50
            # df_tables_lis.loc[j, "name"] = f"P90/P50 ratio (LIS data)"
            # df_tables_lis.loc[
            #     j, "slug"
            # ] = f"p90_p50_ratio_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            # df_tables_lis.loc[
            #     j, "description"
            # ] = f"P90 is the the level of {lis_welfare['welfare_type'][wel]} above which 10% of the population lives. P50 is the median – the level of {lis_welfare['welfare_type'][wel]} below which 50% of the population lives. This variable gives the ratio of the two. It is a measure of inequality within the top half of the distribution. It tells you how many times richer someone in the middle of the distribution would need to be in order to be counted in the richest tenth.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}{lis_equivalence_scales['description'][eq]}"
            # df_tables_lis.loc[j, "unit"] = np.nan
            # df_tables_lis.loc[j, "shortUnit"] = np.nan
            # df_tables_lis.loc[j, "type"] = "Numeric"
            # df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_welfare[
            #     "scale_p90_p50_ratio"
            # ][wel]
            # df_tables_lis.loc[j, "colorScaleScheme"] = "Purples"
            # df_tables_lis.loc[j, "equivalized"] = lis_equivalence_scales["text"][eq]
            # j += 1

            # # P50/P10
            # df_tables_lis.loc[j, "name"] = f"P50/P10 ratio (LIS data)"
            # df_tables_lis.loc[
            #     j, "slug"
            # ] = f"p50_p10_ratio_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            # df_tables_lis.loc[
            #     j, "description"
            # ] = f"P50 is the median – the level of {lis_welfare['welfare_type'][wel]} below which 50% of the population lives. P10 is the the level of {lis_welfare['welfare_type'][wel]} below which 10% of the population lives. This variable gives the ratio of the two. It is a measure of inequality within the bottom half of the distribution. It tells you how many times richer someone just in the the poorest tenth would need to be in order to be reach the median.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}{lis_equivalence_scales['description'][eq]}"
            # df_tables_lis.loc[j, "unit"] = np.nan
            # df_tables_lis.loc[j, "shortUnit"] = np.nan
            # df_tables_lis.loc[j, "type"] = "Numeric"
            # df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_welfare[
            #     "scale_p50_p10_ratio"
            # ][wel]
            # df_tables_lis.loc[j, "colorScaleScheme"] = "YlOrRd"
            # df_tables_lis.loc[j, "equivalized"] = lis_equivalence_scales["text"][eq]
            # j += 1

            # Palma ratio
            df_tables_lis.loc[j, "name"] = f"Palma ratio (LIS data)"
            df_tables_lis.loc[
                j, "slug"
            ] = f"palma_ratio_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_tables_lis.loc[
                j, "description"
            ] = f"The Palma ratio is a measure of inequality: it is the share of total {lis_welfare['welfare_type'][wel]} of the top 10% divided by the share of the bottom 40%.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}{lis_equivalence_scales['description'][eq]}"
            df_tables_lis.loc[j, "unit"] = np.nan
            df_tables_lis.loc[j, "shortUnit"] = np.nan
            df_tables_lis.loc[j, "type"] = "Numeric"
            df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_welfare[
                "scale_palma_ratio"
            ][wel]
            df_tables_lis.loc[j, "colorScaleScheme"] = "YlOrBr"
            df_tables_lis.loc[j, "equivalized"] = lis_equivalence_scales["text"][eq]
            j += 1

            # Headcount ratio (rel)
            df_tables_lis.loc[j, "name"] = f"Share in relative poverty (LIS data)"
            df_tables_lis.loc[
                j, "slug"
            ] = f"headcount_ratio_50_median_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
            df_tables_lis.loc[
                j, "description"
            ] = f"% of population living in households with {lis_welfare['welfare_type'][wel]} below 50% of the median {lis_welfare['welfare_type'][wel]}.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}{lis_equivalence_scales['description'][eq]}"
            df_tables_lis.loc[j, "unit"] = "%"
            df_tables_lis.loc[j, "shortUnit"] = "%"
            df_tables_lis.loc[j, "type"] = "Numeric"
            df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_welfare[
                "scale_relative_poverty"
            ][wel]
            df_tables_lis.loc[j, "colorScaleScheme"] = "YlOrBr"
            df_tables_lis.loc[j, "equivalized"] = lis_equivalence_scales["text"][eq]
            j += 1

    df_tables_lis["tableSlug"] = merged_tables["name"][tab]

df_tables_lis["sourceName"] = sourceName
df_tables_lis["dataPublishedBy"] = dataPublishedBy
df_tables_lis["sourceLink"] = sourceLink
df_tables_lis["colorScaleNumericMinValue"] = colorScaleNumericMinValue
df_tables_lis["tolerance"] = tolerance
df_tables_lis["colorScaleEqualSizeBins"] = colorScaleEqualSizeBins

# Remove all the rows that have the "equivalized" value in the equivalized column
df_tables_lis = df_tables_lis[
    df_tables_lis["equivalized"] != "equivalized"
].reset_index(drop=True)
# Drop the equivalized column
df_tables_lis = df_tables_lis.drop(columns=["equivalized"])

# Concatenate all the tables into one
df_tables = pd.concat([df_tables_pip, df_tables_wid, df_tables_lis], ignore_index=True)
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
        ] = f"Gini coefficient ({source_checkbox['type_title'][view]})"
        df_graphers.loc[j, "ySlugs"] = source_checkbox["gini"][view]
        df_graphers.loc[j, "Indicator Dropdown"] = "Gini coefficient"
        df_graphers.loc[j, "Income measure Dropdown"] = source_checkbox["type_title"][
            view
        ].capitalize()
        df_graphers.loc[
            j, "subtitle"
        ] = f"The Gini coefficient is a measure of the inequality of the income distribution in a population. Higher values indicate a higher level of inequality."
        df_graphers.loc[j, "note"] = ""
        df_graphers.loc[j, "type"] = np.nan
        j += 1

        # Share of the top 10%
        df_graphers.loc[
            j, "title"
        ] = f"Income share of the richest 10% ({source_checkbox['type_title'][view]})"
        df_graphers.loc[j, "ySlugs"] = source_checkbox["top10"][view]
        df_graphers.loc[j, "Indicator Dropdown"] = "Share of the richest 10%"
        df_graphers.loc[j, "Income measure Dropdown"] = source_checkbox["type_title"][
            view
        ].capitalize()
        df_graphers.loc[
            j, "subtitle"
        ] = f"The share of income received by the richest 10% of the population."
        df_graphers.loc[j, "note"] = ""
        df_graphers.loc[j, "type"] = np.nan
        j += 1

        # Share of the bottom 50%
        df_graphers.loc[
            j, "title"
        ] = f"Income share of the poorest 50% ({source_checkbox['type_title'][view]})"
        df_graphers.loc[j, "ySlugs"] = source_checkbox["bottom50"][view]
        df_graphers.loc[j, "Indicator Dropdown"] = "Share of the poorest 50%"
        df_graphers.loc[j, "Income measure Dropdown"] = source_checkbox["type_title"][
            view
        ].capitalize()
        df_graphers.loc[
            j, "subtitle"
        ] = f"The share of income received by the poorest 50% of the population."
        df_graphers.loc[j, "note"] = ""
        j += 1

        # # P90/P10
        # df_graphers.loc[
        #     j, "title"
        # ] = f"Income inequality: P90/P10 ratio ({source_checkbox['type_title'][view]})"
        # df_graphers.loc[j, "ySlugs"] = source_checkbox["p90_p10"][view]
        # df_graphers.loc[j, "Indicator Dropdown"] = "P90/P10"
        # df_graphers.loc[j, "Income measure Dropdown"] = source_checkbox["type_title"][
        #     view
        # ].capitalize()
        # df_graphers.loc[
        #     j, "subtitle"
        # ] = f"P90 and P10 are the levels of income below which 90% and 10% of the population live, respectively. This variable gives the ratio of the two. It is a measure of inequality that indicates the gap between the richest and poorest tenth of the population."
        # df_graphers.loc[j, "note"] = ""
        # df_graphers.loc[j, "type"] = np.nan
        # j += 1

        # # P90/P50
        # df_graphers.loc[
        #     j, "title"
        # ] = f"Income inequality: P90/P50 ratio ({source_checkbox['type_title'][view]})"
        # df_graphers.loc[j, "ySlugs"] = source_checkbox["p90_p50"][view]
        # df_graphers.loc[j, "Indicator Dropdown"] = "P90/P50"
        # df_graphers.loc[j, "Income measure Dropdown"] = source_checkbox["type_title"][
        #     view
        # ].capitalize()
        # df_graphers.loc[
        #     j, "subtitle"
        # ] = f"The P90/P50 ratio measures the degree of inequality within the richest half of the population. A ratio of 2 means that someone just falling in the richest tenth of the population has twice the median income."
        # df_graphers.loc[j, "note"] = ""
        # df_graphers.loc[j, "type"] = np.nan
        # j += 1

        # # P50/P10
        # df_graphers.loc[
        #     j, "title"
        # ] = f"Income inequality: P50/P10 ratio ({source_checkbox['type_title'][view]})"
        # df_graphers.loc[j, "ySlugs"] = source_checkbox["p50_p10"][view]
        # df_graphers.loc[j, "Indicator Dropdown"] = "P50/P10"
        # df_graphers.loc[j, "Income measure Dropdown"] = source_checkbox["type_title"][
        #     view
        # ].capitalize()
        # df_graphers.loc[
        #     j, "subtitle"
        # ] = f"The P50/P10 ratio measures the degree of inequality within the poorest half of the population. A ratio of 2 means that the median income is two times higher than that of someone just falling in the poorest tenth of the population."
        # df_graphers.loc[j, "note"] = ""
        # df_graphers.loc[j, "type"] = np.nan
        # j += 1

        # Palma ratio
        df_graphers.loc[
            j, "title"
        ] = f"Palma ratio ({source_checkbox['type_title'][view]})"
        df_graphers.loc[j, "ySlugs"] = source_checkbox["palma"][view]
        df_graphers.loc[j, "Indicator Dropdown"] = "Palma ratio"
        df_graphers.loc[j, "Income measure Dropdown"] = source_checkbox["type_title"][
            view
        ].capitalize()
        df_graphers.loc[
            j, "subtitle"
        ] = f"The share of income of the richest 10% divided by the share of the poorest 40%."
        df_graphers.loc[j, "note"] = ""
        df_graphers.loc[j, "type"] = np.nan
        j += 1

        # Headcount ratio (rel)
        df_graphers.loc[
            j, "title"
        ] = f"Share in relative poverty ({source_checkbox['type_title'][view]})"
        df_graphers.loc[j, "ySlugs"] = source_checkbox["relative"][view]
        df_graphers.loc[j, "Indicator Dropdown"] = f"Share in relative poverty"
        df_graphers.loc[j, "Income measure Dropdown"] = source_checkbox["type_title"][
            view
        ].capitalize()
        df_graphers.loc[
            j, "subtitle"
        ] = f"The share of population with income below 50% of the median. Relative poverty is a measure of the extent of inequality within the bottom of the distribution."
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

# Remove relative poverty view for before tax (no PIP data)
df_graphers = df_graphers[
    ~(
        (df_graphers["Income measure Dropdown"] == "Before tax")
        & (df_graphers["Indicator Dropdown"] == "Share in relative poverty")
    )
].reset_index(drop=True)

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
    (df_graphers["Indicator Dropdown"] == "Gini coefficient")
    & (df_graphers["Income measure Dropdown"] == "After tax"),
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
        f.write("\ncolumns\t" + tab + "\n" + table_tsv_indented)