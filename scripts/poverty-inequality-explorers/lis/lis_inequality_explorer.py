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
    "explorerTitle": "Inequality Data Explorer: Luxembourg Income Study data",
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
dataPublishedBy = "Luxembourg Income Study (LIS) Database, http://www.lisdatacenter.org (multiple countries; 1967-2021). Luxembourg, LIS."
sourceLink = "https://www.lisdatacenter.org/our-data/lis-database/"
tolerance = 5
colorScaleEqualSizeBins = "true"
new_line = "\\n\\n"

notes_title = "NOTES ON HOW WE PROCESSED THIS INDICATOR"

processing_description = new_line.join(
    [
        "The Luxembourg Income Study data is created from standardized household survey microdata available in their [LISSY platform](https://www.lisdatacenter.org/data-access/lissy/). The estimations follow the methodology available in LIS, Key Figures and DART platform.",
        "After tax income is obtained by using the disposable household income variable (dhi)",
        "Before tax income is estimated by calculating the sum of income from labor and capital (variable hifactor), cash transfers and in-kind goods and services from privates (hiprivate) and private pensions (hi33). This is done only for surveys where tax and contributions are fully captured, collected or imputed.",
        "Income data is converted from local currency into international-$ by dividing by the [LIS PPP factor](https://www.lisdatacenter.org/resources/ppp-deflators/), available as an additional database in the system.",
        "Incomes are top and bottom-coded by replacing negative values with zeros and setting boundaries for extreme values of log income: at the top Q3 plus 3 times the interquartile range (Q3-Q1), and at the bottom Q1 minus 3 times the interquartile range.",
        "Incomes are equivalized by dividing each household observation by the square root of the number of household members (nhhmem). Per capita estimates are calculated by dividing incomes by the number of household members.",
    ]
)

processing_poverty = "Poverty indicators are obtained by using [Stata’s povdeco function](https://ideas.repec.org/c/boc/bocode/s366004.html). Weights are set as the product between the number of household members (nhhmem) and the normalized household weight (hwgt). The function generates FGT(0) and FGT(1), headcount ratio and poverty gap index. After extraction, further data processing steps are done to estimate other poverty indicators using these values, population and poverty lines for absolute and relative poverty."
processing_gini_mean_median = "Gini coefficients are obtained by using [Stata’s ineqdec0 function](https://ideas.repec.org/c/boc/bocode/s366007.html). Weights are set as the product between the number of household members (nhhmem) and the normalized household weight (hwgt). From this function, mean and median values are also calculated."
processing_distribution = "Income shares and thresholds by decile are obtained by using [Stata’s sumdist function](https://ideas.repec.org/c/boc/bocode/s366005.html). The parameters set are again the weight (nhhmem*hwgt) and the number of quantile groups (10). Threshold ratios, share ratios and averages by decile are estimated after the use of LISSY with this data."

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
            # Gini coefficient
            df_tables.loc[j, "name"] = f"Gini coefficient ({welfare['title'][wel]})"
            df_tables.loc[
                j, "slug"
            ] = f"gini_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_tables.loc[j, "description"] = new_line.join(
                [
                    f"The Gini coefficient measures inequality on a scale from 0 to 1. Higher values indicate higher inequality.",
                    welfare["description"][wel],
                    equivalence_scales["description"][eq],
                    notes_title,
                    processing_description,
                    processing_gini_mean_median,
                ]
            )
            df_tables.loc[j, "unit"] = np.nan
            df_tables.loc[j, "shortUnit"] = np.nan
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_gini"][wel]
            df_tables.loc[j, "colorScaleNumericMinValue"] = 1
            df_tables.loc[j, "colorScaleScheme"] = "Oranges"
            j += 1

            # Share of the top 10%
            df_tables.loc[
                j, "name"
            ] = f"{welfare['welfare_type'][wel].capitalize()} share of the richest 10% ({welfare['title'][wel]})"
            df_tables.loc[
                j, "slug"
            ] = f"share_p100_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_tables.loc[j, "description"] = new_line.join(
                [
                    f"The share of {welfare['welfare_type'][wel]} received by the richest 10% of the population.",
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
            df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_top10"][wel]
            df_tables.loc[j, "colorScaleNumericMinValue"] = 100
            df_tables.loc[j, "colorScaleScheme"] = "OrRd"
            j += 1

            # Share of the bottom 50%
            df_tables.loc[
                j, "name"
            ] = f"{welfare['welfare_type'][wel].capitalize()} share of the poorest 50% ({welfare['title'][wel]})"
            df_tables.loc[
                j, "slug"
            ] = f"share_bottom50_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_tables.loc[j, "description"] = new_line.join(
                [
                    f"The share of {welfare['welfare_type'][wel]} received by the poorest 50% of the population.",
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
            df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_bottom50"][wel]
            df_tables.loc[j, "colorScaleNumericMinValue"] = 100
            df_tables.loc[j, "colorScaleScheme"] = "Blues"
            j += 1

            # Palma ratio
            df_tables.loc[j, "name"] = f"Palma ratio ({welfare['title'][wel]})"
            df_tables.loc[
                j, "slug"
            ] = f"palma_ratio_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_tables.loc[j, "description"] = new_line.join(
                [
                    f"The Palma ratio is a measure of inequality that divides the share received by the richest 10% by the share of the poorest 40%. Higher values indicate higher inequality.",
                    welfare["description"][wel],
                    equivalence_scales["description"][eq],
                    notes_title,
                    processing_description,
                    processing_distribution,
                ]
            )
            df_tables.loc[j, "unit"] = np.nan
            df_tables.loc[j, "shortUnit"] = np.nan
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_palma_ratio"][
                wel
            ]
            df_tables.loc[j, "colorScaleNumericMinValue"] = 0
            df_tables.loc[j, "colorScaleScheme"] = "YlOrBr"
            j += 1

            # Headcount ratio (rel)
            df_tables.loc[
                j, "name"
            ] = f"Share in relative poverty ({welfare['title'][wel]})"
            df_tables.loc[
                j, "slug"
            ] = f"headcount_ratio_50_median_{welfare['slug'][wel]}_{equivalence_scales['slug'][eq]}"
            df_tables.loc[j, "description"] = new_line.join(
                [
                    f"The share of the population with {welfare['welfare_type'][wel]} below 50% of the median. Relative poverty reflects the extent of inequality within the bottom of the distribution.",
                    welfare["description"][wel],
                    equivalence_scales["description"][eq],
                    notes_title,
                    processing_description,
                    processing_poverty,
                ]
            )
            df_tables.loc[j, "unit"] = "%"
            df_tables.loc[j, "shortUnit"] = "%"
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[j, "colorScaleNumericBins"] = welfare[
                "scale_relative_poverty"
            ][wel]
            df_tables.loc[j, "colorScaleNumericMinValue"] = welfare[
                "min_relative_poverty"
            ][wel]
            df_tables.loc[j, "colorScaleScheme"] = "YlOrBr"
            j += 1

    df_tables["tableSlug"] = tables["name"][tab]

