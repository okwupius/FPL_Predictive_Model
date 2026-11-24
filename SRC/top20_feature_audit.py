import pandas as pd

preds = pd.read_csv(
    "data/processed/v11_predictions.csv"
)

mapping = pd.read_csv(
    "data/processed/player_mapping.csv"
)

players = pd.read_csv(
    "data/Raw/fpl_players.csv"
)

results = preds.merge(
    mapping[
        [
            "player_id",
            "First_Name",
            "Last_Name"
        ]
    ],
    on="player_id",
    how="left"
)

results = results.sort_values(
    "Projected_Points",
    ascending=False
)

top20 = results.head(20)

print(
    top20[
        [
            "First_Name",
            "Last_Name",
            "Projected_Points",
            "Form",
            "Total_Points",
            "Ownership",
            "xG",
            "xA"
        ]
    ]
)
