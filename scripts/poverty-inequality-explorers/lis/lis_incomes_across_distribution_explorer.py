# %% [markdown]
# # Incomes Across the Distribution Explorer of the Luxembourg Income Study
# This code creates the tsv file for the incomes across the distribution explorer from the LIS data, available [here](https://owid.cloud/admin/explorers/preview/lis-incomes-across-distribution)

import textwrap
from pathlib import Path

import numpy as np

# %%
import pandas as pd

PARENT_DIR = Path(__file__).parent.parent.parent.parent.absolute()
outfile = PARENT_DIR / "explorers" / "lis-incomes-across-distribution.explorer.tsv"

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

# Tables sheet
sheet_name = "tables"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
tables = pd.read_csv(url, keep_default_na=False)

# Deciles9 sheet (needed to handle thresholds data)
sheet_name = "deciles9"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
deciles9 = pd.read_csv(url, keep_default_na=False)

# Deciles10 sheet (needed to handle average and share data)
sheet_name = "deciles10"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
deciles10 = pd.read_csv(url, keep_default_na=False)

# Top sheet (needed to handle data at the top of the distribution)
sheet_name = "top_pct"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
top_pct = pd.read_csv(url, keep_default_na=False)

# Income aggregation sheet (day, month, year)
sheet_name = "income_aggregation"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
income_aggregation = pd.read_csv(
    url, keep_default_na=False, dtype={"multiplier": "str"}
)

# %% [markdown]
# ## Header
# General settings of the explorer are defined here, like the title, subtitle, default country selection, publishing status and others.

