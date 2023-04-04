# %% [markdown]
# # Incomes Across the Distribution Explorer of the World Inequality Database
# This code creates the tsv file for the incomes across the distribution explorer from the WID data, available [here](https://owid.cloud/admin/explorers/preview/wid-keymetrics)

import textwrap
from pathlib import Path

import numpy as np

# %%
import pandas as pd

PARENT_DIR = Path(__file__).parent.parent.parent.parent.absolute()
outfile = PARENT_DIR / "explorers" / "wid-incomes-across-distribution.explorer.tsv"

# %% [markdown]
# ## Google sheets auxiliar data
# These spreadsheets provide with different details depending on each type of welfare measure or tables considered.

# %%
# Read Google sheets
sheet_id = "18T5IGnpyJwb8KL9USYvME6IaLEcYIo26ioHCpkDnwRQ"

# Welfare type sheet
sheet_name = "welfare"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
welfare = pd.read_csv(url, keep_default_na=False)

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

# Relative toggle (to switch between absolute and relative values)
sheet_name = "relative_toggle"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
relative_toggle = pd.read_csv(url, keep_default_na=False, dtype={"checkbox": "str"})

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
    "explorerTitle": "Incomes across the distribution (World Inequality Database)",
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
    "pickerColumnSlugs": "p0p100_avg_pretax p0p100_avg_posttax_dis p0p100_avg_posttax_nat p0p100_avg_wealth",
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

