# %% [markdown]
# # Poverty Data Explorer of World Bank data: 2011 vs 2017 prices
# This code creates the tsv file for the PPP comparison explorer from the World Bank PIP data, available [here](https://ourworldindata.org/explorers/poverty-explorer-2011-vs-2017-ppp)

import textwrap
from pathlib import Path

import numpy as np

# %%
import pandas as pd

PARENT_DIR = Path(__file__).parent.parent.parent.parent.absolute()
outfile = PARENT_DIR / "explorers" / "poverty-explorer-2011-vs-2017-ppp.explorer.tsv"

# %% [markdown]
# ## Google sheets auxiliar data
# These spreadsheets provide with different details depending on each poverty line (from 2011 and 2017 prices), both prices together, relative poverty or survey type.

# %%
# Read Google sheets
sheet_id = "1mR0LPEGlY-wCp1q9lNTlDbVIG65JazKvHL16my9tH8Y"

# Poverty lines in 2011 prices sheet
sheet_name = "povlines_ppp2011"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
povlines_ppp2011 = pd.read_csv(url, dtype={"dollars_text": "str"})

# Poverty lines in 2017 prices sheet
sheet_name = "povlines_ppp2017"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
povlines_ppp2017 = pd.read_csv(url, dtype={"dollars_text": "str"})

# Poverty lines in both 2011 and 2017 prices sheet
sheet_name = "povlines_both"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
povlines_both = pd.read_csv(
    url, dtype={"dollars_2011_text": "str", "dollars_2017_text": "str"}
)

# Relative poverty lines sheet
sheet_name = "povlines_rel"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
povlines_rel = pd.read_csv(url)

# Survey type sheet
sheet_name = "survey_type"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
survey_type = pd.read_csv(url)

# %% [markdown]
# ## Header
# General settings of the explorer are defined here, like the title, subtitle, default country selection, publishing status and others.

# %%
# The header is defined as a dictionary first and then it is converted into a index-oriented dataframe
header_dict = {
    "explorerTitle": "Poverty Data Explorer: World Bank data - 2011 vs. 2017 prices",
    "selection": ["Mozambique", "Nigeria", "Kenya", "Bangladesh", "Bolivia", "World"],
    "explorerSubtitle": "[_Download Poverty data on GitHub_](https://github.com/owid/poverty-data)",
    "isPublished": "true",
    "googleSheet": f"https://docs.google.com/spreadsheets/d/{sheet_id}",
    "wpBlockId": "57756",
    "entityType": "country or region",
}

# Index-oriented dataframe
df_header = pd.DataFrame.from_dict(header_dict, orient="index", columns=None)
# Assigns a cell for each entity separated by comma (like in `selection`)
df_header = df_header[0].apply(pd.Series)

# %% [markdown]
# ## Tables
# Variables are grouped by type to iterate by different poverty lines and survey types at the same time. The output is the list of all the variables being used in the explorer, with metadata.

# %%
new_line = "\\n\\n"

additional_description = new_line.join(
    [
        "Non-market sources of income, including food grown by subsistence farmers for their own consumption, are taken into account.",
    ]
)

notes_title = "NOTES ON HOW WE PROCESSED THIS INDICATOR"

processing_description = new_line.join(
    [
        "For a small number of country-year observations, the World Bank PIP data contains two estimates: one based on income data and one based on consumption data. In these cases we keep only the consumption estimate in order to obtain a single series for each country.",
        "You can find the data with all available income and consumption data points, including these overlapping estimates, in our [complete dataset](https://github.com/owid/poverty-data#a-global-dataset-of-poverty-and-inequality-measures-prepared-by-our-world-in-data-from-the-world-banks-poverty-and-inequality-platform-pip-database) of the World Bank PIP data.",
    ]
)
ppp_description_2017 = "The data is measured in international-$ at 2017 prices – this adjusts for inflation and for differences in the cost of living between countries."
ppp_description_2011 = "The data is measured in international-$ at 2011 prices – this adjusts for inflation and for differences in the cost of living between countries."

# Table generation
df_tables = pd.DataFrame()
j = 0

