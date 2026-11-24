import requests
import pandas as pd

print("Downloading FPL data...")

url = "https://fantasy.premierleague.com/api/bootstrap-static/"

response = requests.get(url)

data = response.json()

players = pd.DataFrame(data["elements"])

players = players[
    [
        "id",
        "first_name",
        "second_name",
        "team",
        "element_type",
        "now_cost",
        "minutes",
        "goals_scored",
        "assists",
        "clean_sheets",
        "total_points",
        "form",
        "selected_by_percent",
        "expected_goals",
        "expected_assists"
    ]
]

players.columns = [
    "id",
    "First_Name",
    "Last_Name",
    "Team",
    "Position",
    "Price",
    "Minutes",
    "Goals",
    "Assists",
    "Clean_Sheets",
    "Total_Points",
    "Form",
    "Ownership",
    "xG",
    "xA"
]

players["Price"] = players["Price"] / 10
players["Ownership"] = players["Ownership"].astype(float)

players.to_csv(
    "data/Raw/fpl_players.csv",
    index=False
)

print("\nDownload Successful!")

print(players.head())

print("\nColumns:")
print(players.columns.tolist())