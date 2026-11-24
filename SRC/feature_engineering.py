import pandas as pd

players = pd.read_csv("data/Raw/fpl_players.csv")

players = players[players["Minutes"] > 0].copy()

# Points per match
players["Points_Per_90"] = (
    players["Total_Points"] /
    (players["Minutes"] / 90)
)

# Goal involvement
players["Goal_Involvement"] = (
    players["Goals"] +
    players["Assists"]
)

# Value
players["Value_Score"] = (
    players["Total_Points"] /
    players["Price"]
)

# Save engineered dataset
players.to_csv(
    "data/processed/fpl_features.csv",
    index=False
)

print(players.head())
print("\nFeatures saved successfully.")