for survey in range(len(survey_type)):
    # Shares (2011)
    for p_2011 in range(len(povlines_ppp2011)):
        df_tables.loc[
            j, "name"
        ] = f"Share of population below ${povlines_ppp2011.dollars_text[p_2011]} a day (2011 prices)"

        df_tables.loc[
            j, "slug"
        ] = f"headcount_ratio_{povlines_ppp2011.cents[p_2011]}_ppp2011"
        df_tables.loc[
            j, "sourceName"
        ] = "World Bank Poverty and Inequality Platform (2022)"
        df_tables.loc[j, "description"] = new_line.join(
            [
                f"% of population living in households with an {survey_type.text[survey]} per person below ${povlines_ppp2011.dollars_text[p_2011]} a day (2011 prices).",
                ppp_description_2011,
                survey_type.description[survey],
                additional_description,
                notes_title,
                processing_description,
            ]
        )
        df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
        df_tables.loc[
            j, "dataPublishedBy"
        ] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, "unit"] = "%"
        df_tables.loc[j, "shortUnit"] = "%"
        df_tables.loc[j, "tolerance"] = 5
        df_tables.loc[j, "type"] = "Numeric"
        df_tables.loc[j, "colorScaleNumericMinValue"] = 0
        df_tables.loc[j, "colorScaleNumericBins"] = "3;10;20;30;40;50;60;70;80;90;100"
        df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables.loc[j, "colorScaleScheme"] = "OrRd"
        df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
        j += 1

    # Shares (2017)
    for p_2017 in range(len(povlines_ppp2017)):
        df_tables.loc[
            j, "name"
        ] = f"Share of population below ${povlines_ppp2017.dollars_text[p_2017]} a day (2017 prices)"
        df_tables.loc[
            j, "slug"
        ] = f"headcount_ratio_{povlines_ppp2017.cents[p_2017]}_ppp2017"
        df_tables.loc[
            j, "sourceName"
        ] = "World Bank Poverty and Inequality Platform (2022)"
        df_tables.loc[j, "description"] = new_line.join(
            [
                f"% of population living in households with an {survey_type.text[survey]} per person below ${povlines_ppp2017.dollars_text[p_2017]} a day (2017 prices).",
                ppp_description_2017,
                survey_type.description[survey],
                additional_description,
                notes_title,
                processing_description,
            ]
        )
        df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
        df_tables.loc[
            j, "dataPublishedBy"
        ] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, "unit"] = "%"
        df_tables.loc[j, "shortUnit"] = "%"
        df_tables.loc[j, "tolerance"] = 5
        df_tables.loc[j, "type"] = "Numeric"
        df_tables.loc[j, "colorScaleNumericMinValue"] = 0
        df_tables.loc[j, "colorScaleNumericBins"] = "3;10;20;30;40;50;60;70;80;90;100"
        df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables.loc[j, "colorScaleScheme"] = "OrRd"
        df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
        j += 1

    # Number (2011)
    for p_2011 in range(len(povlines_ppp2011)):
        df_tables.loc[
            j, "name"
        ] = f"Number of people below ${povlines_ppp2011.dollars_text[p_2011]} a day (2011 prices)"
        df_tables.loc[j, "slug"] = f"headcount_{povlines_ppp2011.cents[p_2011]}_ppp2011"
        df_tables.loc[
            j, "sourceName"
        ] = "World Bank Poverty and Inequality Platform (2022)"
        df_tables.loc[j, "description"] = new_line.join(
            [
                f"Number of people living in households with an {survey_type.text[survey]} per person below ${povlines_ppp2011.dollars_text[p_2011]} a day (2011 prices).",
                ppp_description_2011,
                survey_type.description[survey],
                additional_description,
                notes_title,
                processing_description,
            ]
        )
        df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
        df_tables.loc[
            j, "dataPublishedBy"
        ] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, "unit"] = np.nan
        df_tables.loc[j, "shortUnit"] = np.nan
        df_tables.loc[j, "tolerance"] = 5
        df_tables.loc[j, "type"] = "Numeric"
        df_tables.loc[j, "colorScaleNumericMinValue"] = 0
        df_tables.loc[
            j, "colorScaleNumericBins"
        ] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables.loc[j, "colorScaleScheme"] = "Reds"
        df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
        j += 1

    # Number (2017)
    for p_2017 in range(len(povlines_ppp2017)):
        df_tables.loc[
            j, "name"
        ] = f"Number of people below ${povlines_ppp2017.dollars_text[p_2017]} a day (2017 prices)"
        df_tables.loc[j, "slug"] = f"headcount_{povlines_ppp2017.cents[p_2017]}_ppp2017"
        df_tables.loc[
            j, "sourceName"
        ] = "World Bank Poverty and Inequality Platform (2022)"
        df_tables.loc[j, "description"] = new_line.join(
            [
                f"Number of people living in households with an {survey_type.text[survey]} per person below ${povlines_ppp2017.dollars_text[p_2017]} a day (2017 prices).",
                ppp_description_2017,
                survey_type.description[survey],
                additional_description,
                notes_title,
                processing_description,
            ]
        )
        df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
        df_tables.loc[
            j, "dataPublishedBy"
        ] = "World Bank Poverty and Inequality Platform (PIP)"
        df_tables.loc[j, "unit"] = np.nan
        df_tables.loc[j, "shortUnit"] = np.nan
        df_tables.loc[j, "tolerance"] = 5
        df_tables.loc[j, "type"] = "Numeric"
        df_tables.loc[j, "colorScaleNumericMinValue"] = 0
        df_tables.loc[
            j, "colorScaleNumericBins"
        ] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables.loc[j, "colorScaleScheme"] = "Reds"
        df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
        j += 1

    # Share (relative, 2011)
    for pct in range(len(povlines_rel)):
        df_tables.loc[
            j, "name"
        ] = f"{povlines_rel.percent[pct]} of median - share of population below poverty line (2011 prices)"
        df_tables.loc[
            j, "slug"
        ] = f"headcount_ratio_{povlines_rel.slug_suffix[pct]}_ppp2011"
        df_tables.loc[
            j, "sourceName"
        ] = "World Bank Poverty and Inequality Platform (2022)"
        df_tables.loc[j, "description"] = new_line.join(
            [
                f"% of population living in households with an {survey_type.text[survey]} per person below {povlines_rel.percent[pct]} of the median (2011 prices).",
                survey_type.description[survey],
                additional_description,
                notes_title,
                processing_description,
            ]
        )
        df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
        df_tables.loc[
            j, "dataPublishedBy"
        ] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
        df_tables.loc[j, "unit"] = "%"
        df_tables.loc[j, "shortUnit"] = "%"
        df_tables.loc[j, "tolerance"] = 5
        df_tables.loc[j, "type"] = "Numeric"
        df_tables.loc[j, "colorScaleNumericMinValue"] = 0
        df_tables.loc[j, "colorScaleNumericBins"] = "5;10;15;20;25;30;30.0001"
        df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables.loc[j, "colorScaleScheme"] = "YlOrBr"
        df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
        j += 1

    # Share (relative, 2017)
    for pct in range(len(povlines_rel)):
        df_tables.loc[
            j, "name"
        ] = f"{povlines_rel.percent[pct]} of median - share of population below poverty line (2017 prices)"
        df_tables.loc[
            j, "slug"
        ] = f"headcount_ratio_{povlines_rel.slug_suffix[pct]}_ppp2017"
        df_tables.loc[
            j, "sourceName"
        ] = "World Bank Poverty and Inequality Platform (2022)"
        df_tables.loc[j, "description"] = new_line.join(
            [
                f"% of population living in households with an {survey_type.text[survey]} per person below {povlines_rel.percent[pct]} of the median (2017 prices).",
                survey_type.description[survey],
                additional_description,
                notes_title,
                processing_description,
            ]
        )
        df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
        df_tables.loc[
            j, "dataPublishedBy"
        ] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
        df_tables.loc[j, "unit"] = "%"
        df_tables.loc[j, "shortUnit"] = "%"
        df_tables.loc[j, "tolerance"] = 5
        df_tables.loc[j, "type"] = "Numeric"
        df_tables.loc[j, "colorScaleNumericMinValue"] = 0
        df_tables.loc[j, "colorScaleNumericBins"] = "5;10;15;20;25;30;30.0001"
        df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables.loc[j, "colorScaleScheme"] = "YlOrBr"
        df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
        j += 1

    # Number (relative, 2011)
    for pct in range(len(povlines_rel)):
        df_tables.loc[
            j, "name"
        ] = f"{povlines_rel.percent[pct]} of median - total number of people below poverty line (2011 prices)"
        df_tables.loc[j, "slug"] = f"headcount_{povlines_rel.slug_suffix[pct]}_ppp2011"
        df_tables.loc[
            j, "sourceName"
        ] = "World Bank Poverty and Inequality Platform (2022)"
        df_tables.loc[j, "description"] = new_line.join(
            [
                f"Number of people living in households with an {survey_type.text[survey]} per person below {povlines_rel.percent[pct]} of the median (2011 prices).",
                survey_type.description[survey],
                additional_description,
                notes_title,
                processing_description,
            ]
        )
        df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
        df_tables.loc[
            j, "dataPublishedBy"
        ] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
        df_tables.loc[j, "unit"] = np.nan
        df_tables.loc[j, "shortUnit"] = np.nan
        df_tables.loc[j, "tolerance"] = 5
        df_tables.loc[j, "type"] = "Numeric"
        df_tables.loc[j, "colorScaleNumericMinValue"] = 0
        df_tables.loc[
            j, "colorScaleNumericBins"
        ] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables.loc[j, "colorScaleScheme"] = "YlOrRd"
        df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
        j += 1

    # Number (relative, 2017)
    for pct in range(len(povlines_rel)):
        df_tables.loc[
            j, "name"
        ] = f"{povlines_rel.percent[pct]} of median - total number of people below poverty line (2017 prices)"
        df_tables.loc[j, "slug"] = f"headcount_{povlines_rel.slug_suffix[pct]}_ppp2017"
        df_tables.loc[
            j, "sourceName"
        ] = "World Bank Poverty and Inequality Platform (2022)"
        df_tables.loc[j, "description"] = new_line.join(
            [
                f"Number of people living in households with an {survey_type.text[survey]} per person below {povlines_rel.percent[pct]} of the median (2017 prices).",
                survey_type.description[survey],
                additional_description,
                notes_title,
                processing_description,
            ]
        )
        df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
        df_tables.loc[
            j, "dataPublishedBy"
        ] = "World Bank Poverty and Inequality Platform (PIP), adapted by Our World in Data."
        df_tables.loc[j, "unit"] = np.nan
        df_tables.loc[j, "shortUnit"] = np.nan
        df_tables.loc[j, "tolerance"] = 5
        df_tables.loc[j, "type"] = "Numeric"
        df_tables.loc[j, "colorScaleNumericMinValue"] = 0
        df_tables.loc[
            j, "colorScaleNumericBins"
        ] = "100000;300000;1000000;3000000;10000000;30000000;100000000;300000000;1000000000;1000000001"
        df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables.loc[j, "colorScaleScheme"] = "YlOrRd"
        df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
        j += 1

    # Mean (2011)
    df_tables.loc[j, "name"] = f"Mean {survey_type.text[survey]} per day (2011 prices)"
    df_tables.loc[j, "slug"] = "mean_ppp2011"
    df_tables.loc[j, "sourceName"] = "World Bank Poverty and Inequality Platform (2022)"
    df_tables.loc[j, "description"] = new_line.join(
        [
            f"The mean level of {survey_type.text[survey]} per day (2011 prices).",
            ppp_description_2011,
            survey_type.description[survey],
            additional_description,
            notes_title,
            processing_description,
        ]
    )
    df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
    df_tables.loc[
        j, "dataPublishedBy"
    ] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, "unit"] = "international-$ at 2011 prices"
    df_tables.loc[j, "shortUnit"] = "$"
    df_tables.loc[j, "tolerance"] = 5
    df_tables.loc[j, "type"] = "Numeric"
    df_tables.loc[j, "colorScaleNumericMinValue"] = 0
    df_tables.loc[j, "colorScaleNumericBins"] = "1;2;5;10;20;50;50.0001"
    df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables.loc[j, "colorScaleScheme"] = "BuGn"
    df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # Mean (2017)
    df_tables.loc[j, "name"] = f"Mean {survey_type.text[survey]} per day (2017 prices)"
    df_tables.loc[j, "slug"] = "mean_ppp2017"
    df_tables.loc[j, "sourceName"] = "World Bank Poverty and Inequality Platform (2022)"
    df_tables.loc[j, "description"] = new_line.join(
        [
            f"The mean level of {survey_type.text[survey]} per day (2017 prices).",
            ppp_description_2017,
            survey_type.description[survey],
            additional_description,
            notes_title,
            processing_description,
        ]
    )
    df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
    df_tables.loc[
        j, "dataPublishedBy"
    ] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, "unit"] = "international-$ in 2017 prices"
    df_tables.loc[j, "shortUnit"] = "$"
    df_tables.loc[j, "tolerance"] = 5
    df_tables.loc[j, "type"] = "Numeric"
    df_tables.loc[j, "colorScaleNumericMinValue"] = 0
    df_tables.loc[j, "colorScaleNumericBins"] = "1;2;5;10;20;50;50.0001"
    df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables.loc[j, "colorScaleScheme"] = "BuGn"
    df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # Median (2011)
    df_tables.loc[
        j, "name"
    ] = f"Median {survey_type.text[survey]} per day (2011 prices)"
    df_tables.loc[j, "slug"] = "median_ppp2011"
    df_tables.loc[j, "sourceName"] = "World Bank Poverty and Inequality Platform (2022)"
    df_tables.loc[j, "description"] = new_line.join(
        [
            f"The level of {survey_type.text[survey]} per day below which half of the population live (2011 prices).",
            ppp_description_2011,
            survey_type.description[survey],
            additional_description,
            notes_title,
            processing_description,
        ]
    )
    df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
    df_tables.loc[
        j, "dataPublishedBy"
    ] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, "unit"] = "international-$ at 2011 prices"
    df_tables.loc[j, "shortUnit"] = "$"
    df_tables.loc[j, "tolerance"] = 5
    df_tables.loc[j, "type"] = "Numeric"
    df_tables.loc[j, "colorScaleNumericMinValue"] = 0
    df_tables.loc[j, "colorScaleNumericBins"] = "1;2;5;10;20;50;50.0001"
    df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables.loc[j, "colorScaleScheme"] = "BuGn"
    df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # Median (2017)
    df_tables.loc[
        j, "name"
    ] = f"Median {survey_type.text[survey]} per day (2017 prices)"
    df_tables.loc[j, "slug"] = "median_ppp2017"
    df_tables.loc[j, "sourceName"] = "World Bank Poverty and Inequality Platform (2022)"
    df_tables.loc[j, "description"] = new_line.join(
        [
            f"The level of {survey_type.text[survey]} per day below which half of the population live (2017 prices).",
            ppp_description_2017,
            survey_type.description[survey],
            additional_description,
            notes_title,
            processing_description,
        ]
    )
    df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
    df_tables.loc[
        j, "dataPublishedBy"
    ] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, "unit"] = "international-$ in 2017 prices"
    df_tables.loc[j, "shortUnit"] = "$"
    df_tables.loc[j, "tolerance"] = 5
    df_tables.loc[j, "type"] = "Numeric"
    df_tables.loc[j, "colorScaleNumericMinValue"] = 0
    df_tables.loc[j, "colorScaleNumericBins"] = "1;2;5;10;20;50;50.0001"
    df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables.loc[j, "colorScaleScheme"] = "BuGn"
    df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # P10 (2011)
    df_tables.loc[j, "name"] = "P10 (2011 prices)"
    df_tables.loc[j, "slug"] = "decile1_thr_ppp2011"
    df_tables.loc[j, "sourceName"] = "World Bank Poverty and Inequality Platform (2022)"
    df_tables.loc[j, "description"] = new_line.join(
        [
            f"The level of {survey_type.text[survey]} per day below which 10% of the population falls (2011 prices).",
            ppp_description_2011,
            survey_type.description[survey],
            additional_description,
            notes_title,
            processing_description,
        ]
    )
    df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
    df_tables.loc[
        j, "dataPublishedBy"
    ] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, "unit"] = "international-$ at 2011 prices"
    df_tables.loc[j, "shortUnit"] = "$"
    df_tables.loc[j, "tolerance"] = 5
    df_tables.loc[j, "type"] = "Numeric"
    df_tables.loc[j, "colorScaleNumericMinValue"] = 0
    df_tables.loc[j, "colorScaleNumericBins"] = "1;2;5;10;20;20.0001"
    df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables.loc[j, "colorScaleScheme"] = "Greens"
    df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # P10 (2017)
    df_tables.loc[j, "name"] = "P10 (2017 prices)"
    df_tables.loc[j, "slug"] = "decile1_thr_ppp2017"
    df_tables.loc[j, "sourceName"] = "World Bank Poverty and Inequality Platform (2022)"
    df_tables.loc[j, "description"] = new_line.join(
        [
            f"The level of {survey_type.text[survey]} per day below which 10% of the population falls (2017 prices).",
            ppp_description_2017,
            survey_type.description[survey],
            additional_description,
            notes_title,
            processing_description,
        ]
    )
    df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
    df_tables.loc[
        j, "dataPublishedBy"
    ] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, "unit"] = "international-$ in 2017 prices"
    df_tables.loc[j, "shortUnit"] = "$"
    df_tables.loc[j, "tolerance"] = 5
    df_tables.loc[j, "type"] = "Numeric"
    df_tables.loc[j, "colorScaleNumericMinValue"] = 0
    df_tables.loc[j, "colorScaleNumericBins"] = "1;2;5;10;20;20.0001"
    df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables.loc[j, "colorScaleScheme"] = "Greens"
    df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # P90 (2011)
    df_tables.loc[j, "name"] = "P90 (2011 prices)"
    df_tables.loc[j, "slug"] = "decile9_thr_ppp2011"
    df_tables.loc[j, "sourceName"] = "World Bank Poverty and Inequality Platform (2022)"
    df_tables.loc[j, "description"] = new_line.join(
        [
            f"The level of {survey_type.text[survey]} per day below which 90% of the population falls (2011 prices).",
            ppp_description_2011,
            survey_type.description[survey],
            additional_description,
            notes_title,
            processing_description,
        ]
    )
    df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
    df_tables.loc[
        j, "dataPublishedBy"
    ] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, "unit"] = "international-$ at 2011 prices"
    df_tables.loc[j, "shortUnit"] = "$"
    df_tables.loc[j, "tolerance"] = 5
    df_tables.loc[j, "type"] = "Numeric"
    df_tables.loc[j, "colorScaleNumericMinValue"] = 0
    df_tables.loc[j, "colorScaleNumericBins"] = "5;10;20;50;100;100.0001"
    df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables.loc[j, "colorScaleScheme"] = "Blues"
    df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # P90 (2017)
    df_tables.loc[j, "name"] = "P90 (2017 prices)"
    df_tables.loc[j, "slug"] = "decile9_thr_ppp2017"
    df_tables.loc[j, "sourceName"] = "World Bank Poverty and Inequality Platform (2022)"
    df_tables.loc[j, "description"] = new_line.join(
        [
            f"The level of {survey_type.text[survey]} per day below which 90% of the population falls (2017 prices).",
            ppp_description_2017,
            survey_type.description[survey],
            additional_description,
            notes_title,
            processing_description,
        ]
    )
    df_tables.loc[j, "sourceLink"] = "https://pip.worldbank.org/"
    df_tables.loc[
        j, "dataPublishedBy"
    ] = "World Bank Poverty and Inequality Platform (PIP)"
    df_tables.loc[j, "unit"] = "international-$ in 2017 prices"
    df_tables.loc[j, "shortUnit"] = "$"
    df_tables.loc[j, "tolerance"] = 5
    df_tables.loc[j, "type"] = "Numeric"
    df_tables.loc[j, "colorScaleNumericMinValue"] = 0
    df_tables.loc[j, "colorScaleNumericBins"] = "5;10;20;50;100;100.0001"
    df_tables.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables.loc[j, "colorScaleScheme"] = "Blues"
    df_tables.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

