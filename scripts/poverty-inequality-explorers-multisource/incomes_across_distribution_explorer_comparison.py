# %% [markdown]
# # Incomes Across the Distribution Explorer - Source Comparison
# This code creates the tsv file for the incomes across the distribution comparison explorer, available [here](https://owid.cloud/admin/explorers/preview/incomes-across-distribution-comparison)

import textwrap
from pathlib import Path

import numpy as np

# %%
import pandas as pd

PARENT_DIR = Path(__file__).parent.parent.parent.absolute()
outfile = (
    PARENT_DIR / "explorers" / "incomes-across-distribution-comparison.explorer.tsv"
)

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

# Relative poverty sheet
sheet_name = "povlines_rel"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
lis_povlines_rel = pd.read_csv(url)

# Deciles9 sheet (needed to handle thresholds data)
sheet_name = "deciles9"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
lis_deciles9 = pd.read_csv(url, keep_default_na=False)

# Deciles10 sheet (needed to handle average and share data)
sheet_name = "deciles10"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
lis_deciles10 = pd.read_csv(url, keep_default_na=False)

# Income aggregation sheet (day, month, year)
sheet_name = "income_aggregation"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
lis_income_aggregation = pd.read_csv(
    url, keep_default_na=False, dtype={"multiplier": "str"}
)

# WORLD INEQUALITY DATABASE
# Read Google sheets
sheet_id = "18T5IGnpyJwb8KL9USYvME6IaLEcYIo26ioHCpkDnwRQ"

# Welfare type sheet
sheet_name = "welfare"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
wid_welfare = pd.read_csv(url, keep_default_na=False)

# Deciles9 sheet (needed to handle thresholds data)
sheet_name = "deciles9"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
wid_deciles9 = pd.read_csv(url, keep_default_na=False)

# Deciles10 sheet (needed to handle average and share data)
sheet_name = "deciles10"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
wid_deciles10 = pd.read_csv(url, keep_default_na=False)

# Income aggregation sheet (day, month, year)
sheet_name = "income_aggregation"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
wid_income_aggregation = pd.read_csv(
    url, keep_default_na=False, dtype={"multiplier": "str"}
)

# WORLD BANK POVERTY AND INEQUALITY PLATFORM
# Read Google sheets
sheet_id = "17KJ9YcvfdmO_7-Sv2Ij0vmzAQI6rXSIqHfJtgFHN-a8"

# Survey type sheet
sheet_name = "table"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
pip_tables = pd.read_csv(url)

# Settings for 10 deciles variables (share, avg) sheet
sheet_name = "deciles10"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
pip_deciles10 = pd.read_csv(url, dtype={"dropdown": "str", "decile": "str"})

# Settings for 9 deciles variables (thr) sheet
sheet_name = "deciles9"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
pip_deciles9 = pd.read_csv(url, dtype={"dropdown": "str", "decile": "str"})

# Income aggregation sheet (day, month, year)
sheet_name = "income_aggregation"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
pip_income_aggregation = pd.read_csv(
    url, keep_default_na=False, dtype={"multiplier": "str"}
)

# %% [markdown]
# ## Header
# General settings of the explorer are defined here, like the title, subtitle, default country selection, publishing status and others.

