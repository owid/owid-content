# NOTE: Don't forget to update the consumption and income spells for PIP

####################################################################################################
# COMMON PARAMETERS BETWEEN SOURCES
####################################################################################################
COLOR_SCALE_NUMERIC_MIN_VALUE = 0
TOLERANCE = 5
COLOR_SCALE_EQUAL_SIZEBINS = "true"
NEW_LINE = "\\n\\n"
Y_AXIS_MIN = 0
MAP_TARGET_TIME = 0

####################################################################################################
# WORLD BANK POVERTY AND INEQUALITY PLATFORM
####################################################################################################
SOURCE_NAME_PIP = "World Bank Poverty and Inequality Platform (2024)"
DATA_PUBLISHED_BY_PIP = "World Bank (2024). Poverty and Inequality Platform (version 20240326_2017 and 20240326_2011) [Data set]. World Bank Group. https://pip.worldbank.org/. Accessed March 27, 2024."
SOURCE_LINK_PIP = "https://pip.worldbank.org"
CONSUMPTION_SPELLS_PIP = 7
INCOME_SPELLS_PIP = 8


INCOME_OR_CONSUMPTION_PIP = "Depending on the country and year, the data relates to income measured after taxes and benefits, or to consumption, per capita. 'Per capita' means that the incomes of each household are attributed equally to each member of the household (including children)."
NON_MARKET_DESCRIPTION_PIP = "Non-market sources of income, including food grown by subsistence farmers for their own consumption, are taken into account."

# NOTE: Here income or consumption description depends on the welfare type and it is defined in the Google sheet
ADDITIONAL_DESCRIPTION_PIP = NEW_LINE.join(
    [
        NON_MARKET_DESCRIPTION_PIP,
    ]
)

ADDITIONAL_DESCRIPTION_PIP_COMPARISON = NEW_LINE.join(
    [
        INCOME_OR_CONSUMPTION_PIP,
        NON_MARKET_DESCRIPTION_PIP,
    ]
)

NOTES_TITLE_PIP = "NOTES ON HOW WE PROCESSED THIS INDICATOR"

PROCESSING_DESCRIPTION_PIP_BASE = NEW_LINE.join(
    [
        "For most countries in the PIP dataset, estimates relate to _either_ disposable income or consumption, for all available years. A number of countries, however, have a mix of income and consumption data points, with both data types sometimes available for particular years.",
        "In most of our charts, we present the data with some data points dropped in order to present single series for each country. This allows us to make readable visualizations that combine multiple countries and metrics. In choosing which data points to drop, we try to strike a balance between maintaining comparability over time and showing as long a time series as possible. As such, the exact approach varies somewhat across countries.",
    ]
)

PROCESSING_DESCRIPTION_PIP = NEW_LINE.join(
    [
        PROCESSING_DESCRIPTION_PIP_BASE,
        "If you would like to see the original data with _all_ available income and consumption data points shown separately, you can do so by selecting _Income surveys only_ or _Consumption surveys only_ in the Household survey data type dropdown or by clicking on _Show breaks between less comparable surveys_. You can also download this data in our [complete dataset](https://github.com/owid/poverty-data#a-global-dataset-of-poverty-and-inequality-measures-prepared-by-our-world-in-data-from-the-world-banks-poverty-and-inequality-platform-pip-database) of the World Bank PIP data.",
    ]
)

PROCESSING_DESCRIPTION_PIP_PPP_COMPARISON = NEW_LINE.join(
    [
        PROCESSING_DESCRIPTION_PIP_BASE,
        "If you would like to see the original data with _all_ available income and consumption data points shown separately, you can do so in our [Poverty Data Explorer](https://ourworldindata.org/explorers/poverty-explorer?Indicator=Share+in+poverty&Poverty+line=%2410+per+day&Household+survey+data+type=Show+data+from+both+income+and+consumption+surveys&Show+breaks+between+less+comparable+surveys=true&country=ROU~CHN~BLR~PER). You can also download this data in our [complete dataset](https://github.com/owid/poverty-data#a-global-dataset-of-poverty-and-inequality-measures-prepared-by-our-world-in-data-from-the-world-banks-poverty-and-inequality-platform-pip-database) of the World Bank PIP data.",
    ]
)