# Make tolerance integer (to not break the parameter in the platform)
df_tables["tolerance"] = df_tables["tolerance"].astype("Int64")

# %% [markdown]
# ## Grapher views
# Similar to the tables, this creates the grapher views by grouping by types of variables and then running by survey type and poverty lines.

# %%
# Grapher table generation

df_graphers = pd.DataFrame()

j = 0

for survey in range(len(survey_type)):
    # Share (2011)
    for p_2011 in range(len(povlines_ppp2011)):
        df_graphers.loc[j, "title"] = f"{povlines_ppp2011.title_share[p_2011]}"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"headcount_ratio_{povlines_ppp2011.cents[p_2011]}_ppp2011"
        df_graphers.loc[j, "Indicator Dropdown"] = "Share in poverty"
        df_graphers.loc[j, "International-$ Dropdown"] = "2011 prices"
        df_graphers.loc[
            j, "Poverty line Dropdown"
        ] = f"{povlines_ppp2011.povline_dropdown[p_2011]}"
        df_graphers.loc[
            j, "Household survey data type Dropdown"
        ] = f"{survey_type.dropdown_option[survey]}"
        df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
        df_graphers.loc[j, "subtitle"] = f"{povlines_ppp2011.subtitle[p_2011]}"
        df_graphers.loc[
            j, "note"
        ] = f"This data is expressed in international-$ at 2011 prices. Depending on the country and year, it relates to {survey_type.detailed_text[survey]} per capita."
        df_graphers.loc[j, "type"] = np.nan
        df_graphers.loc[j, "yAxisMin"] = 0
        df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers.loc[j, "hasMapTab"] = "true"
        df_graphers.loc[j, "tab"] = "map"
        df_graphers.loc[j, "mapTargetTime"] = 2019
        df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
        j += 1

    # Share (2017)
    for p_2017 in range(len(povlines_ppp2017)):
        df_graphers.loc[j, "title"] = f"{povlines_ppp2017.title_share[p_2017]}"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"headcount_ratio_{povlines_ppp2017.cents[p_2017]}_ppp2017"
        df_graphers.loc[j, "Indicator Dropdown"] = "Share in poverty"
        df_graphers.loc[j, "International-$ Dropdown"] = "2017 prices"
        df_graphers.loc[
            j, "Poverty line Dropdown"
        ] = f"{povlines_ppp2017.povline_dropdown[p_2017]}"
        df_graphers.loc[
            j, "Household survey data type Dropdown"
        ] = f"{survey_type.dropdown_option[survey]}"
        df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
        df_graphers.loc[j, "subtitle"] = f"{povlines_ppp2017.subtitle[p_2017]}"
        df_graphers.loc[
            j, "note"
        ] = f"This data is expressed in international-$ at 2017 prices. Depending on the country and year, it relates to {survey_type.detailed_text[survey]} per capita."
        df_graphers.loc[j, "type"] = np.nan
        df_graphers.loc[j, "yAxisMin"] = 0
        df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers.loc[j, "hasMapTab"] = "true"
        df_graphers.loc[j, "tab"] = "map"
        df_graphers.loc[j, "mapTargetTime"] = 2019
        df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
        j += 1

    # Number (2011)
    for p_2011 in range(len(povlines_ppp2011)):
        df_graphers.loc[j, "title"] = f"{povlines_ppp2011.title_number[p_2011]}"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"headcount_{povlines_ppp2011.cents[p_2011]}_ppp2011"
        df_graphers.loc[j, "Indicator Dropdown"] = "Number in poverty"
        df_graphers.loc[j, "International-$ Dropdown"] = "2011 prices"
        df_graphers.loc[
            j, "Poverty line Dropdown"
        ] = f"{povlines_ppp2011.povline_dropdown[p_2011]}"
        df_graphers.loc[
            j, "Household survey data type Dropdown"
        ] = f"{survey_type.dropdown_option[survey]}"
        df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
        df_graphers.loc[j, "subtitle"] = f"{povlines_ppp2011.subtitle[p_2011]}"
        df_graphers.loc[
            j, "note"
        ] = f"This data is expressed in international-$ at 2011 prices. Depending on the country and year, it relates to {survey_type.detailed_text[survey]} per capita."
        df_graphers.loc[j, "type"] = np.nan
        df_graphers.loc[j, "yAxisMin"] = 0
        df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers.loc[j, "hasMapTab"] = "true"
        df_graphers.loc[j, "tab"] = "map"
        df_graphers.loc[j, "mapTargetTime"] = 2019
        df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
        j += 1

    # Number (2017)
    for p_2017 in range(len(povlines_ppp2017)):
        df_graphers.loc[j, "title"] = f"{povlines_ppp2017.title_number[p_2017]}"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"headcount_{povlines_ppp2017.cents[p_2017]}_ppp2017"
        df_graphers.loc[j, "Indicator Dropdown"] = "Number in poverty"
        df_graphers.loc[j, "International-$ Dropdown"] = "2017 prices"
        df_graphers.loc[
            j, "Poverty line Dropdown"
        ] = f"{povlines_ppp2017.povline_dropdown[p_2017]}"
        df_graphers.loc[
            j, "Household survey data type Dropdown"
        ] = f"{survey_type.dropdown_option[survey]}"
        df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
        df_graphers.loc[j, "subtitle"] = f"{povlines_ppp2017.subtitle[p_2017]}"
        df_graphers.loc[
            j, "note"
        ] = f"This data is expressed in international-$ at 2017 prices. Depending on the country and year, it relates to {survey_type.detailed_text[survey]} per capita."
        df_graphers.loc[j, "type"] = np.nan
        df_graphers.loc[j, "yAxisMin"] = 0
        df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers.loc[j, "hasMapTab"] = "true"
        df_graphers.loc[j, "tab"] = "map"
        df_graphers.loc[j, "mapTargetTime"] = 2019
        df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
        j += 1

    # Share (2011 and 2017)
    for p in range(len(povlines_both)):
        df_graphers.loc[j, "title"] = f"{povlines_both.title_share[p]}"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"headcount_ratio_{povlines_both.cents_2011[p]}_ppp2011 headcount_ratio_{povlines_both.cents_2017[p]}_ppp2017"
        df_graphers.loc[j, "Indicator Dropdown"] = "Share in poverty"
        df_graphers.loc[j, "International-$ Dropdown"] = "Compare 2017 and 2011 prices"
        df_graphers.loc[
            j, "Poverty line Dropdown"
        ] = f"{povlines_both.povline_dropdown[p]}"
        df_graphers.loc[
            j, "Household survey data type Dropdown"
        ] = f"{survey_type.dropdown_option[survey]}"
        df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
        df_graphers.loc[j, "subtitle"] = f"{povlines_both.subtitle[p]}"
        df_graphers.loc[
            j, "note"
        ] = f"Depending on the country and year, the data relates to {survey_type.detailed_text[survey]} per capita."
        df_graphers.loc[j, "type"] = np.nan
        df_graphers.loc[j, "yAxisMin"] = 0
        df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        df_graphers.loc[j, "hasMapTab"] = np.nan
        df_graphers.loc[j, "tab"] = np.nan
        df_graphers.loc[j, "mapTargetTime"] = np.nan
        df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
        j += 1

    # Number (2011 and 2017)
    for p in range(len(povlines_both)):
        df_graphers.loc[j, "title"] = f"{povlines_both.title_number[p]}"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"headcount_{povlines_both.cents_2011[p]}_ppp2011 headcount_{povlines_both.cents_2017[p]}_ppp2017"
        df_graphers.loc[j, "Indicator Dropdown"] = "Number in poverty"
        df_graphers.loc[j, "International-$ Dropdown"] = "Compare 2017 and 2011 prices"
        df_graphers.loc[
            j, "Poverty line Dropdown"
        ] = f"{povlines_both.povline_dropdown[p]}"
        df_graphers.loc[
            j, "Household survey data type Dropdown"
        ] = f"{survey_type.dropdown_option[survey]}"
        df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
        df_graphers.loc[j, "subtitle"] = f"{povlines_both.subtitle[p]}"
        df_graphers.loc[
            j, "note"
        ] = f"Depending on the country and year, the data relates to {survey_type.detailed_text[survey]} per capita."
        df_graphers.loc[j, "type"] = np.nan
        df_graphers.loc[j, "yAxisMin"] = 0
        df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
        df_graphers.loc[j, "hasMapTab"] = np.nan
        df_graphers.loc[j, "tab"] = np.nan
        df_graphers.loc[j, "mapTargetTime"] = np.nan
        df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
        j += 1

    # Share (relative, 2011)
    for pct in range(len(povlines_rel)):
        df_graphers.loc[j, "title"] = f"{povlines_rel.title_share[pct]} (2011 prices)"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"headcount_ratio_{povlines_rel.slug_suffix[pct]}_ppp2011"
        df_graphers.loc[j, "Indicator Dropdown"] = "Share in poverty"
        df_graphers.loc[j, "International-$ Dropdown"] = "2011 prices"
        df_graphers.loc[j, "Poverty line Dropdown"] = f"{povlines_rel.dropdown[pct]}"
        df_graphers.loc[
            j, "Household survey data type Dropdown"
        ] = f"{survey_type.dropdown_option[survey]}"
        df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
        df_graphers.loc[
            j, "subtitle"
        ] = f"Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel.text[pct]} {survey_type.text[survey]}."
        df_graphers.loc[
            j, "note"
        ] = f"Depending on the country and year, the data relates to {survey_type.detailed_text[survey]} per capita."
        df_graphers.loc[j, "type"] = np.nan
        df_graphers.loc[j, "yAxisMin"] = 0
        df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers.loc[j, "hasMapTab"] = "true"
        df_graphers.loc[j, "tab"] = "map"
        df_graphers.loc[j, "mapTargetTime"] = 2019
        df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
        j += 1

    # Share (relative, 2017)
    for pct in range(len(povlines_rel)):
        df_graphers.loc[j, "title"] = f"{povlines_rel.title_share[pct]} (2017 prices)"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"headcount_ratio_{povlines_rel.slug_suffix[pct]}_ppp2017"
        df_graphers.loc[j, "Indicator Dropdown"] = "Share in poverty"
        df_graphers.loc[j, "International-$ Dropdown"] = "2017 prices"
        df_graphers.loc[j, "Poverty line Dropdown"] = f"{povlines_rel.dropdown[pct]}"
        df_graphers.loc[
            j, "Household survey data type Dropdown"
        ] = f"{survey_type.dropdown_option[survey]}"
        df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
        df_graphers.loc[
            j, "subtitle"
        ] = f"Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel.text[pct]} {survey_type.text[survey]}."
        df_graphers.loc[
            j, "note"
        ] = f"Depending on the country and year, the data relates to {survey_type.detailed_text[survey]} per capita."
        df_graphers.loc[j, "type"] = np.nan
        df_graphers.loc[j, "yAxisMin"] = 0
        df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers.loc[j, "hasMapTab"] = "true"
        df_graphers.loc[j, "tab"] = "map"
        df_graphers.loc[j, "mapTargetTime"] = 2019
        df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
        j += 1

    # Number (relative, 2011)
    for pct in range(len(povlines_rel)):
        df_graphers.loc[j, "title"] = f"{povlines_rel.title_number[pct]} (2011 prices)"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"headcount_{povlines_rel.slug_suffix[pct]}_ppp2011"
        df_graphers.loc[j, "Indicator Dropdown"] = "Number in poverty"
        df_graphers.loc[j, "International-$ Dropdown"] = "2011 prices"
        df_graphers.loc[j, "Poverty line Dropdown"] = f"{povlines_rel.dropdown[pct]}"
        df_graphers.loc[
            j, "Household survey data type Dropdown"
        ] = f"{survey_type.dropdown_option[survey]}"
        df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
        df_graphers.loc[
            j, "subtitle"
        ] = f"Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel.text[pct]} {survey_type.text[survey]}."
        df_graphers.loc[
            j, "note"
        ] = f"Depending on the country and year, the data relates to {survey_type.detailed_text[survey]} per capita."
        df_graphers.loc[j, "type"] = np.nan
        df_graphers.loc[j, "yAxisMin"] = 0
        df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers.loc[j, "hasMapTab"] = "true"
        df_graphers.loc[j, "tab"] = "map"
        df_graphers.loc[j, "mapTargetTime"] = 2019
        df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
        j += 1

    # Number (relative, 2017)
    for pct in range(len(povlines_rel)):
        df_graphers.loc[j, "title"] = f"{povlines_rel.title_number[pct]} (2017 prices)"
        df_graphers.loc[
            j, "ySlugs"
        ] = f"headcount_{povlines_rel.slug_suffix[pct]}_ppp2017"
        df_graphers.loc[j, "Indicator Dropdown"] = "Number in poverty"
        df_graphers.loc[j, "International-$ Dropdown"] = "2017 prices"
        df_graphers.loc[j, "Poverty line Dropdown"] = f"{povlines_rel.dropdown[pct]}"
        df_graphers.loc[
            j, "Household survey data type Dropdown"
        ] = f"{survey_type.dropdown_option[survey]}"
        df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
        df_graphers.loc[
            j, "subtitle"
        ] = f"Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at {povlines_rel.text[pct]} {survey_type.text[survey]}."
        df_graphers.loc[
            j, "note"
        ] = f"Depending on the country and year, the data relates to {survey_type.detailed_text[survey]} per capita."
        df_graphers.loc[j, "type"] = np.nan
        df_graphers.loc[j, "yAxisMin"] = 0
        df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers.loc[j, "hasMapTab"] = "true"
        df_graphers.loc[j, "tab"] = "map"
        df_graphers.loc[j, "mapTargetTime"] = 2019
        df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
        j += 1

    # Share (relative, 2011 vs 2017)
    df_graphers.loc[
        j, "title"
    ] = f"Relative poverty: Share of people below 60% of the median (2011 vs. 2017 prices)"
    df_graphers.loc[
        j, "ySlugs"
    ] = f"headcount_ratio_60_median_ppp2011 headcount_ratio_60_median_ppp2017"
    df_graphers.loc[j, "Indicator Dropdown"] = "Share in poverty"
    df_graphers.loc[j, "International-$ Dropdown"] = "Compare 2017 and 2011 prices"
    df_graphers.loc[j, "Poverty line Dropdown"] = f"Relative poverty: 60% of median"
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = f"Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at 60% of the median {survey_type.text[survey]}."
    df_graphers.loc[
        j, "note"
    ] = f"Depending on the country and year, the data relates to {survey_type.detailed_text[survey]} per capita."
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
    df_graphers.loc[j, "hasMapTab"] = np.nan
    df_graphers.loc[j, "tab"] = np.nan
    df_graphers.loc[j, "mapTargetTime"] = np.nan
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # Number (relative, 2011 vs 2017)
    df_graphers.loc[
        j, "title"
    ] = f"Relative poverty: Number of people below 60% of the median (2011 vs. 2017 prices)"
    df_graphers.loc[
        j, "ySlugs"
    ] = f"headcount_60_median_ppp2011 headcount_60_median_ppp2017"
    df_graphers.loc[j, "Indicator Dropdown"] = "Number in poverty"
    df_graphers.loc[j, "International-$ Dropdown"] = "Compare 2017 and 2011 prices"
    df_graphers.loc[j, "Poverty line Dropdown"] = f"Relative poverty: 60% of median"
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = f"Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at 60% of the median {survey_type.text[survey]}."
    df_graphers.loc[
        j, "note"
    ] = f"Depending on the country and year, the data relates to {survey_type.detailed_text[survey]} per capita."
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
    df_graphers.loc[j, "hasMapTab"] = np.nan
    df_graphers.loc[j, "tab"] = np.nan
    df_graphers.loc[j, "mapTargetTime"] = np.nan
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # Mean (2011)
    df_graphers.loc[
        j, "title"
    ] = f"Mean {survey_type.text[survey]} per day (2011 prices)"
    df_graphers.loc[j, "ySlugs"] = "mean_ppp2011"
    df_graphers.loc[j, "Indicator Dropdown"] = "Mean income or consumption"
    df_graphers.loc[j, "International-$ Dropdown"] = "2011 prices"
    df_graphers.loc[j, "Poverty line Dropdown"] = np.nan
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df_graphers.loc[
        j, "note"
    ] = f"This data is expressed in international-$ at 2011 prices. Depending on the country and year, it relates to {survey_type.detailed_text[survey]} per capita."
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers.loc[j, "hasMapTab"] = "true"
    df_graphers.loc[j, "tab"] = "map"
    df_graphers.loc[j, "mapTargetTime"] = 2019
    df_graphers.loc[j, "yScaleToggle"] = "true"
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # Mean (2017)
    df_graphers.loc[
        j, "title"
    ] = f"Mean {survey_type.text[survey]} per day (2017 prices)"
    df_graphers.loc[j, "ySlugs"] = "mean_ppp2017"
    df_graphers.loc[j, "Indicator Dropdown"] = "Mean income or consumption"
    df_graphers.loc[j, "International-$ Dropdown"] = "2017 prices"
    df_graphers.loc[j, "Poverty line Dropdown"] = np.nan
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df_graphers.loc[
        j, "note"
    ] = f"This data is expressed in international-$ at 2017 prices. Depending on the country and year, it relates to {survey_type.detailed_text[survey]} per capita."
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers.loc[j, "hasMapTab"] = "true"
    df_graphers.loc[j, "tab"] = "map"
    df_graphers.loc[j, "mapTargetTime"] = 2019
    df_graphers.loc[j, "yScaleToggle"] = "true"
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # Mean (2011, 2017)
    df_graphers.loc[
        j, "title"
    ] = f"Mean {survey_type.text[survey]} per day: 2011 vs. 2017 prices"
    df_graphers.loc[j, "ySlugs"] = "mean_ppp2011 mean_ppp2017"
    df_graphers.loc[j, "Indicator Dropdown"] = "Mean income or consumption"
    df_graphers.loc[j, "International-$ Dropdown"] = "Compare 2017 and 2011 prices"
    df_graphers.loc[j, "Poverty line Dropdown"] = np.nan
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df_graphers.loc[
        j, "note"
    ] = f"Depending on the country and year, the data relates to {survey_type.detailed_text[survey]} per capita."
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
    df_graphers.loc[j, "hasMapTab"] = np.nan
    df_graphers.loc[j, "tab"] = np.nan
    df_graphers.loc[j, "mapTargetTime"] = np.nan
    df_graphers.loc[j, "yScaleToggle"] = "true"
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # Median (2011)
    df_graphers.loc[
        j, "title"
    ] = f"Median {survey_type.text[survey]} per day (2011 prices)"
    df_graphers.loc[j, "ySlugs"] = "median_ppp2011"
    df_graphers.loc[j, "Indicator Dropdown"] = "Median income or consumption"
    df_graphers.loc[j, "International-$ Dropdown"] = "2011 prices"
    df_graphers.loc[j, "Poverty line Dropdown"] = np.nan
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df_graphers.loc[
        j, "note"
    ] = f"This data is expressed in international-$ at 2011 prices. Depending on the country and year, it relates to {survey_type.detailed_text[survey]} per capita."
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers.loc[j, "hasMapTab"] = "true"
    df_graphers.loc[j, "tab"] = "map"
    df_graphers.loc[j, "mapTargetTime"] = 2019
    df_graphers.loc[j, "yScaleToggle"] = "true"
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # Median (2017)
    df_graphers.loc[
        j, "title"
    ] = f"Median {survey_type.text[survey]} per day (2017 prices)"
    df_graphers.loc[j, "ySlugs"] = "median_ppp2017"
    df_graphers.loc[j, "Indicator Dropdown"] = "Median income or consumption"
    df_graphers.loc[j, "International-$ Dropdown"] = "2017 prices"
    df_graphers.loc[j, "Poverty line Dropdown"] = np.nan
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df_graphers.loc[
        j, "note"
    ] = f"This data is expressed in international-$ at 2017 prices. Depending on the country and year, it relates to {survey_type.detailed_text[survey]} per capita."
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers.loc[j, "hasMapTab"] = "true"
    df_graphers.loc[j, "tab"] = "map"
    df_graphers.loc[j, "mapTargetTime"] = 2019
    df_graphers.loc[j, "yScaleToggle"] = "true"
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # Median (2011, 2017)
    df_graphers.loc[
        j, "title"
    ] = f"Median {survey_type.text[survey]} per day: 2011 vs. 2017 prices"
    df_graphers.loc[j, "ySlugs"] = "median_ppp2011 median_ppp2017"
    df_graphers.loc[j, "Indicator Dropdown"] = "Median income or consumption"
    df_graphers.loc[j, "International-$ Dropdown"] = "Compare 2017 and 2011 prices"
    df_graphers.loc[j, "Poverty line Dropdown"] = np.nan
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = "This data is adjusted for inflation and for differences in the cost of living between countries."
    df_graphers.loc[
        j, "note"
    ] = f"Depending on the country and year, the data relates to {survey_type.detailed_text[survey]} per capita."
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
    df_graphers.loc[j, "hasMapTab"] = np.nan
    df_graphers.loc[j, "tab"] = np.nan
    df_graphers.loc[j, "mapTargetTime"] = np.nan
    df_graphers.loc[j, "yScaleToggle"] = "true"
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # P10 (2011)
    df_graphers.loc[
        j, "title"
    ] = f"P10: The {survey_type.text[survey]} of the poorest tenth (2011 prices)"
    df_graphers.loc[j, "ySlugs"] = "decile1_thr_ppp2011"
    df_graphers.loc[j, "Indicator Dropdown"] = "P10 (poorest tenth)"
    df_graphers.loc[j, "International-$ Dropdown"] = "2011 prices"
    df_graphers.loc[j, "Poverty line Dropdown"] = np.nan
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = f"P10 is the level of {survey_type.text[survey]} per day below which 10% of the population falls."
    df_graphers.loc[
        j, "note"
    ] = f"This data is measured in international-$ at 2011 prices to account for inflation and differences in the cost of living between countries. Depending on the country and year, it relates to {survey_type.detailed_text[survey]} per capita."
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers.loc[j, "hasMapTab"] = "true"
    df_graphers.loc[j, "tab"] = "map"
    df_graphers.loc[j, "mapTargetTime"] = 2019
    df_graphers.loc[j, "yScaleToggle"] = "true"
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # P10 (2017)
    df_graphers.loc[
        j, "title"
    ] = f"P10: The {survey_type.text[survey]} of the poorest tenth (2017 prices)"
    df_graphers.loc[j, "ySlugs"] = "decile1_thr_ppp2017"
    df_graphers.loc[j, "Indicator Dropdown"] = "P10 (poorest tenth)"
    df_graphers.loc[j, "International-$ Dropdown"] = "2017 prices"
    df_graphers.loc[j, "Poverty line Dropdown"] = np.nan
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = f"P10 is the level of {survey_type.text[survey]} per day below which 10% of the population falls."
    df_graphers.loc[
        j, "note"
    ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. Depending on the country and year, it relates to {survey_type.detailed_text[survey]} per capita."
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers.loc[j, "hasMapTab"] = "true"
    df_graphers.loc[j, "tab"] = "map"
    df_graphers.loc[j, "mapTargetTime"] = 2019
    df_graphers.loc[j, "yScaleToggle"] = "true"
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # P10 (2011, 2017)
    df_graphers.loc[
        j, "title"
    ] = f"P10: The {survey_type.text[survey]} of the poorest tenth (2011 vs. 2017 prices)"
    df_graphers.loc[j, "ySlugs"] = "decile1_thr_ppp2011 decile1_thr_ppp2017"
    df_graphers.loc[j, "Indicator Dropdown"] = "P10 (poorest tenth)"
    df_graphers.loc[j, "International-$ Dropdown"] = "Compare 2017 and 2011 prices"
    df_graphers.loc[j, "Poverty line Dropdown"] = np.nan
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = f"P10 is the level of {survey_type.text[survey]} per day below which 10% of the population falls."
    df_graphers.loc[
        j, "note"
    ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. Depending on the country and year, it relates to {survey_type.detailed_text[survey]} per capita."
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
    df_graphers.loc[j, "hasMapTab"] = np.nan
    df_graphers.loc[j, "tab"] = np.nan
    df_graphers.loc[j, "mapTargetTime"] = np.nan
    df_graphers.loc[j, "yScaleToggle"] = "true"
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # P90 (2011)
    df_graphers.loc[
        j, "title"
    ] = f"P90: The {survey_type.text[survey]} of the richest tenth (2011 prices)"
    df_graphers.loc[j, "ySlugs"] = "decile9_thr_ppp2011"
    df_graphers.loc[j, "Indicator Dropdown"] = "P90 (richest tenth)"
    df_graphers.loc[j, "International-$ Dropdown"] = "2011 prices"
    df_graphers.loc[j, "Poverty line Dropdown"] = np.nan
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = f"P90 is the level of {survey_type.text[survey]} per day above which 10% of the population falls."
    df_graphers.loc[
        j, "note"
    ] = f"This data is measured in international-$ at 2011 prices to account for inflation and differences in the cost of living between countries. Depending on the country and year, it relates to {survey_type.detailed_text[survey]} per capita."
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers.loc[j, "hasMapTab"] = "true"
    df_graphers.loc[j, "tab"] = "map"
    df_graphers.loc[j, "mapTargetTime"] = 2019
    df_graphers.loc[j, "yScaleToggle"] = "true"
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # P90 (2017)
    df_graphers.loc[
        j, "title"
    ] = f"P90: The {survey_type.text[survey]} of the richest tenth (2017 prices)"
    df_graphers.loc[j, "ySlugs"] = "decile9_thr_ppp2017"
    df_graphers.loc[j, "Indicator Dropdown"] = "P90 (richest tenth)"
    df_graphers.loc[j, "International-$ Dropdown"] = "2017 prices"
    df_graphers.loc[j, "Poverty line Dropdown"] = np.nan
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = f"P90 is the level of {survey_type.text[survey]} per day above which 10% of the population falls."
    df_graphers.loc[
        j, "note"
    ] = f"This data is measured in international-$ at 2017 prices to account for inflation and differences in the cost of living between countries. Depending on the country and year, it relates to {survey_type.detailed_text[survey]} per capita."
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers.loc[j, "hasMapTab"] = "true"
    df_graphers.loc[j, "tab"] = "map"
    df_graphers.loc[j, "mapTargetTime"] = 2019
    df_graphers.loc[j, "yScaleToggle"] = "true"
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

    # P90 (2011, 2017)
    df_graphers.loc[
        j, "title"
    ] = f"P90: The {survey_type.text[survey]} of the richest tenth (2011 vs. 2017 prices)"
    df_graphers.loc[j, "ySlugs"] = "decile9_thr_ppp2011 decile9_thr_ppp2017"
    df_graphers.loc[j, "Indicator Dropdown"] = "P90 (richest tenth)"
    df_graphers.loc[j, "International-$ Dropdown"] = "Compare 2017 and 2011 prices"
    df_graphers.loc[j, "Poverty line Dropdown"] = np.nan
    df_graphers.loc[
        j, "Household survey data type Dropdown"
    ] = f"{survey_type.dropdown_option[survey]}"
    df_graphers.loc[j, "tableSlug"] = f"{survey_type.table_name[survey]}"
    df_graphers.loc[
        j, "subtitle"
    ] = f"P90 is the level of {survey_type.text[survey]} per day above which 10% of the population falls."
    df_graphers.loc[
        j, "note"
    ] = f"This data is adjusted for inflation and for differences in the cost of living between countries. Depending on the country and year, it relates to {survey_type.detailed_text[survey]} per capita."
    df_graphers.loc[j, "type"] = np.nan
    df_graphers.loc[j, "yAxisMin"] = 0
    df_graphers.loc[j, "selectedFacetStrategy"] = "entity"
    df_graphers.loc[j, "hasMapTab"] = np.nan
    df_graphers.loc[j, "tab"] = np.nan
    df_graphers.loc[j, "mapTargetTime"] = np.nan
    df_graphers.loc[j, "yScaleToggle"] = "true"
    df_graphers.loc[j, "survey_type"] = survey_type["table_name"][survey]
    j += 1

# %% [markdown]
# Final adjustments to the graphers table:

# %%
# Add PPP comparison article as related question link
df_graphers[
    "relatedQuestionText"
] = "From $1.90 to $2.15 a day: the updated International Poverty Line"
df_graphers[
    "relatedQuestionUrl"
] = "https://ourworldindata.org/from-1-90-to-2-15-a-day-the-updated-international-poverty-line"

# Make mapTargetTime integer (to not break the parameter in the platform)
df_graphers["mapTargetTime"] = df_graphers["mapTargetTime"].astype("Int64")

# Select one default view
df_graphers.loc[
    (df_graphers["ySlugs"] == "headcount_ratio_190_ppp2011 headcount_ratio_215_ppp2017")
    & (df_graphers["tableSlug"] == "inc_or_cons"),
    ["defaultView"],
] = "true"

# When the "Depending on" footnote is introduced, it generates unwanted texts as:
# "Depending on the country and year, the data relates to income measured after taxes and benefits per capita."
# "Depending on the country and year, the data relates to consumption per capita."

# When int-$ are not included
df_graphers["note"] = df_graphers["note"].str.replace(
    "Depending on the country and year, the data relates to income measured after taxes and benefits per capita.",
    "The data relates to income measured after taxes and benefits per capita.",
    regex=False,
)
df_graphers["note"] = df_graphers["note"].str.replace(
    "Depending on the country and year, the data relates to consumption per capita.",
    "The data relates to consumption per capita.",
    regex=False,
)

# When int-$ are included
df_graphers["note"] = df_graphers["note"].str.replace(
    "Depending on the country and year, it relates to income measured after taxes and benefits per capita.",
    "It relates to income measured after taxes and benefits per capita.",
    regex=False,
)
df_graphers["note"] = df_graphers["note"].str.replace(
    "Depending on the country and year, it relates to consumption per capita.",
    "It relates to consumption per capita.",
    regex=False,
)

# Reorder dropdown menus
povline_dropdown_list = [
    "$1.90 per day: International Poverty Line",
    "$2.15 per day: International Poverty Line",
    "$3.20 per day: Lower-middle income poverty line",
    "$3.65 per day: Lower-middle income poverty line",
    "$5.50 per day: Upper-middle income poverty line",
    "$6.85 per day: Upper-middle income poverty line",
    "$1 per day",
    "$10 per day",
    "$20 per day",
    "$30 per day",
    "$40 per day",
    "International Poverty Line",
    "Lower-middle income poverty line",
    "Upper-middle income poverty line",
    "Relative poverty: 40% of median",
    "Relative poverty: 50% of median",
    "Relative poverty: 60% of median",
]


df_graphers_mapping = pd.DataFrame(
    {
        "povline_dropdown": povline_dropdown_list,
    }
)
df_graphers_mapping = df_graphers_mapping.reset_index().set_index("povline_dropdown")

df_graphers["povline_dropdown_aux"] = df_graphers["Poverty line Dropdown"].map(
    df_graphers_mapping["index"]
)
df_graphers = df_graphers.sort_values("povline_dropdown_aux", ignore_index=True)
df_graphers = df_graphers.drop(columns=["povline_dropdown_aux"])

# %% [markdown]
# ## Explorer generation
# Here, the header, tables and graphers dataframes are combined to be shown in for format required for OWID data explorers.

# %%
# Define list of variables to iterate: survey types
survey_list = list(survey_type["table_name"].unique())

# Header is converted into a tab-separated text
header_tsv = df_header.to_csv(sep="\t", header=False)

# Auxiliar variable `survey_type` is dropped and graphers table is converted into a tab-separated text
graphers_tsv = df_graphers.drop(columns=["survey_type"])
graphers_tsv = graphers_tsv.to_csv(sep="\t", index=False)

# This table is indented, to follow explorers' format
graphers_tsv_indented = textwrap.indent(graphers_tsv, "\t")

# The dataframes are combined, including tables which are filtered by survey type and variable
with open(outfile, "w", newline="\n", encoding="utf-8") as f:
    f.write(header_tsv)
    f.write("\ngraphers\n" + graphers_tsv_indented)

    for i in survey_list:
        table_tsv = (
            df_tables[df_tables["survey_type"] == i].copy().reset_index(drop=True)
        )
        table_tsv = table_tsv.drop(columns=["survey_type"])
        table_tsv = table_tsv.to_csv(sep="\t", index=False)
        table_tsv_indented = textwrap.indent(table_tsv, "\t")
        f.write(
            "\ntable\t"
            + "https://raw.githubusercontent.com/owid/notebooks/main/BetterDataDocs/JoeHasell/PIP/data/ppp_vs/final/OWID_internal_upload/explorer_database/"
            + i
            + "/poverty_"
            + i
            + ".csv\t"
            + i
        )
        f.write("\ncolumns\t" + i + "\n" + table_tsv_indented)
