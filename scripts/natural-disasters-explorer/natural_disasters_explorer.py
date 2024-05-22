"""This script creates the tsv file for the natural disasters explorer, which is an indicator-based explorer.

NOTE: 
* This script is quite messy, but it probably doesn't need to be used often (or ever again).
* This script needs to be executed using the ETL virtual environment.

"""

import MySQLdb
import os

from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

# MAIN INPUTS.
# Version of the latest natural disasters dataset.
VERSION = "2024-04-11"
# Date of the last disasters recorded in the dataset.
LAST_DISASTERS_DATE = "April 2024"

########################################################################################################################
# TODO: Currently, we can't set the missing data strategy in an indicator-based explorer. This causes stacked bar charts that use multiple variables to miss many data points (because the data is so sparse).
# For now, create a TEST explorer. Once this is fixed, replace the current explorer.
# OUTPUT_FILE = Path(__file__).parent.parent.parent / "explorers/natural-disasters.explorer.tsv"
OUTPUT_FILE = Path(__file__).parent.parent.parent / "explorers/natural-disasters-TEST.explorer.tsv"
########################################################################################################################
assert OUTPUT_FILE.parent.exists()

# Path to ETL folder.
ETL_FOLDER = Path(__file__).parent.parent.parent.parent / "etl"

# Uncomment to load credentials to local grapher.
# load_dotenv(ETL_FOLDER / ".env")
# Uncomment to load credentials to live grapher.
load_dotenv(ETL_FOLDER / ".env.live")

# List "combined disaster types" (as they were defined in the garden/grapher steps).
DISASTER_COMBINATION_TYPES = [
    'All disasters',
    'All disasters excluding earthquakes',
    'All disasters excluding extreme temperature',
]
# List individual disaster types (as they were defined in the garden/grapher steps).
DISASTER_TYPES = [
    'Drought',
    'Dry mass movement',
    'Earthquake',
    'Extreme temperature',
    'Extreme weather',
    'Flood',
    'Fog',
    'Glacial lake outburst flood',
    'Volcanic activity',
    'Wet mass movement',
    'Wildfire',
    ]
# List human and economic impacts (as they were defined in the garden/grapher steps).
HUMAN_IMPACTS = ["Deaths", "Affected", "Homeless", "Injured", "Total affected"]
ECONOMIC_IMPACTS = [
    "Reconstruction costs as a share of GDP",
    "Total economic damages as a share of GDP",
    "Insured damages as a share of GDP",
]
# Common string to use in the footer of all views in the explorer.
COMMON_NOTE = f"Disasters are recorded until {LAST_DISASTERS_DATE}."
# String to use in the footer of all views in the explorer showing decadal averages.
DECADAL_AVERAGE_NOTE = f"Values are annual numbers averaged over all years in the same decade. For example, values for 2000 show the 2000 to 2009 average. {COMMON_NOTE}"
# Mapping from the impact extracted from the variable title to the title of the view of disaster impacts by type of disaster.
IMPACT_MAPPING = {
    "Deaths": "deaths",
    "Affected": "people requiring immediate assistance",
    "Homeless": "people left homeless",
    "Injured": "people injured",
    "Total affected": "people affected",
}

# Connect to grapher database.
conn = MySQLdb.connect(
        db=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        charset="utf8mb4",
        autocommit=True,
    )

# Download all natural disasters variables (for the relevant version).
query = f"""
SELECT * 
FROM variables
WHERE catalogPath LIKE 'grapher/emdat/{VERSION}/natural_disasters/%'

"""
df = pd.read_sql(sql=query, con=conn)

# Select relevant columns.
df = df[['id', 'name', 'datasetId', 'shortName', 'catalogPath', 'titlePublic', 'titleVariant', 'descriptionShort']]

# Select yearly variables.
df_yearly = df[~df["name"].str.contains("decadal")].reset_index(drop=True)