PROCESSING_DESCRIPTION_PIP_INCOMES_ACROSS_DISTRIBUTION = NEW_LINE.join(
    [
        PROCESSING_DESCRIPTION_PIP_BASE,
        "If you would like to see the original data with _all_ available income and consumption data points shown separately, you can do so in our [Incomes Across the Distribution - World Bank Data Explorer](https://ourworldindata.org/explorers/incomes-across-distribution-wb?Indicator=Decile+thresholds&Decile=9+%28richest%29&Household+survey+data+type=Show+data+from+both+income+and+consumption+surveys&Period=Day&Show+breaks+between+less+comparable+surveys=true&country=ROU~CHN~BLR~PER). You can also download this data in our [complete dataset](https://github.com/owid/poverty-data#a-global-dataset-of-poverty-and-inequality-measures-prepared-by-our-world-in-data-from-the-world-banks-poverty-and-inequality-platform-pip-database) of the World Bank PIP data.",
    ]
)

PROCESSING_DESCRIPTION_PIP_INEQUALITY = NEW_LINE.join(
    [
        PROCESSING_DESCRIPTION_PIP_BASE,
        "If you would like to see the original data with _all_ available income and consumption data points shown separately, you can do so in our [Inequality - World Bank Data Explorer](https://ourworldindata.org/explorers/inequality-wb?country=ROU~CHN~BLR~PER&Indicator=Gini+coefficient&Household+survey+data+type=Show+data+from+both+income+and+consumption+surveys&Show+breaks+between+less+comparable+surveys=true). You can also download this data in our [complete dataset](https://github.com/owid/poverty-data#a-global-dataset-of-poverty-and-inequality-measures-prepared-by-our-world-in-data-from-the-world-banks-poverty-and-inequality-platform-pip-database) of the World Bank PIP data.",
    ]
)

PROCESSING_DESCRIPTION_PIP_POVERTY = NEW_LINE.join(
    [
        PROCESSING_DESCRIPTION_PIP_BASE,
        "If you would like to see the original data with _all_ available income and consumption data points shown separately, you can do so in our [Poverty - World Bank Data Explorer](https://ourworldindata.org/explorers/poverty-wb?Indicator=Share+in+poverty&Poverty+line=%2410+per+day&Household+survey+data+type=Show+data+from+both+income+and+consumption+surveys&Show+breaks+between+less+comparable+surveys=true&country=ROU~CHN~BLR~PER). You can also download this data in our [complete dataset](https://github.com/owid/poverty-data#a-global-dataset-of-poverty-and-inequality-measures-prepared-by-our-world-in-data-from-the-world-banks-poverty-and-inequality-platform-pip-database) of the World Bank PIP data.",
    ]
)

PPP_DESCRIPTION_PIP_2017 = "The data is measured in international-$ at 2017 prices – this adjusts for inflation and for differences in the cost of living between countries."
PPP_DESCRIPTION_PIP_2011 = "The data is measured in international-$ at 2011 prices – this adjusts for inflation and for differences in the cost of living between countries."

####################################################################################################
# WORLD INEQUALITY DATABASE
####################################################################################################
SOURCE_NAME_WID = "World Inequality Database (WID.world) (2024)"
DATA_PUBLISHED_BY_WID = "World Inequality Database (WID), https://wid.world"
SOURCE_LINK_WID = "https://wid.world"

# NOTE: Also update the year here: https://docs.google.com/spreadsheets/d/1wcFsNZCEn_6SJ05BFkXKLUyvCrnigfR8eeemGKgAYsI/edit#gid=329774797
PPP_YEAR_WID = 2023