sourceName = "World Inequality Database (WID.world) (2023)"
dataPublishedBy = "World Inequality Database (WID), https://wid.world"
sourceLink = "https://wid.world"
colorScaleNumericMinValue = 0
tolerance = 5
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

    # Define original variables to not break income aggregations
    for wel in range(len(welfare)):
        # Mean
        df_tables.loc[
            j, "name"
        ] = f"Mean {welfare['welfare_type'][wel]} ({welfare['technical_text'][wel].capitalize()})"
        df_tables.loc[j, "slug"] = f"p0p100_avg_{welfare['slug'][wel]}"
        df_tables.loc[
            j, "description"
        ] = f"Mean {welfare['welfare_type'][wel]}.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]} {welfare['note'][wel]}"
        df_tables.loc[j, "unit"] = "international-$ in 2021 prices"
        df_tables.loc[j, "shortUnit"] = "$"
        df_tables.loc[j, "type"] = "Numeric"
        df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_mean"][wel]
        df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables.loc[j, "colorScaleScheme"] = "BuGn"
        j += 1

        # Median
        df_tables.loc[
            j, "name"
        ] = f"Median {welfare['welfare_type'][wel]} ({welfare['technical_text'][wel].capitalize()})"
        df_tables.loc[j, "slug"] = f"median_{welfare['slug'][wel]}"
        df_tables.loc[
            j, "description"
        ] = f"This is the level of {welfare['welfare_type'][wel]} below which 50% of the population falls.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]} {welfare['note'][wel]}"
        df_tables.loc[j, "unit"] = "international-$ in 2021 prices"
        df_tables.loc[j, "shortUnit"] = "$"
        df_tables.loc[j, "type"] = "Numeric"
        df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_median"][wel]
        df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables.loc[j, "colorScaleScheme"] = "Blues"
        j += 1

        # Thresholds - Deciles
        for dec9 in range(len(deciles9)):
            df_tables.loc[j, "name"] = f"{deciles9['ordinal'][dec9].capitalize()}"
            df_tables.loc[
                j, "slug"
            ] = f"{deciles9['wid_notation'][dec9]}_thr_{welfare['slug'][wel]}"
            df_tables.loc[
                j, "description"
            ] = f"The level of {welfare['welfare_type'][wel]} below which {deciles9['decile'][dec9]}0% of the population falls.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]} {welfare['note'][wel]}"
            df_tables.loc[j, "unit"] = "international-$ in 2021 prices"
            df_tables.loc[j, "shortUnit"] = "$"
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[j, "colorScaleNumericBins"] = deciles9["scale_thr"][dec9]
            df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
            df_tables.loc[j, "colorScaleScheme"] = "Purples"
            j += 1

        # Averages - Deciles
        for dec10 in range(len(deciles10)):
            df_tables.loc[j, "name"] = f"{deciles10['ordinal'][dec10].capitalize()}"
            df_tables.loc[
                j, "slug"
            ] = f"{deciles10['wid_notation'][dec10]}_avg_{welfare['slug'][wel]}"
            df_tables.loc[
                j, "description"
            ] = f"This is the mean {welfare['welfare_type'][wel]} within the {deciles10['ordinal'][dec10]} (tenth of the population).{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]} {welfare['note'][wel]}"
            df_tables.loc[j, "unit"] = "international-$ in 2021 prices"
            df_tables.loc[j, "shortUnit"] = "$"
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[j, "colorScaleNumericBins"] = deciles10["scale_avg"][dec10]
            df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
            df_tables.loc[j, "colorScaleScheme"] = "Greens"
            j += 1

        # Shares - Deciles
        for dec10 in range(len(deciles10)):
            df_tables.loc[j, "name"] = f"{deciles10['ordinal'][dec10].capitalize()}"
            df_tables.loc[
                j, "slug"
            ] = f"{deciles10['wid_notation'][dec10]}_share_{welfare['slug'][wel]}"
            df_tables.loc[
                j, "description"
            ] = f"This is the {welfare['welfare_type'][wel]} of the {deciles10['ordinal'][dec10]} (tenth of the population) as a share of total {welfare['welfare_type'][wel]}.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]} {welfare['note'][wel]}"
            df_tables.loc[j, "unit"] = "%"
            df_tables.loc[j, "shortUnit"] = "%"
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[j, "colorScaleNumericBins"] = deciles10["scale_share"][dec10]
            df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
            df_tables.loc[j, "colorScaleScheme"] = "OrRd"
            j += 1

        # Thresholds - Top percentiles
        for top in range(len(top_pct)):
            df_tables.loc[j, "name"] = f"{top_pct['name'][top].capitalize()}"
            df_tables.loc[
                j, "slug"
            ] = f"{top_pct['wid_notation'][top]}_thr_{welfare['slug'][wel]}"
            df_tables.loc[
                j, "description"
            ] = f"The level of {welfare['welfare_type'][wel]} marking the richest {top_pct['name'][top]}.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]} {welfare['note'][wel]}"
            df_tables.loc[j, "unit"] = "international-$ in 2021 prices"
            df_tables.loc[j, "shortUnit"] = "$"
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[j, "colorScaleNumericBins"] = top_pct["scale_thr"][top]
            df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
            df_tables.loc[j, "colorScaleScheme"] = "Purples"
            j += 1

        # Averages - Top percentiles
        for top in range(len(top_pct)):
            df_tables.loc[j, "name"] = f"{top_pct['name'][top].capitalize()}"
            df_tables.loc[
                j, "slug"
            ] = f"{top_pct['wid_notation'][top]}_avg_{welfare['slug'][wel]}"
            df_tables.loc[
                j, "description"
            ] = f"This is the mean {welfare['welfare_type'][wel]} within the richest {top_pct['name'][top]}.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]} {welfare['note'][wel]}"
            df_tables.loc[j, "unit"] = "international-$ in 2021 prices"
            df_tables.loc[j, "shortUnit"] = "$"
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[j, "colorScaleNumericBins"] = top_pct["scale_avg"][top]
            df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
            df_tables.loc[j, "colorScaleScheme"] = "Greens"
            j += 1

        # Shares - Top percentiles
        for top in range(len(top_pct)):
            df_tables.loc[j, "name"] = f"{top_pct['name'][top].capitalize()}"
            df_tables.loc[
                j, "slug"
            ] = f"{top_pct['wid_notation'][top]}_share_{welfare['slug'][wel]}"
            df_tables.loc[
                j, "description"
            ] = f"This is the {welfare['welfare_type'][wel]} of the {top_pct['name'][top]} as a share of total {welfare['welfare_type'][wel]}.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]} {welfare['note'][wel]}"
            df_tables.loc[j, "unit"] = "%"
            df_tables.loc[j, "shortUnit"] = "%"
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[j, "colorScaleNumericBins"] = top_pct["scale_share"][top]
            df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
            df_tables.loc[j, "colorScaleScheme"] = "OrRd"
            j += 1

        # Income aggregations
        for agg in range(len(income_aggregation)):
            # Mean
            df_tables.loc[
                j, "name"
            ] = f"Mean {welfare['welfare_type'][wel]} ({welfare['technical_text'][wel].capitalize()})"
            df_tables.loc[
                j, "slug"
            ] = f"p0p100_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]}"
            df_tables.loc[
                j, "description"
            ] = f"Mean {welfare['welfare_type'][wel]}.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]} {welfare['note'][wel]}"
            df_tables.loc[j, "unit"] = "international-$ in 2021 prices"
            df_tables.loc[j, "shortUnit"] = "$"
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_mean"][wel]
            df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
            df_tables.loc[j, "colorScaleScheme"] = "BuGn"
            df_tables.loc[
                j, "transform"
            ] = f"multiplyBy p0p100_avg_{welfare['slug'][wel]} {income_aggregation['multiplier'][agg]}"
            j += 1

            # Median
            df_tables.loc[
                j, "name"
            ] = f"Median {welfare['welfare_type'][wel]} ({welfare['technical_text'][wel].capitalize()})"
            df_tables.loc[
                j, "slug"
            ] = f"median_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]}"
            df_tables.loc[
                j, "description"
            ] = f"This is the level of {welfare['welfare_type'][wel]} below which 50% of the population falls.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]} {welfare['note'][wel]}"
            df_tables.loc[j, "unit"] = "international-$ in 2021 prices"
            df_tables.loc[j, "shortUnit"] = "$"
            df_tables.loc[j, "type"] = "Numeric"
            df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_median"][wel]
            df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
            df_tables.loc[j, "colorScaleScheme"] = "Blues"
            df_tables.loc[
                j, "transform"
            ] = f"multiplyBy median_{welfare['slug'][wel]} {income_aggregation['multiplier'][agg]}"
            j += 1

            # Thresholds - Deciles
            for dec9 in range(len(deciles9)):
                df_tables.loc[j, "name"] = f"{deciles9['ordinal'][dec9].capitalize()}"
                df_tables.loc[
                    j, "slug"
                ] = f"{deciles9['wid_notation'][dec9]}_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]}"
                df_tables.loc[
                    j, "description"
                ] = f"The level of {welfare['welfare_type'][wel]} below which {deciles9['decile'][dec9]}0% of the population falls.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]} {welfare['note'][wel]}"
                df_tables.loc[j, "unit"] = "international-$ in 2021 prices"
                df_tables.loc[j, "shortUnit"] = "$"
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[j, "colorScaleNumericBins"] = deciles9["scale_thr"][dec9]
                df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
                df_tables.loc[j, "colorScaleScheme"] = "Purples"
                df_tables.loc[
                    j, "transform"
                ] = f"multiplyBy {deciles9['wid_notation'][dec9]}_thr_{welfare['slug'][wel]} {income_aggregation['multiplier'][agg]}"
                j += 1

            # Averages - Deciles
            for dec10 in range(len(deciles10)):
                df_tables.loc[j, "name"] = f"{deciles10['ordinal'][dec10].capitalize()}"
                df_tables.loc[
                    j, "slug"
                ] = f"{deciles10['wid_notation'][dec10]}_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]}"
                df_tables.loc[
                    j, "description"
                ] = f"This is the mean {welfare['welfare_type'][wel]} within the {deciles10['ordinal'][dec10]} (tenth of the population).{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]} {welfare['note'][wel]}"
                df_tables.loc[j, "unit"] = "international-$ in 2021 prices"
                df_tables.loc[j, "shortUnit"] = "$"
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[j, "colorScaleNumericBins"] = deciles10["scale_avg"][
                    dec10
                ]
                df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
                df_tables.loc[j, "colorScaleScheme"] = "Greens"
                df_tables.loc[
                    j, "transform"
                ] = f"multiplyBy {deciles10['wid_notation'][dec10]}_avg_{welfare['slug'][wel]} {income_aggregation['multiplier'][agg]}"
                j += 1

            # Thresholds - Top percentiles
            for top in range(len(top_pct)):
                df_tables.loc[j, "name"] = f"{top_pct['name'][top].capitalize()}"
                df_tables.loc[
                    j, "slug"
                ] = f"{top_pct['wid_notation'][top]}_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]}"
                df_tables.loc[
                    j, "description"
                ] = f"The level of {welfare['welfare_type'][wel]} marking the richest {top_pct['name'][top]}.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]} {welfare['note'][wel]}"
                df_tables.loc[j, "unit"] = "international-$ in 2021 prices"
                df_tables.loc[j, "shortUnit"] = "$"
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[j, "colorScaleNumericBins"] = top_pct["scale_thr"][top]
                df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
                df_tables.loc[j, "colorScaleScheme"] = "Purples"
                df_tables.loc[
                    j, "transform"
                ] = f"multiplyBy {top_pct['wid_notation'][top]}_thr_{welfare['slug'][wel]} {income_aggregation['multiplier'][agg]}"
                j += 1

            # Averages - Top percentiles
            for top in range(len(top_pct)):
                df_tables.loc[j, "name"] = f"{top_pct['name'][top].capitalize()}"
                df_tables.loc[
                    j, "slug"
                ] = f"{top_pct['wid_notation'][top]}_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]}"
                df_tables.loc[
                    j, "description"
                ] = f"This is the mean {welfare['welfare_type'][wel]} within the richest {top_pct['name'][top]}.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]} {welfare['note'][wel]}"
                df_tables.loc[j, "unit"] = "international-$ in 2021 prices"
                df_tables.loc[j, "shortUnit"] = "$"
                df_tables.loc[j, "type"] = "Numeric"
                df_tables.loc[j, "colorScaleNumericBins"] = top_pct["scale_avg"][top]
                df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
                df_tables.loc[j, "colorScaleScheme"] = "Greens"
                df_tables.loc[
                    j, "transform"
                ] = f"multiplyBy {top_pct['wid_notation'][top]}_avg_{welfare['slug'][wel]} {income_aggregation['multiplier'][agg]}"
                j += 1

    df_tables["tableSlug"] = tables["name"][tab]

