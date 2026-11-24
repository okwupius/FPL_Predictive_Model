import pandas as pd

# Load player data
players = pd.read_csv("data/Raw/fpl_players.csv")

# Remove players with no minutes
players = players[players["Minutes"] > 0].copy()

# Convert Form to number
players["Form"] = pd.to_numeric(players["Form"])

# Minutes factor
players["Minutes_Factor"] = players["Minutes"] / players["Minutes"].max()

# Simple attacking score
players["Attacking_Score"] = (
    players["Goals"] * 4
    + players["Assists"] * 3
)

# Ownership factor
players["Ownership"] = pd.to_numeric(players["Ownership"])

players["Ownership_Factor"] = (
    players["Ownership"] / players["Ownership"].max()
)

# Expected points model
players["Expected_Points"] = (
    0.40 * players["Form"]
    + 0.30 * players["Minutes_Factor"] * 10
    + 0.20 * players["Attacking_Score"]
    + 0.10 * players["Ownership_Factor"] * 10
)

# Sort by prediction
predictions = players.sort_values(
    "Expected_Points",
    ascending=False
)

print("\nTOP 20 EXPECTED POINTS PLAYERS\n")

print(
    predictions[
        [
            "First_Name",
            "Last_Name",
            "Price",
            "Expected_Points"
        ]
    ].head(20)
)