ADDITIONAL_DESCRIPTION_WID = NEW_LINE.join(
    [
        "The data is estimated from a combination of household surveys, tax records and national accounts data. This combination can provide a more accurate picture of the incomes of the richest, which tend to be captured poorly in household survey data alone.",
        "These underlying data sources are not always available. For some countries, observations are extrapolated from data relating to other years, or are sometimes modeled based on data observed in other countries. For more information on this methodology, see this related [technical note](https://wid.world/document/countries-with-regional-income-imputations-on-wid-world-world-inequality-lab-technical-note-2021-15/).",
    ]
)
PPP_DESCRIPTION_WID = f"The data is measured in international-$ at {PPP_YEAR_WID} prices – this adjusts for inflation and for differences in the cost of living between countries."

####################################################################################################
# LUXEMBOURG INCOME STUDY
####################################################################################################
SOURCE_NAME_LIS = "Luxembourg Income Study (2023)"
DATA_PUBLISHED_BY_LIS = "Luxembourg Income Study (LIS) Database, http://www.lisdatacenter.org (multiple countries; 1967-2021). Luxembourg, LIS."
SOURCE_LINK_LIS = "https://www.lisdatacenter.org/our-data/lis-database/"

NOTES_TITLE_LIS = "NOTES ON HOW WE PROCESSED THIS INDICATOR"

PROCESSING_DESCRIPTION_LIS = NEW_LINE.join(
    [
        "The Luxembourg Income Study data is created from standardized household survey microdata available in their [LISSY platform](https://www.lisdatacenter.org/data-access/lissy/). The estimations follow the methodology available in LIS, Key Figures and DART platform.",
        "After tax income is obtained by using the disposable household income variable (dhi)",
        "Before tax income is estimated by calculating the sum of income from labor and capital (variable hifactor), cash transfers and in-kind goods and services from privates (hiprivate) and private pensions (hi33). This is done only for surveys where tax and contributions are fully captured, collected or imputed.",
        "Income data is converted from local currency into international-$ by dividing by the [LIS PPP factor](https://www.lisdatacenter.org/resources/ppp-deflators/), available as an additional database in the system.",
        "Incomes are top and bottom-coded by replacing negative values with zeros and setting boundaries for extreme values of log income: at the top Q3 plus 3 times the interquartile range (Q3-Q1), and at the bottom Q1 minus 3 times the interquartile range.",
        "Incomes are equivalized by dividing each household observation by the square root of the number of household members (nhhmem). Per capita estimates are calculated by dividing incomes by the number of household members.",
    ]
)

PROCESSING_POVERTY_LIS = "Poverty indicators are obtained by using [Stata’s povdeco function](https://ideas.repec.org/c/boc/bocode/s366004.html). Weights are set as the product between the number of household members (nhhmem) and the normalized household weight (hwgt). The function generates FGT(0) and FGT(1), headcount ratio and poverty gap index. After extraction, further data processing steps are done to estimate other poverty indicators using these values, population and poverty lines for absolute and relative poverty."
PROCESSING_GINI_MEAN_MEDIAN_LIS = "Gini coefficients are obtained by using [Stata’s ineqdec0 function](https://ideas.repec.org/c/boc/bocode/s366007.html). Weights are set as the product between the number of household members (nhhmem) and the normalized household weight (hwgt). From this function, mean and median values are also calculated."
PROCESSING_DISTRIBUTION_LIS = "Income shares and thresholds by decile are obtained by using [Stata’s sumdist function](https://ideas.repec.org/c/boc/bocode/s366005.html). The parameters set are again the weight (nhhmem*hwgt) and the number of quantile groups (10). Threshold ratios, share ratios and averages by decile are estimated after the use of LISSY with this data."

PPP_DESCRIPTION_LIS = "The data is measured in international-$ at 2017 prices – this adjusts for inflation and for differences in the cost of living between countries."