# Select decadal variables.
df_decadal = df[df["name"].str.contains("decadal")].reset_index(drop=True)

# Initialize a list that will gather all relevant data to construct the explorer file.
data = []

# Add rows of decadal data.

########################################################################################################################
# TODO: Uncomment once missing data strategy can be set to "Show entities with missing data".
# # Add a row with all variables showing a specific impact.
# for impact in HUMAN_IMPACTS:
#     names = [f"{impact} - {disaster} (decadal)" for disaster in DISASTER_TYPES]
#     selected = df_decadal[df_decadal["name"].isin(names)]
#     data.append({"yVariableIds": " ".join(selected["id"].astype(str).tolist()), "Disaster Type Dropdown": "All disasters (by type)", "Impact Dropdown": impact, "Timespan Radio": "Decadal average", "Per capita Checkbox": "false", "type": "StackedBar", "note": DECADAL_AVERAGE_NOTE, "title": f"Decadal average: Annual number of {IMPACT_MAPPING[impact]} from natural disasters"})
# # Add a row with all variables showing a specific impact per 100,000 people.
# for impact in HUMAN_IMPACTS:
#     names = [f"{impact} per 100,000 people - {disaster} (decadal)" for disaster in DISASTER_TYPES]
#     selected = df_decadal[df_decadal["name"].isin(names)]
#     data.append({"yVariableIds": " ".join(selected["id"].astype(str).tolist()), "Disaster Type Dropdown": "All disasters (by type)", "Impact Dropdown": impact, "Timespan Radio": "Decadal average", "Per capita Checkbox": "true", "type": "StackedBar", "note": DECADAL_AVERAGE_NOTE, "title": f"Decadal average: Annual rate of {IMPACT_MAPPING[impact]} from natural disasters"})
########################################################################################################################
# Add a row for each disaster type and human impact.
for impact in HUMAN_IMPACTS:
    for disaster in DISASTER_COMBINATION_TYPES + DISASTER_TYPES:
        name = f"{impact} - {disaster} (decadal)"
        selected = df_decadal[(df_decadal["name"] == name)]
        assert len(selected) == 1
        data.append({"yVariableIds": selected["id"].item(), "Disaster Type Dropdown": disaster, "Impact Dropdown": impact, "Timespan Radio": "Decadal average", "Per capita Checkbox": "false", "type": "StackedBar", "note": DECADAL_AVERAGE_NOTE})
# Add a row for each disaster type and human impact per 100,000 people.
for impact in HUMAN_IMPACTS:
    for disaster in DISASTER_COMBINATION_TYPES + DISASTER_TYPES:
        name = f"{impact} per 100,000 people - {disaster} (decadal)"
        selected = df_decadal[(df_decadal["name"] == name)]
        assert len(selected) == 1
        data.append({"yVariableIds": selected["id"].item(), "Disaster Type Dropdown": disaster, "Impact Dropdown": impact, "Timespan Radio": "Decadal average", "Per capita Checkbox": "true", "type": "StackedBar", "note": DECADAL_AVERAGE_NOTE})
# Add a row for each individual disaster type and economic impact per GDP.
for impact in ECONOMIC_IMPACTS:
    for disaster in DISASTER_COMBINATION_TYPES + DISASTER_TYPES:
        name = f"{impact} - {disaster} (decadal)"
        selected = df_decadal[(df_decadal["name"] == name)]
        assert len(selected) == 1
        data.append({"yVariableIds": selected["id"].item(), "Disaster Type Dropdown": disaster, "Impact Dropdown": impact, "Timespan Radio": "Decadal average", "Per capita Checkbox": "false", "type": "StackedBar", "note": DECADAL_AVERAGE_NOTE})