# %%
# The header is defined as a dictionary first and then it is converted into a index-oriented dataframe
header_dict = {
    "explorerTitle": "Incomes Across the Distribution Explorer - Source comparison",
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

    for agg in range(len(pip_income_aggregation)):
        # mean
        df_tables_pip.loc[j, "name"] = f"Mean {pip_tables.text[tab]} (PIP)"
        df_tables_pip.loc[j, "slug"] = f"mean{pip_income_aggregation.slug_suffix[agg]}"
        df_tables_pip.loc[
            j, "description"
        ] = f"The mean level of {pip_tables.text[tab]} per {pip_income_aggregation.aggregation[agg]}."
        df_tables_pip.loc[j, "unit"] = "international-$ in 2017 prices"
        df_tables_pip.loc[j, "shortUnit"] = "$"
        df_tables_pip.loc[j, "type"] = "Numeric"
        df_tables_pip.loc[j, "colorScaleNumericBins"] = pip_income_aggregation.scale[
            agg
        ]
        df_tables_pip.loc[j, "colorScaleScheme"] = "BuGn"
        df_tables_pip.loc[
            j, "transform"
        ] = f"multiplyBy mean {pip_income_aggregation.multiplier[agg]}"
        j += 1

        # median
        df_tables_pip.loc[j, "name"] = f"Median {pip_tables.text[tab]} (PIP)"
        df_tables_pip.loc[
            j, "slug"
        ] = f"median{pip_income_aggregation.slug_suffix[agg]}"
        df_tables_pip.loc[
            j, "description"
        ] = f"The level of {pip_tables.text[tab]} per {pip_income_aggregation.aggregation[agg]} below which half of the population live."
        df_tables_pip.loc[j, "unit"] = "international-$ in 2017 prices"
        df_tables_pip.loc[j, "shortUnit"] = "$"
        df_tables_pip.loc[j, "type"] = "Numeric"
        df_tables_pip.loc[j, "colorScaleNumericBins"] = pip_income_aggregation.scale[
            agg
        ]
        df_tables_pip.loc[j, "colorScaleScheme"] = "Blues"
        df_tables_pip.loc[
            j, "transform"
        ] = f"multiplyBy median {pip_income_aggregation.multiplier[agg]}"
        j += 1

        for dec9 in range(len(pip_deciles9)):
            # thresholds
            df_tables_pip.loc[j, "name"] = f"{pip_deciles9.ordinal[dec9]} (PIP)"
            df_tables_pip.loc[
                j, "slug"
            ] = f"decile{pip_deciles9.decile[dec9]}_thr{pip_income_aggregation.slug_suffix[agg]}"
            df_tables_pip.loc[
                j, "description"
            ] = f"The level of {pip_tables.text[tab]} per {pip_income_aggregation.aggregation[agg]} below which {pip_deciles9.decile[dec9]}0% of the population falls."
            df_tables_pip.loc[j, "unit"] = "international-$ in 2017 prices"
            df_tables_pip.loc[j, "shortUnit"] = "$"
            df_tables_pip.loc[j, "type"] = "Numeric"
            df_tables_pip.loc[
                j, "colorScaleNumericBins"
            ] = pip_income_aggregation.scale[agg]
            df_tables_pip.loc[j, "colorScaleScheme"] = "Purples"
            df_tables_pip.loc[
                j, "transform"
            ] = f"multiplyBy decile{pip_deciles9.decile[dec9]}_thr {pip_income_aggregation.multiplier[agg]}"
            j += 1

        for dec10 in range(len(pip_deciles10)):
            # averages
            df_tables_pip.loc[j, "name"] = f"{pip_deciles10.ordinal[dec10]} (PIP)"
            df_tables_pip.loc[
                j, "slug"
            ] = f"decile{pip_deciles10.decile[dec10]}_avg{pip_income_aggregation.slug_suffix[agg]}"
            df_tables_pip.loc[
                j, "description"
            ] = f"The mean {pip_tables.text[tab]} per {pip_income_aggregation.aggregation[agg]} within the {pip_deciles10.ordinal[dec10]} (tenth of the population)."
            df_tables_pip.loc[j, "unit"] = "international-$ in 2017 prices"
            df_tables_pip.loc[j, "shortUnit"] = "$"
            df_tables_pip.loc[j, "type"] = "Numeric"
            df_tables_pip.loc[
                j, "colorScaleNumericBins"
            ] = pip_income_aggregation.scale[agg]
            df_tables_pip.loc[j, "colorScaleScheme"] = "Greens"
            df_tables_pip.loc[
                j, "transform"
            ] = f"multiplyBy decile{pip_deciles10.decile[dec10]}_avg {pip_income_aggregation.multiplier[agg]}"
            j += 1

    for dec10 in range(len(pip_deciles10)):
        # shares
        df_tables_pip.loc[j, "name"] = f"{pip_deciles10.ordinal[dec10]} (PIP)"
        df_tables_pip.loc[j, "slug"] = f"decile{pip_deciles10.decile[dec10]}_share"
        df_tables_pip.loc[
            j, "description"
        ] = f"The {pip_tables.text[tab]} of the {pip_deciles10.ordinal[dec10]} (tenth of the population) as a share of total {pip_tables.text[tab]}."
        df_tables_pip.loc[j, "unit"] = "%"
        df_tables_pip.loc[j, "shortUnit"] = "%"
        df_tables_pip.loc[j, "type"] = "Numeric"
        df_tables_pip.loc[j, "colorScaleNumericBins"] = pip_deciles10.scale_share[dec10]
        df_tables_pip.loc[j, "colorScaleScheme"] = "OrRd"
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
        for agg in range(len(wid_income_aggregation)):
            # Mean
            df_tables_wid.loc[
                j, "name"
            ] = f"Mean {wid_welfare['welfare_type'][wel]} (WID)"
            df_tables_wid.loc[
                j, "slug"
            ] = f"p0p100_avg_{wid_welfare['slug'][wel]}{wid_income_aggregation['slug_suffix'][agg]}"
            df_tables_wid.loc[
                j, "description"
            ] = f"Mean {wid_welfare['welfare_type'][wel]}.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
            df_tables_wid.loc[j, "unit"] = "international-$ in 2021 prices"
            df_tables_wid.loc[j, "shortUnit"] = "$"
            df_tables_wid.loc[j, "type"] = "Numeric"
            df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare["scale_mean"][
                wel
            ]
            df_tables_wid.loc[j, "colorScaleScheme"] = "BuGn"
            df_tables_wid.loc[
                j, "transform"
            ] = f"multiplyBy p0p100_avg_{wid_welfare['slug'][wel]} {wid_income_aggregation['multiplier'][agg]}"
            j += 1

            # Median
            df_tables_wid.loc[
                j, "name"
            ] = f"Median {wid_welfare['welfare_type'][wel]} (WID)"
            df_tables_wid.loc[
                j, "slug"
            ] = f"median_{wid_welfare['slug'][wel]}{wid_income_aggregation['slug_suffix'][agg]}"
            df_tables_wid.loc[
                j, "description"
            ] = f"This is the level of {wid_welfare['welfare_type'][wel]} below which 50% of the population falls.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
            df_tables_wid.loc[j, "unit"] = "international-$ in 2021 prices"
            df_tables_wid.loc[j, "shortUnit"] = "$"
            df_tables_wid.loc[j, "type"] = "Numeric"
            df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare["scale_median"][
                wel
            ]
            df_tables_wid.loc[j, "colorScaleScheme"] = "Blues"
            df_tables_wid.loc[
                j, "transform"
            ] = f"multiplyBy median_{wid_welfare['slug'][wel]} {wid_income_aggregation['multiplier'][agg]}"
            j += 1

            # Thresholds - Deciles
            for dec9 in range(len(wid_deciles9)):
                df_tables_wid.loc[
                    j, "name"
                ] = f"{wid_deciles9['ordinal'][dec9].capitalize()} (WID)"
                df_tables_wid.loc[
                    j, "slug"
                ] = f"{wid_deciles9['wid_notation'][dec9]}_thr_{wid_welfare['slug'][wel]}{wid_income_aggregation['slug_suffix'][agg]}"
                df_tables_wid.loc[
                    j, "description"
                ] = f"The level of {wid_welfare['welfare_type'][wel]} below which {wid_deciles9['decile'][dec9]}0% of the population falls.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
                df_tables_wid.loc[j, "unit"] = "international-$ in 2021 prices"
                df_tables_wid.loc[j, "shortUnit"] = "$"
                df_tables_wid.loc[j, "type"] = "Numeric"
                df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_deciles9[
                    "scale_thr"
                ][dec9]
                df_tables_wid.loc[j, "colorScaleScheme"] = "Purples"
                df_tables_wid.loc[
                    j, "transform"
                ] = f"multiplyBy {wid_deciles9['wid_notation'][dec9]}_thr_{wid_welfare['slug'][wel]} {wid_income_aggregation['multiplier'][agg]}"
                j += 1

            # Averages - Deciles
            for dec10 in range(len(wid_deciles10)):
                df_tables_wid.loc[
                    j, "name"
                ] = f"{wid_deciles10['ordinal'][dec10].capitalize()} (WID)"
                df_tables_wid.loc[
                    j, "slug"
                ] = f"{wid_deciles10['wid_notation'][dec10]}_avg_{wid_welfare['slug'][wel]}{wid_income_aggregation['slug_suffix'][agg]}"
                df_tables_wid.loc[
                    j, "description"
                ] = f"This is the mean {wid_welfare['welfare_type'][wel]} within the {wid_deciles10['ordinal'][dec10]} (tenth of the population).{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
                df_tables_wid.loc[j, "unit"] = "international-$ in 2021 prices"
                df_tables_wid.loc[j, "shortUnit"] = "$"
                df_tables_wid.loc[j, "type"] = "Numeric"
                df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_deciles10[
                    "scale_avg"
                ][dec10]
                df_tables_wid.loc[j, "colorScaleScheme"] = "Greens"
                df_tables_wid.loc[
                    j, "transform"
                ] = f"multiplyBy {wid_deciles10['wid_notation'][dec10]}_avg_{wid_welfare['slug'][wel]} {wid_income_aggregation['multiplier'][agg]}"
                j += 1

        # Shares - Deciles
        for dec10 in range(len(wid_deciles10)):
            df_tables_wid.loc[
                j, "name"
            ] = f"{wid_deciles10['ordinal'][dec10].capitalize()} (WID)"
            df_tables_wid.loc[
                j, "slug"
            ] = f"{wid_deciles10['wid_notation'][dec10]}_share_{wid_welfare['slug'][wel]}"
            df_tables_wid.loc[
                j, "description"
            ] = f"This is the {wid_welfare['welfare_type'][wel]} of the {wid_deciles10['ordinal'][dec10]} (tenth of the population) as a share of total {wid_welfare['welfare_type'][wel]}.{new_line}This is {wid_welfare['technical_text'][wel]}. {wid_welfare['subtitle'][wel]} {wid_welfare['note'][wel]}"
            df_tables_wid.loc[j, "unit"] = "%"
            df_tables_wid.loc[j, "shortUnit"] = "%"
            df_tables_wid.loc[j, "type"] = "Numeric"
            df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_deciles10[
                "scale_share"
            ][dec10]
            df_tables_wid.loc[j, "colorScaleScheme"] = "OrRd"
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
            for agg in range(len(lis_income_aggregation)):
                # Mean
                df_tables_lis.loc[
                    j, "name"
                ] = f"Mean {lis_welfare['welfare_type'][wel]} (LIS)"
                df_tables_lis.loc[
                    j, "slug"
                ] = f"mean_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}{lis_income_aggregation['slug_suffix'][agg]}"
                df_tables_lis.loc[
                    j, "description"
                ] = f"Mean {lis_welfare['welfare_type'][wel]}.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
                df_tables_lis.loc[j, "unit"] = "international-$ in 2017 prices"
                df_tables_lis.loc[j, "shortUnit"] = "$"
                df_tables_lis.loc[j, "type"] = "Numeric"
                df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_welfare[
                    "scale_mean"
                ][wel]
                df_tables_lis.loc[j, "colorScaleScheme"] = "BuGn"
                df_tables_lis.loc[
                    j, "transform"
                ] = f"multiplyBy mean_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]} {lis_income_aggregation['multiplier'][agg]}"
                j += 1

                # Median
                df_tables_lis.loc[
                    j, "name"
                ] = f"Median {lis_welfare['welfare_type'][wel]} (LIS)"
                df_tables_lis.loc[
                    j, "slug"
                ] = f"median_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}{lis_income_aggregation['slug_suffix'][agg]}"
                df_tables_lis.loc[
                    j, "description"
                ] = f"The level of {lis_welfare['welfare_type'][wel]} below which half of the population live.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
                df_tables_lis.loc[j, "unit"] = "international-$ in 2017 prices"
                df_tables_lis.loc[j, "shortUnit"] = "$"
                df_tables_lis.loc[j, "type"] = "Numeric"
                df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_welfare[
                    "scale_median"
                ][wel]
                df_tables_lis.loc[j, "colorScaleScheme"] = "Blues"
                df_tables_lis.loc[
                    j, "transform"
                ] = f"multiplyBy median_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]} {lis_income_aggregation['multiplier'][agg]}"
                j += 1

                # Thresholds - Deciles
                for dec9 in range(len(lis_deciles9)):
                    df_tables_lis.loc[
                        j, "name"
                    ] = f"{lis_deciles9['ordinal'][dec9].capitalize()} (LIS)"
                    df_tables_lis.loc[
                        j, "slug"
                    ] = f"thr_{lis_deciles9['lis_notation'][dec9]}_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}{lis_income_aggregation['slug_suffix'][agg]}"
                    df_tables_lis.loc[
                        j, "description"
                    ] = f"The level of {lis_welfare['welfare_type'][wel]} below which {lis_deciles9['decile'][dec9]}0% of the population falls.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
                    df_tables_lis.loc[j, "unit"] = "international-$ in 2017 prices"
                    df_tables_lis.loc[j, "shortUnit"] = "$"
                    df_tables_lis.loc[j, "type"] = "Numeric"
                    df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_deciles9[
                        "scale_thr"
                    ][dec9]
                    df_tables_lis.loc[j, "colorScaleScheme"] = "Purples"
                    df_tables_lis.loc[
                        j, "transform"
                    ] = f"multiplyBy thr_{lis_deciles9['lis_notation'][dec9]}_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]} {lis_income_aggregation['multiplier'][agg]}"
                    j += 1

                # Averages - Deciles
                for dec10 in range(len(lis_deciles10)):
                    df_tables_lis.loc[
                        j, "name"
                    ] = f"{lis_deciles10['ordinal'][dec10].capitalize()} (LIS)"
                    df_tables_lis.loc[
                        j, "slug"
                    ] = f"avg_{lis_deciles10['lis_notation'][dec10]}_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}{lis_income_aggregation['slug_suffix'][agg]}"
                    df_tables_lis.loc[
                        j, "description"
                    ] = f"This is the mean {lis_welfare['welfare_type'][wel]} within the {lis_deciles10['ordinal'][dec10]} (tenth of the population).{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
                    df_tables_lis.loc[j, "unit"] = "international-$ in 2017 prices"
                    df_tables_lis.loc[j, "shortUnit"] = "$"
                    df_tables_lis.loc[j, "type"] = "Numeric"
                    df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_deciles10[
                        "scale_avg"
                    ][dec10]
                    df_tables_lis.loc[j, "colorScaleScheme"] = "Greens"
                    df_tables_lis.loc[
                        j, "transform"
                    ] = f"multiplyBy avg_{lis_deciles10['lis_notation'][dec10]}_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]} {lis_income_aggregation['multiplier'][agg]}"
                    j += 1

            # Shares - Deciles
            for dec10 in range(len(lis_deciles10)):
                df_tables_lis.loc[
                    j, "name"
                ] = f"{lis_deciles10['ordinal'][dec10].capitalize()} (LIS)"
                df_tables_lis.loc[
                    j, "slug"
                ] = f"share_{lis_deciles10['lis_notation'][dec10]}_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
                df_tables_lis.loc[
                    j, "description"
                ] = f"This is the {lis_welfare['welfare_type'][wel]} of the {lis_deciles10['ordinal'][dec10]} (tenth of the population) as a share of total {lis_welfare['welfare_type'][wel]}.{new_line}This is {lis_welfare['technical_text'][wel]}. {lis_welfare['subtitle'][wel]}{new_line}Household {lis_welfare['welfare_type'][wel]} {lis_equivalence_scales['note'][eq]}"
                df_tables_lis.loc[j, "unit"] = "%"
                df_tables_lis.loc[j, "shortUnit"] = "%"
                df_tables_lis.loc[j, "type"] = "Numeric"
                df_tables_lis.loc[j, "colorScaleNumericBins"] = lis_deciles10[
                    "scale_share"
                ][dec10]
                df_tables_lis.loc[j, "colorScaleScheme"] = "OrRd"
                j += 1

    df_tables_lis["tableSlug"] = merged_tables["name"][tab]

df_tables_lis["sourceName"] = sourceName
df_tables_lis["dataPublishedBy"] = dataPublishedBy
df_tables_lis["sourceLink"] = sourceLink
df_tables_lis["colorScaleNumericMinValue"] = colorScaleNumericMinValue
df_tables_lis["tolerance"] = tolerance
df_tables_lis["colorScaleEqualSizeBins"] = colorScaleEqualSizeBins

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
        for agg in range(len(lis_income_aggregation)):
            # Mean
            df_graphers.loc[
                j, "title"
            ] = f"Mean income per {lis_income_aggregation['aggregation'][agg]} ({source_checkbox['type_title'][view]})"
            df_graphers.loc[j, "ySlugs"] = source_checkbox["mean"][view].replace(
                "{agg}", lis_income_aggregation["slug_suffix"][agg]
            )
            df_graphers.loc[j, "Income type Dropdown"] = source_checkbox["type_title"][
                view
            ].capitalize()
            df_graphers.loc[j, "Metric Dropdown"] = "Mean income or consumption"
            df_graphers.loc[j, "Decile Dropdown"] = np.nan
            df_graphers.loc[j, "Aggregation Radio"] = lis_income_aggregation[
                "aggregation"
            ][agg].capitalize()
            df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][view]
            df_graphers.loc[j, "World Inequality Database Checkbox"] = source_checkbox[
                "wid"
            ][view]
            df_graphers.loc[j, "Luxembourg Income Study Checkbox"] = source_checkbox[
                "lis"
            ][view]
            df_graphers.loc[
                j, "subtitle"
            ] = f"This data is adjusted for inflation and for differences in the cost of living between countries."
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2017 prices."
            df_graphers.loc[j, "yScaleToggle"] = "true"
            j += 1

        #     # Median
        #     df_graphers.loc[
        #         j, "title"
        #     ] = f"Median per {lis_income_aggregation['aggregation'][agg]} ({source_checkbox['type_title'][view]})"
        #     df_graphers.loc[
        #         j, "ySlugs"
        #     ] = f"median_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
        #     df_graphers.loc[j, "Metric Dropdown"] = "Median income or consumption"
        #     df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][view]
        #     df_graphers.loc[j, "World Inequality Database Checkbox"] = source_checkbox[
        #         "wid"
        #     ][view]
        #     df_graphers.loc[j, "Luxembourg Income Study Checkbox"] = source_checkbox[
        #         "lis"
        #     ][view]
        #     df_graphers.loc[j, "Decile Dropdown"] = np.nan
        #     df_graphers.loc[
        #         j, "Welfare type Dropdown"
        #     ] = f"{welfare['dropdown_option'][wel]}"
        #     df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
        #         "text"
        #     ][eq].capitalize()
        #     df_graphers.loc[j, "Relative change Checkbox"] = relative_toggle[
        #         "checkbox"
        #     ][rel_toggle]
        #     df_graphers.loc[j, "stackMode"] = relative_toggle["stack_mode"][rel_toggle]
        #     df_graphers.loc[
        #         j, "subtitle"
        #     ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. {welfare['subtitle'][wel]}"
        #     df_graphers.loc[
        #         j, "note"
        #     ] = f"This data is measured in international-$ at 2017 prices."
        #     df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
        #     df_graphers.loc[j, "hasMapTab"] = "true"
        #     df_graphers.loc[j, "tab"] = "map"
        #     df_graphers.loc[j, "yScaleToggle"] = "true"
        #     j += 1

        #     # Thresholds - Deciles
        #     for dec9 in range(len(deciles9)):
        #         df_graphers.loc[
        #             j, "title"
        #         ] = f"Threshold {welfare['welfare_type'][wel]} marking the {deciles9['ordinal'][dec9]} ({source_checkbox['type_title'][view]})"
        #         df_graphers.loc[
        #             j, "ySlugs"
        #         ] = f"thr_{deciles9['lis_notation'][dec9]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
        #         df_graphers.loc[j, "Metric Dropdown"] = "Decile thresholds"
        #         df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][
        #             view
        #         ]
        #         df_graphers.loc[
        #             j, "World Inequality Database Checkbox"
        #         ] = source_checkbox["wid"][view]
        #         df_graphers.loc[
        #             j, "Luxembourg Income Study Checkbox"
        #         ] = source_checkbox["lis"][view]
        #         df_graphers.loc[j, "Decile Dropdown"] = deciles9["dropdown"][dec9]
        #         df_graphers.loc[
        #             j, "Welfare type Dropdown"
        #         ] = f"{welfare['dropdown_option'][wel]}"
        #         df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
        #             "text"
        #         ][eq].capitalize()
        #         df_graphers.loc[j, "Relative change Checkbox"] = relative_toggle[
        #             "checkbox"
        #         ][rel_toggle]
        #         df_graphers.loc[j, "stackMode"] = relative_toggle["stack_mode"][
        #             rel_toggle
        #         ]
        #         df_graphers.loc[
        #             j, "subtitle"
        #         ] = f"This is the level of {welfare['welfare_type'][wel]} below which {deciles9['decile'][dec9]}0% of the population falls. {welfare['subtitle'][wel]}"
        #         df_graphers.loc[
        #             j, "note"
        #         ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries."
        #         df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
        #         df_graphers.loc[j, "hasMapTab"] = "true"
        #         df_graphers.loc[j, "tab"] = "map"
        #         df_graphers.loc[j, "yScaleToggle"] = "true"
        #         j += 1

        #     # Averages - Deciles
        #     for dec10 in range(len(deciles10)):
        #         df_graphers.loc[
        #             j, "title"
        #         ] = f"Mean {welfare['welfare_type'][wel]} within the {deciles10['ordinal'][dec10]} ({source_checkbox['type_title'][view]})"
        #         df_graphers.loc[
        #             j, "ySlugs"
        #         ] = f"avg_{deciles10['lis_notation'][dec10]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
        #         df_graphers.loc[
        #             j, "Metric Dropdown"
        #         ] = "Mean income or consumption, by decile"
        #         df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][
        #             view
        #         ]
        #         df_graphers.loc[
        #             j, "World Inequality Database Checkbox"
        #         ] = source_checkbox["wid"][view]
        #         df_graphers.loc[
        #             j, "Luxembourg Income Study Checkbox"
        #         ] = source_checkbox["lis"][view]
        #         df_graphers.loc[j, "Decile Dropdown"] = deciles10["dropdown"][dec10]
        #         df_graphers.loc[
        #             j, "Welfare type Dropdown"
        #         ] = f"{welfare['dropdown_option'][wel]}"
        #         df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
        #             "text"
        #         ][eq].capitalize()
        #         df_graphers.loc[j, "Relative change Checkbox"] = relative_toggle[
        #             "checkbox"
        #         ][rel_toggle]
        #         df_graphers.loc[j, "stackMode"] = relative_toggle["stack_mode"][
        #             rel_toggle
        #         ]
        #         df_graphers.loc[
        #             j, "subtitle"
        #         ] = f"This is the mean {welfare['welfare_type'][wel]} within the {deciles10['ordinal'][dec10]} (tenth of the population). {welfare['subtitle'][wel]}"
        #         df_graphers.loc[
        #             j, "note"
        #         ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries."
        #         df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
        #         df_graphers.loc[j, "hasMapTab"] = "true"
        #         df_graphers.loc[j, "tab"] = "map"
        #         df_graphers.loc[j, "yScaleToggle"] = "true"
        #         j += 1

        # # Shares - Deciles
        # for dec10 in range(len(deciles10)):
        #     df_graphers.loc[
        #         j, "title"
        #     ] = f"{welfare['welfare_type'][wel].capitalize()} share of the {deciles10['ordinal'][dec10]} ({source_checkbox['type_title'][view]})"
        #     df_graphers.loc[
        #         j, "ySlugs"
        #     ] = f"share_{deciles10['lis_notation'][dec10]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
        #     df_graphers.loc[j, "Metric Dropdown"] = "Decile shares"
        #     df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][view]
        #     df_graphers.loc[j, "World Inequality Database Checkbox"] = source_checkbox[
        #         "wid"
        #     ][view]
        #     df_graphers.loc[j, "Luxembourg Income Study Checkbox"] = source_checkbox[
        #         "lis"
        #     ][view]
        #     df_graphers.loc[j, "Decile Dropdown"] = deciles10["dropdown"][dec10]
        #     df_graphers.loc[
        #         j, "Welfare type Dropdown"
        #     ] = f"{welfare['dropdown_option'][wel]}"
        #     df_graphers.loc[j, "Equivalence scale Dropdown"] = equivalence_scales[
        #         "text"
        #     ][eq].capitalize()
        #     df_graphers.loc[j, "Relative change Checkbox"] = relative_toggle[
        #         "checkbox"
        #     ][rel_toggle]
        #     df_graphers.loc[j, "stackMode"] = relative_toggle["stack_mode"][rel_toggle]
        #     df_graphers.loc[
        #         j, "subtitle"
        #     ] = f"This is the {welfare['welfare_type'][wel]} of the {deciles10['ordinal'][dec10]} (tenth of the population) as a share of total {welfare['welfare_type'][wel]}. {welfare['subtitle'][wel]}"
        #     df_graphers.loc[j, "note"] = np.nan
        #     df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
        #     df_graphers.loc[j, "hasMapTab"] = "true"
        #     df_graphers.loc[j, "tab"] = "map"
        #     j += 1

        # # Gini coefficient
        # df_graphers.loc[
        #     j, "title"
        # ] = f"Income inequality: Gini coefficient ({source_checkbox['type_title'][view]})"
        # df_graphers.loc[j, "ySlugs"] = source_checkbox["gini"][view]
        # df_graphers.loc[j, "Income type Dropdown"] = source_checkbox["type_title"][
        #     view
        # ].capitalize()
        # df_graphers.loc[j, "Metric Dropdown"] = "Gini coefficient"
        # df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][view]
        # df_graphers.loc[j, "World Inequality Database Checkbox"] = source_checkbox[
        #     "wid"
        # ][view]
        # df_graphers.loc[j, "Luxembourg Income Study Checkbox"] = source_checkbox["lis"][
        #     view
        # ]
        # df_graphers.loc[
        #     j, "subtitle"
        # ] = f"The Gini coefficient is a measure of the inequality of the income distribution in a population. Higher values indicate a higher level of inequality."
        # df_graphers.loc[j, "note"] = ""
        # df_graphers.loc[j, "type"] = np.nan
        # j += 1

        # # Share of the top 10%
        # df_graphers.loc[
        #     j, "title"
        # ] = f"Income share of the top 10% ({source_checkbox['type_title'][view]})"
        # df_graphers.loc[j, "ySlugs"] = source_checkbox["top10"][view]
        # df_graphers.loc[j, "Income type Dropdown"] = source_checkbox["type_title"][
        #     view
        # ].capitalize()
        # df_graphers.loc[j, "Metric Dropdown"] = "Top 10% share"
        # df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][view]
        # df_graphers.loc[j, "World Inequality Database Checkbox"] = source_checkbox[
        #     "wid"
        # ][view]
        # df_graphers.loc[j, "Luxembourg Income Study Checkbox"] = source_checkbox["lis"][
        #     view
        # ]
        # df_graphers.loc[
        #     j, "subtitle"
        # ] = f"This is the income of the richest 10% as a share of total income."
        # df_graphers.loc[j, "note"] = ""
        # df_graphers.loc[j, "type"] = np.nan
        # j += 1

        # # Share of the bottom 50%
        # df_graphers.loc[
        #     j, "title"
        # ] = f"Income share of the bottom 50% ({source_checkbox['type_title'][view]})"
        # df_graphers.loc[j, "ySlugs"] = source_checkbox["bottom50"][view]
        # df_graphers.loc[j, "Income type Dropdown"] = source_checkbox["type_title"][
        #     view
        # ].capitalize()
        # df_graphers.loc[j, "Metric Dropdown"] = "Bottom 50% share"
        # df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][view]
        # df_graphers.loc[j, "World Inequality Database Checkbox"] = source_checkbox[
        #     "wid"
        # ][view]
        # df_graphers.loc[j, "Luxembourg Income Study Checkbox"] = source_checkbox["lis"][
        #     view
        # ]
        # df_graphers.loc[
        #     j, "subtitle"
        # ] = f"This is the income of the poorest 50% as a share of total income."
        # df_graphers.loc[j, "note"] = ""
        # j += 1

        # # P90/P10
        # df_graphers.loc[
        #     j, "title"
        # ] = f"Income inequality: P90/P10 ratio ({source_checkbox['type_title'][view]})"
        # df_graphers.loc[j, "ySlugs"] = source_checkbox["p90_p10"][view]
        # df_graphers.loc[j, "Income type Dropdown"] = source_checkbox["type_title"][
        #     view
        # ].capitalize()
        # df_graphers.loc[j, "Metric Dropdown"] = "P90/P10"
        # df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][view]
        # df_graphers.loc[j, "World Inequality Database Checkbox"] = source_checkbox[
        #     "wid"
        # ][view]
        # df_graphers.loc[j, "Luxembourg Income Study Checkbox"] = source_checkbox["lis"][
        #     view
        # ]
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
        # df_graphers.loc[j, "Income type Dropdown"] = source_checkbox["type_title"][
        #     view
        # ].capitalize()
        # df_graphers.loc[j, "Metric Dropdown"] = "P90/P50"
        # df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][view]
        # df_graphers.loc[j, "World Inequality Database Checkbox"] = source_checkbox[
        #     "wid"
        # ][view]
        # df_graphers.loc[j, "Luxembourg Income Study Checkbox"] = source_checkbox["lis"][
        #     view
        # ]
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
        # df_graphers.loc[j, "Income type Dropdown"] = source_checkbox["type_title"][
        #     view
        # ].capitalize()
        # df_graphers.loc[j, "Metric Dropdown"] = "P50/P10"
        # df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][view]
        # df_graphers.loc[j, "World Inequality Database Checkbox"] = source_checkbox[
        #     "wid"
        # ][view]
        # df_graphers.loc[j, "Luxembourg Income Study Checkbox"] = source_checkbox["lis"][
        #     view
        # ]
        # df_graphers.loc[
        #     j, "subtitle"
        # ] = f"The P50/P10 ratio measures the degree of inequality within the poorest half of the population. A ratio of 2 means that the median income is two times higher than that of someone just falling in the poorest tenth of the population."
        # df_graphers.loc[j, "note"] = ""
        # df_graphers.loc[j, "type"] = np.nan
        # j += 1

        # # Palma ratio
        # df_graphers.loc[
        #     j, "title"
        # ] = f"Income inequality: Palma ratio ({source_checkbox['type_title'][view]})"
        # df_graphers.loc[j, "ySlugs"] = source_checkbox["palma"][view]
        # df_graphers.loc[j, "Income type Dropdown"] = source_checkbox["type_title"][
        #     view
        # ].capitalize()
        # df_graphers.loc[j, "Metric Dropdown"] = "Palma ratio"
        # df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][view]
        # df_graphers.loc[j, "World Inequality Database Checkbox"] = source_checkbox[
        #     "wid"
        # ][view]
        # df_graphers.loc[j, "Luxembourg Income Study Checkbox"] = source_checkbox["lis"][
        #     view
        # ]
        # df_graphers.loc[
        #     j, "subtitle"
        # ] = f"The Palma ratio is the share of total income of the top 10% divided by the share of the bottom 40%."
        # df_graphers.loc[j, "note"] = ""
        # df_graphers.loc[j, "type"] = np.nan
        # j += 1

        # # Headcount ratio (rel)
        # df_graphers.loc[
        #     j, "title"
        # ] = f"Relative poverty: Share of people below 50% of the median income ({source_checkbox['type_title'][view]})"
        # df_graphers.loc[j, "ySlugs"] = source_checkbox["relative"][view]
        # df_graphers.loc[j, "Income type Dropdown"] = source_checkbox["type_title"][
        #     view
        # ].capitalize()
        # df_graphers.loc[
        #     j, "Metric Dropdown"
        # ] = f"Share in relative poverty (< 50% of the median)"
        # df_graphers.loc[j, "World Bank PIP Checkbox"] = source_checkbox["pip"][view]
        # df_graphers.loc[j, "World Inequality Database Checkbox"] = source_checkbox[
        #     "wid"
        # ][view]
        # df_graphers.loc[j, "Luxembourg Income Study Checkbox"] = source_checkbox["lis"][
        #     view
        # ]
        # df_graphers.loc[
        #     j, "subtitle"
        # ] = f"Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at 50% of the median income."
        # df_graphers.loc[j, "note"] = ""
        # df_graphers.loc[j, "type"] = np.nan
        # j += 1

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
    & (df_graphers["Metric Dropdown"] == "Mean income or consumption")
    & (df_graphers["Aggregation Radio"] == "Year")
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
