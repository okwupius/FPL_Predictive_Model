import pandas as pd

players = pd.read_csv(
    "data/Raw/fpl_players.csv"
)

mapping = players[
    [
        "id",
        "First_Name",
        "Last_Name",
        "Price",
        "Position",
        "Team"
    ]
].copy()

mapping = mapping.rename(
    columns={
        "id": "player_id"
    }
)

mapping.to_csv(
    "data/processed/player_mapping.csv",
    index=False
)

print(mapping.head())

print("\nColumns:")
print(mapping.columns.tolist())

print(f"\nTotal Players: {len(mapping)}")