df_tables["sourceName"] = sourceName
df_tables["dataPublishedBy"] = dataPublishedBy
df_tables["sourceLink"] = sourceLink
df_tables["colorScaleNumericMinValue"] = colorScaleNumericMinValue
df_tables["tolerance"] = tolerance

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
        for agg in range(len(income_aggregation)):
            # Mean
            df_graphers.loc[
                j, "title"
            ] = f"Mean {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} {welfare['title'][wel].capitalize()}"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"p0p100_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]}"
            df_graphers.loc[j, "Metric Dropdown"] = "Mean income or wealth"
            df_graphers.loc[
                j, "Data type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[j, "Decile/quantile Dropdown"] = np.nan
            df_graphers.loc[
                j, "Aggregation Radio"
            ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
            df_graphers.loc[j, "Relative change Checkbox"] = "false"
            df_graphers.loc[j, "stackMode"] = "absolute"
            df_graphers.loc[
                j, "subtitle"
            ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. {welfare['subtitle'][wel]}"
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2021 prices. {welfare['note'][wel]}"
            df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers.loc[j, "hasMapTab"] = "true"
            df_graphers.loc[j, "tab"] = "map"
            df_graphers.loc[j, "yScaleToggle"] = "true"
            j += 1

            # Median
            df_graphers.loc[
                j, "title"
            ] = f"Median {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} {welfare['title'][wel].capitalize()}"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"median_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]}"
            df_graphers.loc[j, "Metric Dropdown"] = "Median income or wealth"
            df_graphers.loc[
                j, "Data type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[j, "Decile/quantile Dropdown"] = np.nan
            df_graphers.loc[
                j, "Aggregation Radio"
            ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
            df_graphers.loc[j, "Relative change Checkbox"] = "false"
            df_graphers.loc[j, "stackMode"] = "absolute"
            df_graphers.loc[
                j, "subtitle"
            ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. {welfare['subtitle'][wel]}"
            df_graphers.loc[
                j, "note"
            ] = f"This data is measured in international-$ at 2021 prices. {welfare['note'][wel]}"
            df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers.loc[j, "hasMapTab"] = "true"
            df_graphers.loc[j, "tab"] = "map"
            df_graphers.loc[j, "yScaleToggle"] = "true"
            j += 1

            # Thresholds - Deciles
            for dec9 in range(len(deciles9)):
                df_graphers.loc[
                    j, "title"
                ] = f"Threshold {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} marking the {deciles9['ordinal'][dec9]} {welfare['title'][wel].capitalize()}"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"{deciles9['wid_notation'][dec9]}_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]}"
                df_graphers.loc[j, "Metric Dropdown"] = "Decile thresholds"
                df_graphers.loc[
                    j, "Data type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Decile/quantile Dropdown"] = deciles9["dropdown"][
                    dec9
                ]
                df_graphers.loc[
                    j, "Aggregation Radio"
                ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
                df_graphers.loc[j, "Relative change Checkbox"] = "false"
                df_graphers.loc[j, "stackMode"] = "absolute"
                df_graphers.loc[
                    j, "subtitle"
                ] = f"This is the level of {welfare['welfare_type'][wel]} below which {deciles9['decile'][dec9]}0% of the population falls. {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2021 prices to account for inflation and differences in the cost of living between countries. {welfare['note'][wel]}"
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                df_graphers.loc[j, "yScaleToggle"] = "true"
                j += 1

            # Averages - Deciles
            for dec10 in range(len(deciles10)):
                df_graphers.loc[
                    j, "title"
                ] = f"Mean {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} within the {deciles10['ordinal'][dec10]} {welfare['title'][wel].capitalize()}"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"{deciles10['wid_notation'][dec10]}_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]}"
                df_graphers.loc[
                    j, "Metric Dropdown"
                ] = "Mean income or wealth, by decile"
                df_graphers.loc[
                    j, "Data type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Decile/quantile Dropdown"] = deciles10["dropdown"][
                    dec10
                ]
                df_graphers.loc[
                    j, "Aggregation Radio"
                ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
                df_graphers.loc[j, "Relative change Checkbox"] = "false"
                df_graphers.loc[j, "stackMode"] = "absolute"
                df_graphers.loc[
                    j, "subtitle"
                ] = f"This is the mean {welfare['welfare_type'][wel]} within the {deciles10['ordinal'][dec10]} (tenth of the population). {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2021 prices to account for inflation and differences in the cost of living between countries. {welfare['note'][wel]}"
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                df_graphers.loc[j, "yScaleToggle"] = "true"
                j += 1

            # Thresholds - Top
            for top in range(len(top_pct)):
                df_graphers.loc[
                    j, "title"
                ] = f"Threshold {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} marking the richest {top_pct['name'][top]} {welfare['title'][wel].capitalize()}"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"{top_pct['wid_notation'][top]}_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]}"
                df_graphers.loc[j, "Metric Dropdown"] = "Decile thresholds"
                df_graphers.loc[
                    j, "Data type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Decile/quantile Dropdown"] = top_pct["name"][top]
                df_graphers.loc[
                    j, "Aggregation Radio"
                ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
                df_graphers.loc[j, "Relative change Checkbox"] = "false"
                df_graphers.loc[j, "stackMode"] = "absolute"
                df_graphers.loc[j, "subtitle"] = f"{welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2021 prices to account for inflation and differences in the cost of living between countries. {welfare['note'][wel]}"
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                df_graphers.loc[j, "yScaleToggle"] = "true"
                j += 1

            # Averages - Top
            for top in range(len(top_pct)):
                df_graphers.loc[
                    j, "title"
                ] = f"Mean {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} within the {top_pct['name'][top]} {welfare['title'][wel].capitalize()}"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"{top_pct['wid_notation'][top]}_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]}"
                df_graphers.loc[
                    j, "Metric Dropdown"
                ] = "Mean income or wealth, by decile"
                df_graphers.loc[
                    j, "Data type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Decile/quantile Dropdown"] = top_pct["name"][top]
                df_graphers.loc[
                    j, "Aggregation Radio"
                ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
                df_graphers.loc[j, "Relative change Checkbox"] = "false"
                df_graphers.loc[j, "stackMode"] = "absolute"
                df_graphers.loc[
                    j, "subtitle"
                ] = f"This is the mean {welfare['welfare_type'][wel]} within the richest {top_pct['name'][top]}. {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2021 prices to account for inflation and differences in the cost of living between countries. {welfare['note'][wel]}"
                df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
                df_graphers.loc[j, "hasMapTab"] = "true"
                df_graphers.loc[j, "tab"] = "map"
                df_graphers.loc[j, "yScaleToggle"] = "true"
                j += 1

            for rel_toggle in range(len(relative_toggle)):
                # Thresholds - Multiple deciles
                df_graphers.loc[
                    j, "title"
                ] = f"Threshold {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} for each decile {welfare['title'][wel].capitalize()}"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"p10p20_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p20p30_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p30p40_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p40p50_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p50p60_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p60p70_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p70p80_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p80p90_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p90p100_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]}"
                df_graphers.loc[j, "Metric Dropdown"] = "Decile thresholds"
                df_graphers.loc[
                    j, "Data type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Decile/quantile Dropdown"] = "All deciles"
                df_graphers.loc[
                    j, "Aggregation Radio"
                ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
                df_graphers.loc[j, "Relative change Checkbox"] = relative_toggle[
                    "checkbox"
                ][rel_toggle]
                df_graphers.loc[j, "stackMode"] = relative_toggle["stack_mode"][
                    rel_toggle
                ]
                df_graphers.loc[
                    j, "subtitle"
                ] = f"This is the level of income or consumption per year below which 10%, 20%, 30%, etc. of the population falls. {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2021 prices to account for inflation and differences in the cost of living between countries. {welfare['note'][wel]}"
                df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
                df_graphers.loc[j, "hasMapTab"] = "false"
                df_graphers.loc[j, "tab"] = "chart"
                df_graphers.loc[j, "yScaleToggle"] = "true"
                j += 1

                # Averages - Multiple deciles
                df_graphers.loc[
                    j, "title"
                ] = f"Mean {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} within each decile {welfare['title'][wel].capitalize()}"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"p0p10_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p10p20_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p20p30_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p30p40_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p40p50_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p50p60_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p60p70_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p70p80_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p80p90_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p90p100_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]}"
                df_graphers.loc[
                    j, "Metric Dropdown"
                ] = "Mean income or wealth, by decile"
                df_graphers.loc[
                    j, "Data type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Decile/quantile Dropdown"] = "All deciles"
                df_graphers.loc[
                    j, "Aggregation Radio"
                ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
                df_graphers.loc[j, "Relative change Checkbox"] = relative_toggle[
                    "checkbox"
                ][rel_toggle]
                df_graphers.loc[j, "stackMode"] = relative_toggle["stack_mode"][
                    rel_toggle
                ]
                df_graphers.loc[
                    j, "subtitle"
                ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2021 prices. {welfare['note'][wel]}"
                df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
                df_graphers.loc[j, "hasMapTab"] = "false"
                df_graphers.loc[j, "tab"] = "chart"
                df_graphers.loc[j, "yScaleToggle"] = "true"
                j += 1

                # Thresholds - Multiple deciles (including top)
                df_graphers.loc[
                    j, "title"
                ] = f"Threshold {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} for each decile {welfare['title'][wel].capitalize()}"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"p10p20_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p20p30_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p30p40_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p40p50_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p50p60_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p60p70_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p70p80_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p80p90_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p90p100_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p99p100_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p99_9p100_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p99_99p100_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p99_999p100_thr_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]}"
                df_graphers.loc[j, "Metric Dropdown"] = "Decile thresholds"
                df_graphers.loc[
                    j, "Data type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Decile/quantile Dropdown"] = "All deciles + top"
                df_graphers.loc[
                    j, "Aggregation Radio"
                ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
                df_graphers.loc[j, "Relative change Checkbox"] = relative_toggle[
                    "checkbox"
                ][rel_toggle]
                df_graphers.loc[j, "stackMode"] = relative_toggle["stack_mode"][
                    rel_toggle
                ]
                df_graphers.loc[
                    j, "subtitle"
                ] = f"This is the level of income or consumption per year below which 10%, 20%, 30%, etc. of the population falls. {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2021 prices to account for inflation and differences in the cost of living between countries. {welfare['note'][wel]}"
                df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
                df_graphers.loc[j, "hasMapTab"] = "false"
                df_graphers.loc[j, "tab"] = "chart"
                df_graphers.loc[j, "yScaleToggle"] = "true"
                j += 1

                # Averages - Multiple deciles (including top)
                df_graphers.loc[
                    j, "title"
                ] = f"Mean {welfare['welfare_type'][wel]} per {income_aggregation['aggregation'][agg]} within each decile {welfare['title'][wel].capitalize()}"
                df_graphers.loc[
                    j, "ySlugs"
                ] = f"p0p10_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p10p20_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p20p30_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p30p40_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p40p50_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p50p60_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p60p70_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p70p80_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p80p90_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p90p100_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p99p100_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p99_9p100_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p99_99p100_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]} p99_999p100_avg_{welfare['slug'][wel]}{income_aggregation['slug_suffix'][agg]}"
                df_graphers.loc[
                    j, "Metric Dropdown"
                ] = "Mean income or wealth, by decile"
                df_graphers.loc[
                    j, "Data type Dropdown"
                ] = f"{welfare['dropdown_option'][wel]}"
                df_graphers.loc[j, "Decile/quantile Dropdown"] = "All deciles + top"
                df_graphers.loc[
                    j, "Aggregation Radio"
                ] = f"{income_aggregation['aggregation'][agg].capitalize()}"
                df_graphers.loc[j, "Relative change Checkbox"] = relative_toggle[
                    "checkbox"
                ][rel_toggle]
                df_graphers.loc[j, "stackMode"] = relative_toggle["stack_mode"][
                    rel_toggle
                ]
                df_graphers.loc[
                    j, "subtitle"
                ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. {welfare['subtitle'][wel]}"
                df_graphers.loc[
                    j, "note"
                ] = f"This data is measured in international-$ at 2021 prices. {welfare['note'][wel]}"
                df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
                df_graphers.loc[j, "hasMapTab"] = "false"
                df_graphers.loc[j, "tab"] = "chart"
                df_graphers.loc[j, "yScaleToggle"] = "true"
                j += 1

        # Shares - Deciles
        for dec10 in range(len(deciles10)):
            df_graphers.loc[
                j, "title"
            ] = f"{welfare['welfare_type'][wel].capitalize()} share of the {deciles10['ordinal'][dec10]} {welfare['title'][wel].capitalize()}"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"{deciles10['wid_notation'][dec10]}_share_{welfare['slug'][wel]}"
            df_graphers.loc[j, "Metric Dropdown"] = "Decile shares"
            df_graphers.loc[
                j, "Data type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[j, "Decile/quantile Dropdown"] = deciles10["dropdown"][
                dec10
            ]
            df_graphers.loc[j, "Aggregation Radio"] = np.nan
            df_graphers.loc[j, "Relative change Checkbox"] = "false"
            df_graphers.loc[j, "stackMode"] = "absolute"
            df_graphers.loc[
                j, "subtitle"
            ] = f"This is the {welfare['welfare_type'][wel]} of the {deciles10['ordinal'][dec10]} (tenth of the population) as a share of total {welfare['welfare_type'][wel]}. {welfare['subtitle'][wel]}"
            df_graphers.loc[j, "note"] = f"{welfare['note'][wel]}"
            df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers.loc[j, "hasMapTab"] = "true"
            df_graphers.loc[j, "tab"] = "map"
            j += 1

        # Shares - Top
        for top in range(len(top_pct)):
            df_graphers.loc[
                j, "title"
            ] = f"{welfare['welfare_type'][wel].capitalize()} share of the richest {top_pct['name'][top]} {welfare['title'][wel].capitalize()}"
            df_graphers.loc[
                j, "ySlugs"
            ] = f"{top_pct['wid_notation'][top]}_share_{welfare['slug'][wel]}"
            df_graphers.loc[j, "Metric Dropdown"] = "Decile shares"
            df_graphers.loc[
                j, "Data type Dropdown"
            ] = f"{welfare['dropdown_option'][wel]}"
            df_graphers.loc[j, "Decile/quantile Dropdown"] = top_pct["name"][top]
            df_graphers.loc[j, "Aggregation Radio"] = np.nan
            df_graphers.loc[j, "Relative change Checkbox"] = "false"
            df_graphers.loc[j, "stackMode"] = "absolute"
            df_graphers.loc[
                j, "subtitle"
            ] = f"This is the {welfare['welfare_type'][wel]} of the richest {top_pct['name'][top]} as a share of total {welfare['welfare_type'][wel]}. {welfare['subtitle'][wel]}"
            df_graphers.loc[j, "note"] = f"{welfare['note'][wel]}"
            df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
            df_graphers.loc[j, "hasMapTab"] = "true"
            df_graphers.loc[j, "tab"] = "map"
            j += 1

        # Shares - Multiple deciles
        df_graphers.loc[
            j, "title"
        ] = f"{welfare['welfare_type'][wel].capitalize()} share for each decile {welfare['title'][wel].capitalize()}"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"p0p10_share_{welfare['slug'][wel]} p20p30_share_{welfare['slug'][wel]} p30p40_share_{welfare['slug'][wel]} p40p50_share_{welfare['slug'][wel]} p50p60_share_{welfare['slug'][wel]} p60p70_share_{welfare['slug'][wel]} p70p80_share_{welfare['slug'][wel]} p80p90_share_{welfare['slug'][wel]} p90p100_share_{welfare['slug'][wel]}"
        df_graphers.loc[j, "Metric Dropdown"] = "Decile shares"
        df_graphers.loc[j, "Data type Dropdown"] = f"{welfare['dropdown_option'][wel]}"
        df_graphers.loc[j, "Decile/quantile Dropdown"] = "All deciles"
        df_graphers.loc[j, "Aggregation Radio"] = np.nan
        df_graphers.loc[j, "Relative change Checkbox"] = "false"
        df_graphers.loc[j, "stackMode"] = "absolute"
        df_graphers.loc[
            j, "subtitle"
        ] = f"This is the {welfare['welfare_type'][wel]} of each decile (tenth of the population) as a share of total {welfare['welfare_type'][wel]}. {welfare['subtitle'][wel]}"
        df_graphers.loc[j, "note"] = f"{welfare['note'][wel]}"
        df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        df_graphers.loc[j, "hasMapTab"] = "false"
        df_graphers.loc[j, "tab"] = "chart"
        j += 1

        # Shares - Multiple deciles (including top)
        df_graphers.loc[
            j, "title"
        ] = f"{welfare['welfare_type'][wel].capitalize()} share for each decile {welfare['title'][wel].capitalize()}"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"p0p10_share_{welfare['slug'][wel]} p10p20_share_{welfare['slug'][wel]} p20p30_share_{welfare['slug'][wel]} p30p40_share_{welfare['slug'][wel]} p40p50_share_{welfare['slug'][wel]} p50p60_share_{welfare['slug'][wel]} p60p70_share_{welfare['slug'][wel]} p70p80_share_{welfare['slug'][wel]} p80p90_share_{welfare['slug'][wel]} p90p100_share_{welfare['slug'][wel]} p99p100_share_{welfare['slug'][wel]} p99_9p100_share_{welfare['slug'][wel]} p99_99p100_share_{welfare['slug'][wel]} p99_999p100_share_{welfare['slug'][wel]}"
        df_graphers.loc[j, "Metric Dropdown"] = "Decile shares"
        df_graphers.loc[j, "Data type Dropdown"] = f"{welfare['dropdown_option'][wel]}"
        df_graphers.loc[j, "Decile/quantile Dropdown"] = "All deciles + top"
        df_graphers.loc[j, "Aggregation Radio"] = np.nan
        df_graphers.loc[j, "Relative change Checkbox"] = "false"
        df_graphers.loc[j, "stackMode"] = "absolute"
        df_graphers.loc[
            j, "subtitle"
        ] = f"This is the {welfare['welfare_type'][wel]} of each decile (tenth of the population) as a share of total {welfare['welfare_type'][wel]}. {welfare['subtitle'][wel]}"
        df_graphers.loc[j, "note"] = f"{welfare['note'][wel]}"
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

# Correct title for wealth values (there is a space before the comma)
df_graphers["title"] = df_graphers["title"].str.strip()

# Select one default view
df_graphers.loc[
    (df_graphers["Metric Dropdown"] == "Decile thresholds")
    & (df_graphers["Data type Dropdown"] == "Income before tax")
    & (df_graphers["Decile/quantile Dropdown"] == "All deciles")
    & (df_graphers["Aggregation Radio"] == "Year")
    & (df_graphers["Relative change Checkbox"] == "false"),
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
    "Top 1%",
    "Top 0.1%",
    "Top 0.01%",
    "Top 0.001%",
]

df_graphers_mapping = pd.DataFrame(
    {
        "decile_dropdown": decile_dropdown_list,
    }
)
df_graphers_mapping = df_graphers_mapping.reset_index().set_index("decile_dropdown")
df_graphers["decile_dropdown_aux"] = df_graphers["Decile/quantile Dropdown"].map(
    df_graphers_mapping["index"]
)

# Metric dropdown
metric_dropdown_list = [
    "Mean income or wealth",
    "Mean income or wealth, by decile",
    "Median income or wealth",
    "Decile thresholds",
    "Decile shares",
]

df_graphers_mapping = pd.DataFrame(
    {
        "metric_dropdown": metric_dropdown_list,
    }
)
df_graphers_mapping = df_graphers_mapping.reset_index().set_index("metric_dropdown")
df_graphers["metric_dropdown_aux"] = df_graphers["Metric Dropdown"].map(
    df_graphers_mapping["index"]
)

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
        f.write("\ncolumns\t" + tables["name"][tab] + "\n\n" + table_tsv_indented)
