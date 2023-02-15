# %% [markdown]
# # Poverty metrics (expanded) explorer of the Luxembourg Income Study
# This code creates the tsv file for the expanded poverty metrics explorer from the LIS data, available [here](https://owid.cloud/admin/explorers/preview/lis-expanded-poverty)

import textwrap
from pathlib import Path

import numpy as np

# %%
import pandas as pd

PARENT_DIR = Path(__file__).parent.parent.parent.absolute()
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
    "explorerTitle": "Poverty Explorer of the Luxembourg Income Study - Additional metrics",
    "selection": [
        "Chile",
        "Brazil",
        "South Africa",
        "United States",
        "France",
        "China",
    ],
    "explorerSubtitle": "",
    "isPublished": "false",
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

sourceName = "World Inequality Database (WID.world) (2022)"
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

    for wel in range(len(welfare)):
        # Gini coefficient
        df_tables.loc[
            j, "name"
        ] = f"Gini coefficient ({welfare['technical_text'][wel].capitalize()})"
        df_tables.loc[j, "slug"] = f"p0p100_gini_{welfare['slug'][wel]}"
        df_tables.loc[
            j, "description"
        ] = f"The Gini coefficient is a measure of the inequality of the {welfare['welfare_type'][wel]} distribution in a population. Higher values indicate a higher level of inequality.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]} {welfare['note'][wel]}"
        df_tables.loc[j, "unit"] = np.nan
        df_tables.loc[j, "shortUnit"] = np.nan
        df_tables.loc[j, "type"] = "Numeric"
        df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_gini"][wel]
        df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables.loc[j, "colorScaleScheme"] = "Reds"
        j += 1

        # Mean
        df_tables.loc[
            j, "name"
        ] = f"Mean {welfare['welfare_type'][wel]}  ({welfare['technical_text'][wel].capitalize()})"
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
        ] = f"Median {welfare['welfare_type'][wel]}  ({welfare['technical_text'][wel].capitalize()})"
        df_tables.loc[j, "slug"] = f"p50p60_thr_{welfare['slug'][wel]}"
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

        # Share of the top 10%
        df_tables.loc[
            j, "name"
        ] = f"{welfare['welfare_type'][wel].capitalize()} share of the richest 10% ({welfare['technical_text'][wel].capitalize()})"
        df_tables.loc[j, "slug"] = f"p90p100_share_{welfare['slug'][wel]}"
        df_tables.loc[
            j, "description"
        ] = f"This is the {welfare['welfare_type'][wel]} of the richest 10% as a share of total {welfare['welfare_type'][wel]}.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]} {welfare['note'][wel]}"
        df_tables.loc[j, "unit"] = "%"
        df_tables.loc[j, "shortUnit"] = "%"
        df_tables.loc[j, "type"] = "Numeric"
        df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_top10"][wel]
        df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables.loc[j, "colorScaleScheme"] = "Greens"
        j += 1

        # Share of the top 1%
        df_tables.loc[
            j, "name"
        ] = f"{welfare['welfare_type'][wel].capitalize()} share of the richest 1% ({welfare['technical_text'][wel].capitalize()})"
        df_tables.loc[j, "slug"] = f"p99p100_share_{welfare['slug'][wel]}"
        df_tables.loc[
            j, "description"
        ] = f"This is the {welfare['welfare_type'][wel]} of the richest 1% as a share of total {welfare['welfare_type'][wel]}.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]} {welfare['note'][wel]}"
        df_tables.loc[j, "unit"] = "%"
        df_tables.loc[j, "shortUnit"] = "%"
        df_tables.loc[j, "type"] = "Numeric"
        df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_top1"][wel]
        df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables.loc[j, "colorScaleScheme"] = "Greens"
        j += 1

        # Share of the top 0.1%
        df_tables.loc[
            j, "name"
        ] = f"{welfare['welfare_type'][wel].capitalize()} share of the richest 0.1% ({welfare['technical_text'][wel].capitalize()})"
        df_tables.loc[j, "slug"] = f"p99_9p100_share_{welfare['slug'][wel]}"
        df_tables.loc[
            j, "description"
        ] = f"This is the {welfare['welfare_type'][wel]} of the richest 0.1% as a share of total {welfare['welfare_type'][wel]}.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]} {welfare['note'][wel]}"
        df_tables.loc[j, "unit"] = "%"
        df_tables.loc[j, "shortUnit"] = "%"
        df_tables.loc[j, "type"] = "Numeric"
        df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_top01"][wel]
        df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables.loc[j, "colorScaleScheme"] = "Greens"
        j += 1

        # Palma ratio
        df_tables.loc[
            j, "name"
        ] = f"Palma ratio ({welfare['technical_text'][wel].capitalize()})"
        df_tables.loc[j, "slug"] = f"palma_ratio_{welfare['slug'][wel]}"
        df_tables.loc[
            j, "description"
        ] = f"The Palma ratio is a measure of inequality: it is the share of total {welfare['welfare_type'][wel]} of the top 10% divided by the share of the bottom 40%.{new_line}This is {welfare['technical_text'][wel]}. {welfare['subtitle'][wel]} {welfare['note'][wel]}"
        df_tables.loc[j, "unit"] = np.nan
        df_tables.loc[j, "shortUnit"] = np.nan
        df_tables.loc[j, "type"] = "Numeric"
        df_tables.loc[j, "colorScaleNumericBins"] = welfare["scale_palma_ratio"][wel]
        df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables.loc[j, "colorScaleScheme"] = "Oranges"
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