df_tables["sourceName"] = sourceName
df_tables["dataPublishedBy"] = dataPublishedBy
df_tables["sourceLink"] = sourceLink
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
            ] = f"The Gini coefficient measures inequality on a scale from 0 to 1. Higher values indicate higher inequality. {welfare['subtitle_ineq'][wel]}"
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
            ] = f"The Palma ratio is a measure of inequality that divides the share received by the richest 10% by the share of the poorest 40%. Higher values indicate higher inequality. {welfare['subtitle_ineq'][wel]}"
            df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
            df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers.loc[j, "hasMapTab"] = "true"
            df_graphers.loc[j, "tab"] = "map"
            j += 1

            # Headcount ratio (rel)
            df_graphers.loc[
                j, "title"
            ] = f"Share of people in relative poverty ({welfare['title'][wel]})"
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
            ] = f"The share of the population with {welfare['welfare_type'][wel]} below 50% of the median. Relative poverty reflects the extent of inequality within the bottom of the distribution. {welfare['subtitle'][wel]}"
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
        ] = f"The Gini coefficient measures inequality on a scale from 0 to 1. Higher values indicate higher inequality."
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
        ] = f"The Palma ratio is a measure of inequality that divides the share received by the richest 10% by the share of the poorest 40%. Higher values indicate higher inequality."
        df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
        df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        df_graphers.loc[j, "hasMapTab"] = "false"
        df_graphers.loc[j, "tab"] = "chart"
        j += 1

        # Headcount ratio (rel)
        df_graphers.loc[
            j, "title"
        ] = f"Share of people in relative poverty (after tax vs. before tax)"
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
        ] = f"The share of the population with {welfare['welfare_type'][wel]} below 50% of the median. Relative poverty reflects the extent of inequality within the bottom of the distribution."
        df_graphers.loc[j, "note"] = equivalence_scales["note"][eq]
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