# %%
# The header is defined as a dictionary first and then it is converted into a index-oriented dataframe
header_dict = {
    "explorerTitle": "Incomes Across the Distribution Data Explorer: Luxembourg Income Study data",
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
    "wpBlockId": "57755",
    "entityType": "country or region",
    "pickerColumnSlugs": "mean_mi_eq_year median_mi_eq_year mean_dhi_eq_year median_dhi_eq_year",
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
dataPublishedBy = "Luxembourg Income Study (LIS) Database, http://www.lisdatacenter.org (multiple countries; 1967-2021). Luxembourg, LIS."
sourceLink = "https://www.lisdatacenter.org/our-data/lis-database/"
colorScaleNumericMinValue = 0
tolerance = 5
colorScaleEqualSizeBins = "true"
new_line = "<br><br>"

notes_title = "NOTES ON HOW WE PROCESSED THIS INDICATOR"

processing_description = new_line.join(
    [
        "The Luxembourg Income Study data is created from standardized household survey microdata available in their <a href='https://www.lisdatacenter.org/data-access/lissy/'>LISSY platform</a>. The estimations follow the methodology available in LIS, Key Figures and DART platform.",
        "After tax income is obtained by using the disposable household income variable (dhi)",
        "Before tax income is estimated by calculating the sum of income from labor and capital (variable hifactor), cash transfers and in-kind goods and services from privates (hiprivate) and private pensions (hi33). This is done only for surveys where tax and contributions are fully captured, collected or imputed.",
        "Income data is converted from local currency into international-$ by dividing by the <a href='https://www.lisdatacenter.org/resources/ppp-deflators/'>LIS PPP factor</a>, available as an additional database in the system.",
        "Incomes are top and bottom-coded by replacing negative values with zeros and setting boundaries for extreme values of log income: at the top Q3 plus 3 times the interquartile range (Q3-Q1), and at the bottom Q1 minus 3 times the interquartile range.",
        "Incomes are equivalized by dividing each household observation by the square root of the number of household members (nhhmem). Per capita estimates are calculated by dividing incomes by the number of household members.",
    ]
)

processing_poverty = "Poverty indicators are obtained by using <a href='https://ideas.repec.org/c/boc/bocode/s366004.html'>Stata’s povdeco function</a>. Weights are set as the product between the number of household members (nhhmem) and the normalized household weight (hwgt). The function generates FGT(0) and FGT(1), headcount ratio and poverty gap index. After extraction, further data processing steps are done to estimate other poverty indicators using these values, population and poverty lines for absolute and relative poverty."
processing_gini_mean_median = "Gini coefficients are obtained by using <a href='https://ideas.repec.org/c/boc/bocode/s366007.html'>Stata’s ineqdec0 function</a>. Weights are set as the product between the number of household members (nhhmem) and the normalized household weight (hwgt). From this function, mean and median values are also calculated."
processing_distribution = "Income shares and thresholds by decile are obtained by using <a href='https://ideas.repec.org/c/boc/bocode/s366005.html'>Stata’s sumdist function</a>. The parameters set are again the weight (nhhmem*hwgt) and the number of quantile groups (10). Threshold ratios, share ratios and averages by decile are estimated after the use of LISSY with this data."

ppp_description = "The data is measured in international-$ at 2017 prices – this adjusts for inflation and for differences in the cost of living between countries."

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
            # I need the original variables to not break the aggregations
            # Mean
            df_tables.loc[
                j, "name"
            ] = f"Mean {welfare['welfare_type'][wel]} ({welfare['title'][wel]})"
            df_tables.loc[
                j, "slug"
            ] = f"mean_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_tables.loc[j, "description"] = new_line.join(
                [
                    f"Mean {welfare['welfare_type'][wel]}.",
                    welfare["description"][wel],
                    equivalence_scales["description"][eq],
                    ppp_description,
                    notes_title,
                    processing_description,
                    processing_gini_mean_median,
                ]
            )
            df_tables.loc[j, "unit"] = "international-$ in 2017 prices"
            df_tables.loc[j, "shortUnit"] = "$"
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_mean"][wel]
            df_tables.loc[j, "colorScaleScheme"] = "BuGn"
            j += 1

            # Median
            df_tables.loc[
                j, "name"
            ] = f"Median {welfare['welfare_type'][wel]} ({welfare['title'][wel]})"
            df_tables.loc[
                j, "slug"
            ] = f"median_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_tables.loc[j, "description"] = new_line.join(
                [
                    f"The level of {welfare['welfare_type'][wel]} below which half of the population live.",
                    welfare["description"][wel],
                    equivalence_scales["description"][eq],
                    ppp_description,
                    notes_title,
                    processing_description,
                    processing_gini_mean_median,
                ]
            )
            df_tables.loc[j, "unit"] = "international-$ in 2017 prices"
            df_tables.loc[j, "shortUnit"] = "$"
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_median"][wel]
            df_tables.loc[j, "colorScaleScheme"] = "Blues"
            j += 1

            # Thresholds - Deciles
            for dec9 in range(len(deciles9)):
                df_tables.loc[
                    j, "name"
                ] = f"{deciles9['ordinal'][dec9].capitalize()} ({welfare['title'][wel]})"
                df_tables.loc[
                    j, "slug"
                ] = f"thr_{deciles9['lis_notation'][dec9]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
                df_tables.loc[j, "description"] = new_line.join(
                    [
                        f"The level of {welfare['welfare_type'][wel]} below which {deciles9['decile'][dec9]}0% of the population falls.",
                        welfare["description"][wel],
                        equivalence_scales["description"][eq],
                        ppp_description,
                        notes_title,
                        processing_description,
                        processing_distribution,
                    ]
                )
                df_tables.loc[j, "unit"] = "international-$ in 2017 prices"
                df_tables.loc[j, "shortUnit"] = "$"
                df_tables.loc[j, "type"] = "Numeric"
                # df_tables.loc[j, "colorScaleNumericBins"] = deciles9["scale_thr"][dec9]
                df_tables.loc[j, "colorScaleScheme"] = "Purples"
                j += 1

            # Averages - Deciles
            for dec10 in range(len(deciles10)):
                df_tables.loc[
                    j, "name"
                ] = f"{deciles10['ordinal'][dec10].capitalize()} ({welfare['title'][wel]})"
                df_tables.loc[
                    j, "slug"
                ] = f"avg_{deciles10['lis_notation'][dec10]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
                df_tables.loc[j, "description"] = new_line.join(
                    [
                        f"The mean {welfare['welfare_type'][wel]} within the {deciles10['ordinal'][dec10]} (tenth of the population).",
                        welfare["description"][wel],
                        equivalence_scales["description"][eq],
                        ppp_description,
                        notes_title,
                        processing_description,
                        processing_distribution,
                    ]
                )
                df_tables.loc[j, "unit"] = "international-$ in 2017 prices"
                df_tables.loc[j, "shortUnit"] = "$"
                df_tables.loc[j, "type"] = "Numeric"
                # df_tables.loc[j, "colorScaleNumericBins"] = deciles10["scale_avg"][
                #     dec10
                # ]
                df_tables.loc[j, "colorScaleScheme"] = "Greens"
                j += 1

            # Shares - Deciles
            for dec10 in range(len(deciles10)):
                df_tables.loc[
                    j, "name"
                ] = f"{deciles10['ordinal'][dec10].capitalize()} ({welfare['title'][wel]})"
                df_tables.loc[
                    j, "slug"
                ] = f"share_{deciles10['lis_notation'][dec10]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
                df_tables.loc[j, "description"] = new_line.join(
                    [
                        f"The share of {welfare['welfare_type'][wel]} received by the {deciles10['ordinal'][dec10]} (tenth of the population).",
                        welfare["description"][wel],
                        equivalence_scales["description"][eq],
                        notes_title,
                        processing_description,
                        processing_distribution,
                    ]
                )
                df_tables.loc[j, "unit"] = "%"
                df_tables.loc[j, "shortUnit"] = "%"
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[j, "colorScaleNumericBins"] = deciles10[
                    f"scale_share_{welfare['slug'][wel]}"
                ][dec10]
                df_tables.loc[j, "colorScaleScheme"] = "OrRd"
                j += 1

            # Income aggregations
            for agg in range(len(income_aggregation)):
                # Mean
                df_tables.loc[
                    j, "name"
                ] = f"Mean {welfare['welfare_type'][wel]} ({welfare['title'][wel]})"
                df_tables.loc[
                    j, "slug"
                ] = f"mean_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]}"
                df_tables.loc[j, "description"] = new_line.join(
                    [
                        f"Mean {welfare['welfare_type'][wel]}.",
                        welfare["description"][wel],
                        equivalence_scales["description"][eq],
                        ppp_description,
                        notes_title,
                        processing_description,
                        processing_gini_mean_median,
                    ]
                )
                df_tables.loc[j, "unit"] = "international-$ in 2017 prices"
                df_tables.loc[j, "shortUnit"] = "$"
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[j, "colorScaleNumericBins"] = income_aggregation["scale"][
                    agg
                ]
                df_tables.loc[j, "colorScaleScheme"] = "BuGn"
                df_tables.loc[
                    j, "transform"
                ] = f"multiplyBy mean_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]} {income_aggregation['multiplier'][agg]}"
                j += 1

                # Median
                df_tables.loc[
                    j, "name"
                ] = f"Median {welfare['welfare_type'][wel]} ({welfare['title'][wel]})"
                df_tables.loc[
                    j, "slug"
                ] = f"median_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]}"
                df_tables.loc[j, "description"] = new_line.join(
                    [
                        f"The level of {welfare['welfare_type'][wel]} below which half of the population live.",
                        welfare["description"][wel],
                        equivalence_scales["description"][eq],
                        ppp_description,
                        notes_title,
                        processing_description,
                        processing_gini_mean_median,
                    ]
                )
                df_tables.loc[j, "unit"] = "international-$ in 2017 prices"
                df_tables.loc[j, "shortUnit"] = "$"
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[j, "colorScaleNumericBins"] = income_aggregation["scale"][
                    agg
                ]
                df_tables.loc[j, "colorScaleScheme"] = "Blues"
                df_tables.loc[
                    j, "transform"
                ] = f"multiplyBy median_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]} {income_aggregation['multiplier'][agg]}"
                j += 1

                # Thresholds - Deciles
                for dec9 in range(len(deciles9)):
                    df_tables.loc[
                        j, "name"
                    ] = f"{deciles9['ordinal'][dec9].capitalize()} ({welfare['title'][wel]})"
                    df_tables.loc[
                        j, "slug"
                    ] = f"thr_{deciles9['lis_notation'][dec9]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]}"
                    df_tables.loc[j, "description"] = new_line.join(
                        [
                            f"The level of {welfare['welfare_type'][wel]} below which {deciles9['decile'][dec9]}0% of the population falls.",
                            welfare["description"][wel],
                            equivalence_scales["description"][eq],
                            ppp_description,
                            notes_title,
                            processing_description,
                            processing_distribution,
                        ]
                    )
                    df_tables.loc[j, "unit"] = "international-$ in 2017 prices"
                    df_tables.loc[j, "shortUnit"] = "$"
                    df_tables.loc[j, "type"] = "Numeric"
                    df_tables.loc[j, "colorScaleNumericBins"] = deciles9[
                        f"scale_thr_{welfare['slug'][wel]}_{income_aggregation['aggregation'][agg]}"
                    ][dec9]
                    df_tables.loc[j, "colorScaleScheme"] = "Purples"
                    df_tables.loc[
                        j, "transform"
                    ] = f"multiplyBy thr_{deciles9['lis_notation'][dec9]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]} {income_aggregation['multiplier'][agg]}"
                    j += 1

                # Averages - Deciles
                for dec10 in range(len(deciles10)):
                    df_tables.loc[
                        j, "name"
                    ] = f"{deciles10['ordinal'][dec10].capitalize()} ({welfare['title'][wel]})"
                    df_tables.loc[
                        j, "slug"
                    ] = f"avg_{deciles10['lis_notation'][dec10]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]}"
                    df_tables.loc[j, "description"] = new_line.join(
                        [
                            f"The mean {welfare['welfare_type'][wel]} within the {deciles10['ordinal'][dec10]} (tenth of the population).",
                            welfare["description"][wel],
                            equivalence_scales["description"][eq],
                            ppp_description,
                            notes_title,
                            processing_description,
                            processing_distribution,
                        ]
                    )
                    df_tables.loc[j, "unit"] = "international-$ in 2017 prices"
                    df_tables.loc[j, "shortUnit"] = "$"
                    df_tables.loc[j, "type"] = "Numeric"
                    df_tables.loc[j, "colorScaleNumericBins"] = deciles10[
                        f"scale_avg_{welfare['slug'][wel]}_{income_aggregation['aggregation'][agg]}"
                    ][dec10]
                    df_tables.loc[j, "colorScaleScheme"] = "Greens"
                    df_tables.loc[
                        j, "transform"
                    ] = f"multiplyBy avg_{deciles10['lis_notation'][dec10]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]} {income_aggregation['multiplier'][agg]}"
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
    for agg in range(len(income_aggregation)):
        for eq in range(len(equivalence_scales)):
            for wel in range(len(welfare)):
                # Mean
                df_graphers.loc[
                    j, "title"
                ] = f"Mean {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} ({welfare['title'][wel]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"mean_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]}"
                df_graphers.loc[j, "Indicator Dropdown"] = "Mean income"
                df_graphers.loc[j, "Decile Dropdown"] = np.nan
                df_graphers.loc[
                    j, "Income measure Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[
                    j, "Period Radio"
                ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
                df_graphers.loc[
                    j,
                    "Adjust for cost sharing within households (equivalized income) Checkbox",
                ] = equivalence_scales["checkbox"][eq]
                df_graphers.loc[
                    j, "subtitle"
                ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2017 prices. {equivalence_scales['note'][eq]}"
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                df_graphers.loc[j, "yScaleToggle"] = "true"
                j += 1

                # Median
                df_graphers.loc[
                    j, "title"
                ] = f"Median {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} ({welfare['title'][wel]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"median_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]}"
                df_graphers.loc[j, "Indicator Dropdown"] = "Median income"
                df_graphers.loc[j, "Decile Dropdown"] = np.nan
                df_graphers.loc[
                    j, "Income measure Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[
                    j, "Period Radio"
                ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
                df_graphers.loc[
                    j,
                    "Adjust for cost sharing within households (equivalized income) Checkbox",
                ] = equivalence_scales["checkbox"][eq]
                df_graphers.loc[
                    j, "subtitle"
                ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2017 prices. {equivalence_scales['note'][eq]}"
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                df_graphers.loc[j, "yScaleToggle"] = "true"
                j += 1

                # Thresholds - Deciles
                for dec9 in range(len(deciles9)):
                    df_graphers.loc[
                        j, "title"
                    ] = f"Threshold {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} marking the {deciles9['ordinal'][dec9]} ({welfare['title'][wel]})"
                    df_graphers.loc[
                        j, "ySlugs"
                    ] = f"thr_{deciles9['lis_notation'][dec9]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]}"
                    df_graphers.loc[j, "Indicator Dropdown"] = "Decile thresholds"
                    df_graphers.loc[j, "Decile Dropdown"] = deciles9["dropdown"][dec9]
                    df_graphers.loc[
                        j, "Income measure Dropdown"
                    ] = f"{welfare['dropdown_option'][wel]}"
                    df_graphers.loc[
                        j, "Period Radio"
                    ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
                    df_graphers.loc[
                        j,
                        "Adjust for cost sharing within households (equivalized income) Checkbox",
                    ] = equivalence_scales["checkbox"][eq]
                    df_graphers.loc[
                        j, "subtitle"
                    ] = f"The level of {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} below which {deciles9['decile'][dec9]}0% of the population falls. {welfare['subtitle'][wel]}"
                    df_graphers.loc[
                        j, "note"
                    ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. {equivalence_scales['note'][eq]}"
                    df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                    df_graphers.loc[j, "hasMapTab"] = "true"
                    df_graphers.loc[j, "tab"] = "map"
                    df_graphers.loc[j, "yScaleToggle"] = "true"
                    j += 1

                # Averages - Deciles
                for dec10 in range(len(deciles10)):
                    df_graphers.loc[
                        j, "title"
                    ] = f"Mean {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} within the {deciles10['ordinal'][dec10]} ({welfare['title'][wel]})"
                    df_graphers.loc[
                        j, "ySlugs"
                    ] = f"avg_{deciles10['lis_notation'][dec10]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]}"
                    df_graphers.loc[j, "Indicator Dropdown"] = "Mean income, by decile"
                    df_graphers.loc[j, "Decile Dropdown"] = deciles10["dropdown"][dec10]
                    df_graphers.loc[
                        j, "Income measure Dropdown"
                    ] = f"{welfare['dropdown_option'][wel]}"
                    df_graphers.loc[
                        j, "Period Radio"
                    ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
                    df_graphers.loc[
                        j,
                        "Adjust for cost sharing within households (equivalized income) Checkbox",
                    ] = equivalence_scales["checkbox"][eq]
                    df_graphers.loc[
                        j, "subtitle"
                    ] = f"The mean {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} within the {deciles10['ordinal'][dec10]} (tenth of the population). {welfare['subtitle'][wel]}"
                    df_graphers.loc[
                        j, "note"
                    ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. {equivalence_scales['note'][eq]}"
                    df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                    df_graphers.loc[j, "hasMapTab"] = "true"
                    df_graphers.loc[j, "tab"] = "map"
                    df_graphers.loc[j, "yScaleToggle"] = "true"
                    j += 1

                # Thresholds - Multiple deciles
                df_graphers.loc[
                    j, "title"
                ] = f"Threshold {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} for each decile ({welfare['title'][wel]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"thr_p10_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} thr_p20_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} thr_p30_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} thr_p40_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} thr_p50_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} thr_p60_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} thr_p70_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} thr_p80_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} thr_p90_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]}"
                df_graphers.loc[j, "Indicator Dropdown"] = "Decile thresholds"
                df_graphers.loc[j, "Decile Dropdown"] = "All deciles"
                df_graphers.loc[
                    j, "Income measure Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[
                    j, "Period Radio"
                ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
                df_graphers.loc[
                    j,
                    "Adjust for cost sharing within households (equivalized income) Checkbox",
                ] = equivalence_scales["checkbox"][eq]
                df_graphers.loc[j, "hideRelativeToggle"] = "false"
                df_graphers.loc[
                    j, "subtitle"
                ] = f"The level of income per {income_aggregation['aggregation'][agg]} below which 10%, 20%, 30%, etc. of the population falls. {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. {equivalence_scales['note'][eq]}"
                df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
                df_graphers.loc[j, "hasMapTab"] = "false"
                df_graphers.loc[j, "tab"] = "chart"
                df_graphers.loc[j, "yScaleToggle"] = "true"
                j += 1

                # Averages - Multiple deciles
                df_graphers.loc[
                    j, "title"
                ] = f"Mean {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} within each decile ({welfare['title'][wel]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"avg_p10_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} avg_p20_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} avg_p30_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} avg_p40_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} avg_p50_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} avg_p60_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} avg_p70_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} avg_p80_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} avg_p90_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} avg_p100_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]}"
                df_graphers.loc[j, "Indicator Dropdown"] = "Mean income, by decile"
                df_graphers.loc[j, "Decile Dropdown"] = "All deciles"
                df_graphers.loc[
                    j, "Income measure Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[
                    j, "Period Radio"
                ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
                df_graphers.loc[
                    j,
                    "Adjust for cost sharing within households (equivalized income) Checkbox",
                ] = equivalence_scales["checkbox"][eq]
                df_graphers.loc[j, "hideRelativeToggle"] = "false"
                df_graphers.loc[
                    j, "subtitle"
                ] = f"The mean {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} within each decile (tenth of the population). {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. {equivalence_scales['note'][eq]}"
                df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
                df_graphers.loc[j, "hasMapTab"] = "false"
                df_graphers.loc[j, "tab"] = "chart"
                df_graphers.loc[j, "yScaleToggle"] = "true"
                j += 1

            # BEFORE VS. AFTER TAX
            # Mean
            df_graphers.loc[
                j, "title"
            ] = f"Mean income per {income_aggregation['aggregation'][agg]} (after tax vs. before tax)"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"mean_mi_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} mean_dhi_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]}"
            df_graphers.loc[j, "Indicator Dropdown"] = "Mean income"
            df_graphers.loc[j, "Decile Dropdown"] = np.nan
            df_graphers.loc[j, "Income measure Dropdown"] = "After tax vs. before tax"
            df_graphers.loc[
                j, "Period Radio"
            ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
            df_graphers.loc[
                j,
                "Adjust for cost sharing within households (equivalized income) Checkbox",
            ] = equivalence_scales["checkbox"][eq]
            df_graphers.loc[
                j, "subtitle"
            ] = f"This data is adjusted for inflation and for differences in the cost of living between countries."
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2017 prices. {equivalence_scales['note'][eq]}"
            df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
            df_graphers.loc[j, "hasMapTab"] = "false"
            df_graphers.loc[j, "tab"] = "chart"
            df_graphers.loc[j, "yScaleToggle"] = "true"
            j += 1

            # Median
            df_graphers.loc[
                j, "title"
            ] = f"Median income per {income_aggregation['aggregation'][agg]} (after tax vs. before tax)"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"median_mi_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} median_dhi_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]}"
            df_graphers.loc[j, "Indicator Dropdown"] = "Median income"
            df_graphers.loc[j, "Decile Dropdown"] = np.nan
            df_graphers.loc[j, "Income measure Dropdown"] = "After tax vs. before tax"
            df_graphers.loc[
                j, "Period Radio"
            ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
            df_graphers.loc[
                j,
                "Adjust for cost sharing within households (equivalized income) Checkbox",
            ] = equivalence_scales["checkbox"][eq]
            df_graphers.loc[
                j, "subtitle"
            ] = f"This data is adjusted for inflation and for differences in the cost of living between countries."
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2017 prices. {equivalence_scales['note'][eq]}"
            df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
            df_graphers.loc[j, "hasMapTab"] = "false"
            df_graphers.loc[j, "tab"] = "chart"
            df_graphers.loc[j, "yScaleToggle"] = "true"
            j += 1

            # Thresholds - Deciles
            for dec9 in range(len(deciles9)):
                df_graphers.loc[
                    j, "title"
                ] = f"Threshold income per {income_aggregation['aggregation'][agg]} marking the {deciles9['ordinal'][dec9]} (after tax vs. before tax)"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"thr_{deciles9['lis_notation'][dec9]}_mi_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} thr_{deciles9['lis_notation'][dec9]}_dhi_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]}"
                df_graphers.loc[j, "Indicator Dropdown"] = "Decile thresholds"
                df_graphers.loc[j, "Decile Dropdown"] = deciles9["dropdown"][dec9]
                df_graphers.loc[
                    j, "Income measure Dropdown"
                ] = "After tax vs. before tax"
                df_graphers.loc[
                    j, "Period Radio"
                ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
                df_graphers.loc[
                    j,
                    "Adjust for cost sharing within households (equivalized income) Checkbox",
                ] = equivalence_scales["checkbox"][eq]
                df_graphers.loc[
                    j, "subtitle"
                ] = f"The level of income per {income_aggregation['aggregation'][agg]} below which {deciles9['decile'][dec9]}0% of the population falls."
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. {equivalence_scales['note'][eq]}"
                df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
                df_graphers.loc[j, "hasMapTab"] = "false"
                df_graphers.loc[j, "tab"] = "chart"
                df_graphers.loc[j, "yScaleToggle"] = "true"
                j += 1

            # Averages - Deciles
            for dec10 in range(len(deciles10)):
                df_graphers.loc[
                    j, "title"
                ] = f"Mean income per {income_aggregation['aggregation'][agg]} within the {deciles10['ordinal'][dec10]} (after tax vs. before tax)"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"avg_{deciles10['lis_notation'][dec10]}_mi_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]} avg_{deciles10['lis_notation'][dec10]}_dhi_{equivalence_scales['slug'][eq]}{income_aggregation['slug_suffix'][agg]}"
                df_graphers.loc[j, "Indicator Dropdown"] = "Mean income, by decile"
                df_graphers.loc[j, "Decile Dropdown"] = deciles10["dropdown"][dec10]
                df_graphers.loc[
                    j, "Income measure Dropdown"
                ] = "After tax vs. before tax"
                df_graphers.loc[
                    j, "Period Radio"
                ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
                df_graphers.loc[
                    j,
                    "Adjust for cost sharing within households (equivalized income) Checkbox",
                ] = equivalence_scales["checkbox"][eq]
                df_graphers.loc[
                    j, "subtitle"
                ] = f"The mean income per {income_aggregation['aggregation'][agg]} within the {deciles10['ordinal'][dec10]} (tenth of the population)."
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. {equivalence_scales['note'][eq]}"
                df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
                df_graphers.loc[j, "hasMapTab"] = "false"
                df_graphers.loc[j, "tab"] = "chart"
                df_graphers.loc[j, "yScaleToggle"] = "true"
                j += 1

                # # Compare equivalence scales
                # # Mean
                # df_graphers.loc[
                #     j, "title"
                # ] = f"Mean {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} ({welfare['title'][wel]}, equivalized vs. per capita)"
                # df_graphers.loc[
                #     j, "ySlugs"
                # ] = f"mean_{welfare['slug'][wel]}_eq{income_aggregation['slug_suffix'][agg]} mean_{welfare['slug'][wel]}_pc{income_aggregation['slug_suffix'][agg]}"
                # df_graphers.loc[j, "Indicator Dropdown"] = "Mean income"
                # df_graphers.loc[j, "Decile Dropdown"] = np.nan
                # df_graphers.loc[
                #     j, "Income measure Dropdown"
                # ] = f"{welfare['dropdown_option'][wel]}"
                # df_graphers.loc[
                #     j, "Period Radio"
                # ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
                # df_graphers.loc[
                #     j, "Equivalence scale Dropdown"
                # ] = "Equivalized vs. per capita"
                # df_graphers.loc[j, "Relative change Checkbox"] = relative_toggle[
                #     "checkbox"
                # ][rel_toggle]
                # df_graphers.loc[j, "stackMode"] = relative_toggle["stack_mode"][
                #     rel_toggle
                # ]
                # df_graphers.loc[
                #     j, "subtitle"
                # ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. {welfare['subtitle'][wel]}"
                # df_graphers.loc[
                #     j, "note"
                # ] = f"This data is measured in international-$ at 2017 prices."
                # df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
                # df_graphers.loc[j, "hasMapTab"] = "false"
                # df_graphers.loc[j, "tab"] = "chart"
                # df_graphers.loc[j, "yScaleToggle"] = "true"
                # j += 1

                # # Median
                # df_graphers.loc[
                #     j, "title"
                # ] = f"Median {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} ({welfare['title'][wel]}, equivalized vs. per capita)"
                # df_graphers.loc[
                #     j, "ySlugs"
                # ] = f"median_{welfare['slug'][wel]}_eq{income_aggregation['slug_suffix'][agg]} median_{welfare['slug'][wel]}_pc{income_aggregation['slug_suffix'][agg]}"
                # df_graphers.loc[
                #     j, "Indicator Dropdown"
                # ] = "Median income"
                # df_graphers.loc[j, "Decile Dropdown"] = np.nan
                # df_graphers.loc[
                #     j, "Income measure Dropdown"
                # ] = f"{welfare['dropdown_option'][wel]}"
                # df_graphers.loc[
                #     j, "Period Radio"
                # ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
                # df_graphers.loc[
                #     j, "Equivalence scale Dropdown"
                # ] = "Equivalized vs. per capita"
                # df_graphers.loc[j, "Relative change Checkbox"] = relative_toggle[
                #     "checkbox"
                # ][rel_toggle]
                # df_graphers.loc[j, "stackMode"] = relative_toggle["stack_mode"][
                #     rel_toggle
                # ]
                # df_graphers.loc[
                #     j, "subtitle"
                # ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. {welfare['subtitle'][wel]}"
                # df_graphers.loc[
                #     j, "note"
                # ] = f"This data is measured in international-$ at 2017 prices."
                # df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
                # df_graphers.loc[j, "hasMapTab"] = "false"
                # df_graphers.loc[j, "tab"] = "chart"
                # df_graphers.loc[j, "yScaleToggle"] = "true"
                # j += 1

                # # Thresholds - Deciles
                # for dec9 in range(len(deciles9)):
                #     df_graphers.loc[
                #         j, "title"
                #     ] = f"Threshold {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} marking the {deciles9['ordinal'][dec9]} ({welfare['title'][wel]}, equivalized vs. per capita)"
                #     df_graphers.loc[
                #         j, "ySlugs"
                #     ] = f"thr_{deciles9['lis_notation'][dec9]}_{welfare['slug'][wel]}_eq{income_aggregation['slug_suffix'][agg]} thr_{deciles9['lis_notation'][dec9]}_{welfare['slug'][wel]}_pc{income_aggregation['slug_suffix'][agg]}"
                #     df_graphers.loc[j, "Indicator Dropdown"] = "Decile thresholds"
                #     df_graphers.loc[j, "Decile Dropdown"] = deciles9["dropdown"][
                #         dec9
                #     ]
                #     df_graphers.loc[
                #         j, "Income measure Dropdown"
                #     ] = f"{welfare['dropdown_option'][wel]}"
                #     df_graphers.loc[
                #         j, "Period Radio"
                #     ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
                #     df_graphers.loc[
                #         j, "Equivalence scale Dropdown"
                #     ] = "Equivalized vs. per capita"
                #     df_graphers.loc[
                #         j, "Relative change Checkbox"
                #     ] = relative_toggle["checkbox"][rel_toggle]
                #     df_graphers.loc[j, "stackMode"] = relative_toggle["stack_mode"][
                #         rel_toggle
                #     ]
                #     df_graphers.loc[
                #         j, "subtitle"
                #     ] = f"This is the level of {welfare['welfare_type'][wel]} below which {deciles9['decile'][dec9]}0% of the population falls. {welfare['subtitle'][wel]}"
                #     df_graphers.loc[
                #         j, "note"
                #     ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries."
                #     df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
                #     df_graphers.loc[j, "hasMapTab"] = "false"
                #     df_graphers.loc[j, "tab"] = "chart"
                #     df_graphers.loc[j, "yScaleToggle"] = "true"
                #     j += 1

                # # Averages - Deciles
                # for dec10 in range(len(deciles10)):
                #     df_graphers.loc[
                #         j, "title"
                #     ] = f"Mean {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} within the {deciles10['ordinal'][dec10]} ({welfare['title'][wel]}, equivalized vs. per capita)"
                #     df_graphers.loc[
                #         j, "ySlugs"
                #     ] = f"avg_{deciles10['lis_notation'][dec10]}_{welfare['slug'][wel]}_eq{income_aggregation['slug_suffix'][agg]} avg_{deciles10['lis_notation'][dec10]}_{welfare['slug'][wel]}_pc{income_aggregation['slug_suffix'][agg]}"
                #     df_graphers.loc[
                #         j, "Indicator Dropdown"
                #     ] = "Mean income, by decile"
                #     df_graphers.loc[j, "Decile Dropdown"] = deciles10["dropdown"][
                #         dec10
                #     ]
                #     df_graphers.loc[
                #         j, "Income measure Dropdown"
                #     ] = f"{welfare['dropdown_option'][wel]}"
                #     df_graphers.loc[
                #         j, "Period Radio"
                #     ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
                #     df_graphers.loc[
                #         j, "Equivalence scale Dropdown"
                #     ] = "Equivalized vs. per capita"
                #     df_graphers.loc[
                #         j, "Relative change Checkbox"
                #     ] = relative_toggle["checkbox"][rel_toggle]
                #     df_graphers.loc[j, "stackMode"] = relative_toggle["stack_mode"][
                #         rel_toggle
                #     ]
                #     df_graphers.loc[
                #         j, "subtitle"
                #     ] = f"This is the mean {welfare['welfare_type'][wel]} within the {deciles10['ordinal'][dec10]} (tenth of the population). {welfare['subtitle'][wel]}"
                #     df_graphers.loc[
                #         j, "note"
                #     ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries."
                #     df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
                #     df_graphers.loc[j, "hasMapTab"] = "false"
                #     df_graphers.loc[j, "tab"] = "chart"
                #     df_graphers.loc[j, "yScaleToggle"] = "true"
                #     j += 1

    # This is an adaptation of the code to make both before and after tax graphs and share graphs
    for eq in range(len(equivalence_scales)):
        for wel in range(len(welfare)):
            # Shares - Deciles
            for dec10 in range(len(deciles10)):
                df_graphers.loc[
                    j, "title"
                ] = f"{welfare['welfare_type'][wel].capitalize()} share of the {deciles10['ordinal'][dec10]} ({welfare['title'][wel]})"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"share_{deciles10['lis_notation'][dec10]}_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
                df_graphers.loc[j, "Indicator Dropdown"] = "Decile shares"
                df_graphers.loc[j, "Decile Dropdown"] = deciles10["dropdown"][dec10]
                df_graphers.loc[
                    j, "Income measure Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Period Radio"] = np.nan
                df_graphers.loc[
                    j,
                    "Adjust for cost sharing within households (equivalized income) Checkbox",
                ] = equivalence_scales["checkbox"][eq]
                df_graphers.loc[
                    j, "subtitle"
                ] = f"The share of {welfare['welfare_type'][wel]} received by the {deciles10['ordinal'][dec10]} (tenth of the population). {welfare['subtitle'][wel]}"
                df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                j += 1

            # Shares - Multiple deciles
            df_graphers.loc[
                j, "title"
            ] = f"{welfare['welfare_type'][wel].capitalize()} share for each decile ({welfare['title'][wel]})"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"share_p10_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]} share_p20_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]} share_p30_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]} share_p40_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]} share_p50_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]} share_p60_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]} share_p70_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]} share_p80_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]} share_p90_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]} share_p100_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_graphers.loc[j, "Indicator Dropdown"] = "Decile shares"
            df_graphers.loc[j, "Decile Dropdown"] = "All deciles"
            df_graphers.loc[
                j, "Income measure Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[j, "Period Radio"] = np.nan
            df_graphers.loc[
                j,
                "Adjust for cost sharing within households (equivalized income) Checkbox",
            ] = equivalence_scales["checkbox"][eq]
            df_graphers.loc[
                j, "subtitle"
            ] = f"The share of {welfare['welfare_type'][wel]} received by each decile (tenth of the population). {welfare['subtitle'][wel]}"
            df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
            df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
            df_graphers.loc[j, "hasMapTab"] = "false"
            df_graphers.loc[j, "tab"] = "chart"
            j += 1

        # BEFORE VS. AFTER TAX
        # Shares - Deciles
        for dec10 in range(len(deciles10)):
            df_graphers.loc[
                j, "title"
            ] = f"Income share of the {deciles10['ordinal'][dec10]} (after tax vs. before tax)"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"share_{deciles10['lis_notation'][dec10]}_mi_{equivalence_scales['slug'][eq]} share_{deciles10['lis_notation'][dec10]}_dhi_{equivalence_scales['slug'][eq]}"
            df_graphers.loc[j, "Indicator Dropdown"] = "Decile shares"
            df_graphers.loc[j, "Decile Dropdown"] = deciles10["dropdown"][dec10]
            df_graphers.loc[j, "Income measure Dropdown"] = "After tax vs. before tax"
            df_graphers.loc[j, "Period Radio"] = np.nan
            df_graphers.loc[
                j,
                "Adjust for cost sharing within households (equivalized income) Checkbox",
            ] = equivalence_scales["checkbox"][eq]
            df_graphers.loc[
                j, "subtitle"
            ] = f"The share of income received by the {deciles10['ordinal'][dec10]} (tenth of the population)."
            df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
            df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
            df_graphers.loc[j, "hasMapTab"] = "false"
            df_graphers.loc[j, "tab"] = "chart"
            j += 1

            # # Compare equivalence scales (without relative change)
            # # Shares - Deciles
            # for dec10 in range(len(deciles10)):
            #     df_graphers.loc[
            #         j, "title"
            #     ] = f"{welfare['welfare_type'][wel].capitalize()} share of the {deciles10['ordinal'][dec10]} ({welfare['title'][wel]}, equivalized vs. per capita)"
            #     df_graphers.loc[
            #         j, "ySlugs"
            #     ] = f"share_{deciles10['lis_notation'][dec10]}_{welfare['slug'][wel]}_eq share_{deciles10['lis_notation'][dec10]}_{welfare['slug'][wel]}_pc"
            #     df_graphers.loc[j, "Indicator Dropdown"] = "Decile shares"
            #     df_graphers.loc[j, "Decile Dropdown"] = deciles10["dropdown"][dec10]
            #     df_graphers.loc[
            #         j, "Income measure Dropdown"
            #     ] = f"{welfare['dropdown_option'][wel]}"
            #     df_graphers.loc[j, "Period Radio"] = np.nan
            #     df_graphers.loc[
            #         j, "Equivalence scale Dropdown"
            #     ] = "Equivalized vs. per capita"
            #     df_graphers.loc[j, "Relative change Checkbox"] = "false"
            #     df_graphers.loc[j, "stackMode"] = "absolute"
            #     df_graphers.loc[
            #         j, "subtitle"
            #     ] = f"This is the {welfare['welfare_type'][wel]} of the {deciles10['ordinal'][dec10]} (tenth of the population) as a share of total {welfare['welfare_type'][wel]}. {welfare['subtitle'][wel]}"
            #     df_graphers.loc[j, "note"] = np.nan
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
    (df_graphers["Indicator Dropdown"] == "Decile thresholds")
    & (df_graphers["Decile Dropdown"] == "All deciles")
    & (df_graphers["Income measure Dropdown"] == "After tax")
    & (df_graphers["Period Radio"] == "Year")
    & (
        df_graphers[
            "Adjust for cost sharing within households (equivalized income) Checkbox"
        ]
        == "false"
    ),
    ["defaultView"],
] = "true"

# Reorder dropdown menus
# Decile/quantile Dropdown
decile_dropdown_list = [
    np.nan,
    "1 (poorest)",
    "2",
    "3",
    "4",
    "5",
    "5 (median)",
    "6",
    "7",
    "8",
    "9",
    "9 (richest)",
    "10 (richest)",
    "All deciles",
]

df_graphers_mapping = pd.DataFrame(
    {
        "decile_dropdown": decile_dropdown_list,
    }
)
df_graphers_mapping = df_graphers_mapping.reset_index().set_index("decile_dropdown")
df_graphers["decile_dropdown_aux"] = df_graphers["Decile Dropdown"].map(
    df_graphers_mapping["index"]
)

# Metric dropdown
metric_dropdown_list = [
    "Mean income",
    "Mean income, by decile",
    "Median income",
    "Decile thresholds",
    "Decile shares",
]

df_graphers_mapping = pd.DataFrame(
    {
        "metric_dropdown": metric_dropdown_list,
    }
)
df_graphers_mapping = df_graphers_mapping.reset_index().set_index("metric_dropdown")
df_graphers["metric_dropdown_aux"] = df_graphers["Indicator Dropdown"].map(
    df_graphers_mapping["index"]
)

# # Equivalence scales dropdown
# eq_dropdown_list = ["Equivalized", "Per capita", "Equivalized vs. per capita"]

# df_graphers_mapping = pd.DataFrame(
#     {
#         "eq_dropdown": eq_dropdown_list,
#     }
# )
# df_graphers_mapping = df_graphers_mapping.reset_index().set_index("eq_dropdown")
# df_graphers["eq_dropdown_aux"] = df_graphers["Equivalence scale Dropdown"].map(
#     df_graphers_mapping["index"]
# )

# Sort by auxiliary variables and drop
df_graphers = df_graphers.sort_values(
    ["decile_dropdown_aux", "metric_dropdown_aux"], ignore_index=True
)
df_graphers = df_graphers.drop(columns=["metric_dropdown_aux", "decile_dropdown_aux"])

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