df_graphers = pd.DataFrame()

j = 0

for tab in range(len(tables)):
    for wel in range(len(welfare)):
        # Gini coefficient
        df_graphers.loc[
            j, "title"
        ] = f"{welfare['welfare_type'][wel].capitalize()} inequality: Gini coefficient {welfare['title'][wel].capitalize()}"
        df_graphers.loc[j, "ySlugs"] = f"p0p100_gini_{welfare['slug'][wel]}"
        df_graphers.loc[j, "Metric Dropdown"] = "Gini coefficient"
        df_graphers.loc[
            j, "Welfare type Dropdown"
        ] = f"{welfare['dropdown_option'][wel]}"
        df_graphers.loc[
            j, "subtitle"
        ] = f"The Gini coefficient is a measure of the inequality of the {welfare['welfare_type'][wel]} distribution in a population. Higher values indicate a higher level of inequality. {welfare['subtitle'][wel]}"
        df_graphers.loc[j, "note"] = f"{welfare['note'][wel]}"
        df_graphers.loc[j, "facet"] = np.nan
        df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers.loc[j, "hasMapTab"] = "true"
        df_graphers.loc[j, "tab"] = "map"
        df_graphers.loc[j, "mapTargetTime"] = 2019
        j += 1

        # Mean
        df_graphers.loc[
            j, "title"
        ] = f"Mean {welfare['welfare_type'][wel]} {welfare['title'][wel].capitalize()}"
        df_graphers.loc[j, "ySlugs"] = f"p0p100_avg_{welfare['slug'][wel]}"
        df_graphers.loc[j, "Metric Dropdown"] = "Mean income or wealth"
        df_graphers.loc[
            j, "Welfare type Dropdown"
        ] = f"{welfare['dropdown_option'][wel]}"
        df_graphers.loc[
            j, "subtitle"
        ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. {welfare['subtitle'][wel]}"
        df_graphers.loc[
            j, "note"
        ] = f"This data is measured in international-$ at 2021 prices. {welfare['note'][wel]}"
        df_graphers.loc[j, "facet"] = np.nan
        df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers.loc[j, "hasMapTab"] = "true"
        df_graphers.loc[j, "tab"] = "map"
        df_graphers.loc[j, "mapTargetTime"] = 2019
        df_graphers.loc[j, "yScaleToggle"] = "true"
        j += 1

        # Median
        df_graphers.loc[
            j, "title"
        ] = f"Median {welfare['welfare_type'][wel]} {welfare['title'][wel].capitalize()}"
        df_graphers.loc[j, "ySlugs"] = f"p50p60_thr_{welfare['slug'][wel]}"
        df_graphers.loc[j, "Metric Dropdown"] = "Median income or wealth"
        df_graphers.loc[
            j, "Welfare type Dropdown"
        ] = f"{welfare['dropdown_option'][wel]}"
        df_graphers.loc[
            j, "subtitle"
        ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. {welfare['subtitle'][wel]}"
        df_graphers.loc[
            j, "note"
        ] = f"This data is measured in international-$ at 2021 prices. {welfare['note'][wel]}"
        df_graphers.loc[j, "facet"] = np.nan
        df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers.loc[j, "hasMapTab"] = "true"
        df_graphers.loc[j, "tab"] = "map"
        df_graphers.loc[j, "mapTargetTime"] = 2019
        df_graphers.loc[j, "yScaleToggle"] = "true"
        j += 1

        # Share of the top 10%
        df_graphers.loc[
            j, "title"
        ] = f"{welfare['welfare_type'][wel].capitalize()} share of the top 10% {welfare['title'][wel].capitalize()}"
        df_graphers.loc[j, "ySlugs"] = f"p90p100_share_{welfare['slug'][wel]}"
        df_graphers.loc[j, "Metric Dropdown"] = "Top 10% share"
        df_graphers.loc[
            j, "Welfare type Dropdown"
        ] = f"{welfare['dropdown_option'][wel]}"
        df_graphers.loc[
            j, "subtitle"
        ] = f"This is the {welfare['welfare_type'][wel]} of the richest 10% as a share of total {welfare['welfare_type'][wel]}. {welfare['subtitle'][wel]}"
        df_graphers.loc[j, "note"] = f"{welfare['note'][wel]}"
        df_graphers.loc[j, "facet"] = np.nan
        df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers.loc[j, "hasMapTab"] = "true"
        df_graphers.loc[j, "tab"] = "map"
        df_graphers.loc[j, "mapTargetTime"] = 2019
        j += 1

        # Share of the top 1%
        df_graphers.loc[
            j, "title"
        ] = f"{welfare['welfare_type'][wel].capitalize()} share of the top 1% {welfare['title'][wel].capitalize()}"
        df_graphers.loc[j, "ySlugs"] = f"p99p100_share_{welfare['slug'][wel]}"
        df_graphers.loc[j, "Metric Dropdown"] = "Top 1% share"
        df_graphers.loc[
            j, "Welfare type Dropdown"
        ] = f"{welfare['dropdown_option'][wel]}"
        df_graphers.loc[
            j, "subtitle"
        ] = f"This is the {welfare['welfare_type'][wel]} of the richest 1% as a share of total {welfare['welfare_type'][wel]}. {welfare['subtitle'][wel]}"
        df_graphers.loc[j, "note"] = f"{welfare['note'][wel]}"
        df_graphers.loc[j, "facet"] = np.nan
        df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers.loc[j, "hasMapTab"] = "true"
        df_graphers.loc[j, "tab"] = "map"
        df_graphers.loc[j, "mapTargetTime"] = 2019
        j += 1

        # # Palma ratio
        df_graphers.loc[
            j, "title"
        ] = f"{welfare['welfare_type'][wel].capitalize()} inequality: Palma ratio {welfare['title'][wel].capitalize()}"
        df_graphers.loc[j, "ySlugs"] = f"palma_ratio_{welfare['slug'][wel]}"
        df_graphers.loc[j, "Metric Dropdown"] = "Palma ratio"
        df_graphers.loc[
            j, "Welfare type Dropdown"
        ] = f"{welfare['dropdown_option'][wel]}"
        df_graphers.loc[
            j, "subtitle"
        ] = f"The Palma ratio is the share of total {welfare['welfare_type'][wel]} of the top 10% divided by the share of the bottom 40%. {welfare['subtitle'][wel]}"
        df_graphers.loc[j, "note"] = f"{welfare['note'][wel]}"
        df_graphers.loc[j, "facet"] = np.nan
        df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers.loc[j, "hasMapTab"] = "true"
        df_graphers.loc[j, "tab"] = "map"
        df_graphers.loc[j, "mapTargetTime"] = 2019
        j += 1

    df_graphers["tableSlug"] = tables["name"][tab]

# %% [markdown]
# Final adjustments to the graphers table: add `relatedQuestion` link and `defaultView`:

# %%
# Add related question link
df_graphers["relatedQuestionText"] = np.nan
df_graphers["relatedQuestionUrl"] = np.nan

# Add yAxisMin
df_graphers["yAxisMin"] = yAxisMin

# Make mapTargetTime integer (to not break the parameter in the platform)
df_graphers["mapTargetTime"] = df_graphers["mapTargetTime"].astype("Int64")

# Select one default view
df_graphers.loc[
    (df_graphers["Metric Dropdown"] == "Gini coefficient")
    & (df_graphers["Welfare type Dropdown"] == "Income before tax"),
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