# Add rows of yearly data.
########################################################################################################################
# TODO: Uncomment once missing data strategy can be set to "Show entities with missing data".
# # Add a row with all variables showing a specific impact.
# for impact in HUMAN_IMPACTS:
#     names = [f"{impact} - {disaster}" for disaster in DISASTER_TYPES]
#     selected = df_yearly[df_yearly["name"].isin(names)]
#     data.append({"yVariableIds": " ".join(selected["id"].astype(str).tolist()), "Disaster Type Dropdown": "All disasters (by type)", "Impact Dropdown": impact, "Timespan Radio": "Annual", "Per capita Checkbox": "false", "type": "StackedBar", "note": COMMON_NOTE, "title": f"Annual number of {IMPACT_MAPPING[impact]} from natural disasters"})
# # Add a row with all variables showing a specific impact per 100,000 people.
# for impact in HUMAN_IMPACTS:
#     names = [f"{impact} per 100,000 people - {disaster}" for disaster in DISASTER_TYPES]
#     selected = df_yearly[df_yearly["name"].isin(names)]
#     data.append({"yVariableIds": " ".join(selected["id"].astype(str).tolist()), "Disaster Type Dropdown": "All disasters (by type)", "Impact Dropdown": impact, "Timespan Radio": "Annual", "Per capita Checkbox": "true", "type": "StackedBar", "note": COMMON_NOTE, "title": f"Annual rate of {IMPACT_MAPPING[impact]} from natural disasters"})
########################################################################################################################
# Add a row for each disaster type and human impact.
for impact in HUMAN_IMPACTS:
    for disaster in DISASTER_COMBINATION_TYPES + DISASTER_TYPES:
        name = f"{impact} - {disaster}"
        selected = df_yearly[(df_yearly["name"] == name)]
        assert len(selected) == 1
        data.append({"yVariableIds": selected["id"].item(), "Disaster Type Dropdown": disaster, "Impact Dropdown": impact, "Timespan Radio": "Annual", "Per capita Checkbox": "false", "type": "StackedBar", "note": COMMON_NOTE})
# Add a row for each disaster type and human impact per 100,000 people.
for impact in HUMAN_IMPACTS:
    for disaster in DISASTER_COMBINATION_TYPES + DISASTER_TYPES:
        name = f"{impact} per 100,000 people - {disaster}"
        selected = df_yearly[(df_yearly["name"] == name)]
        assert len(selected) == 1
        data.append({"yVariableIds": selected["id"].item(), "Disaster Type Dropdown": disaster, "Impact Dropdown": impact, "Timespan Radio": "Annual", "Per capita Checkbox": "true", "type": "StackedBar", "note": COMMON_NOTE})
# Add a row for each individual disaster type and economic impact per GDP.
for impact in ECONOMIC_IMPACTS:
    for disaster in DISASTER_COMBINATION_TYPES + DISASTER_TYPES:
        name = f"{impact} - {disaster}"
        selected = df_yearly[(df_yearly["name"] == name)]
        if len(selected) == 1:
            data.append({"yVariableIds": selected["id"].item(), "Disaster Type Dropdown": disaster, "Impact Dropdown": impact, "Timespan Radio": "Annual", "Per capita Checkbox": "false", "type": "StackedBar", "note": COMMON_NOTE})
        else:
            print(f"Not found: {name}")

# Prepare header of explorer file.
df_explorer = pd.DataFrame.from_records(data)
explorer = """explorerTitle\tNatural Disasters
explorerSubtitle\tExplore the global frequency, severity, and consequences of disasters.
isPublished\tfalse
selection\tWorld
hideAlertBanner\ttrue
hasMapTab\ttrue
tab\tchart
wpBlockId\t46066
yAxisMin\t0
hideAnnotationFieldsInTitle\ttrue
graphers
"""
# Add column names to explorer.
explorer += "\t" + "\t".join(df_explorer.columns) + "\n"

# Add rows to explorer.
for i, row in df_explorer.iterrows():
    explorer += "\t" + "\t".join([str(item) if pd.notna(item) else "" for item in row]) + "\n"

# Save explorer file.
with open(OUTPUT_FILE, "w") as output_file:
    output_file.write(explorer)
