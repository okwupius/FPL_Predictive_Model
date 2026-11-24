import pandas as pd

players = pd.read_csv(
    "data/processed/model_v5_data.csv"
)

strength = pd.read_csv(
    "data/processed/team_strength.csv"
)

players = players.merge(
    strength,
    left_on="opponent_team",
    right_on="Team",
    how="left"
)

players.to_csv(
    "data/processed/model_v7_data.csv",
    index=False
)

print(players.columns.tolist())