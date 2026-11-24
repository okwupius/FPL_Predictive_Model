import pandas as pd

history = pd.read_csv(
    "data/processed/enhanced_training_data.csv"
)

players = pd.read_csv(
    "data/Raw/fpl_players.csv"
)

player_features = players[
    [
        "id",
        "Price",
        "Ownership",
        "xG",
        "xA",
        "Position",
        "Team"
    ]
].copy()

player_features = player_features.rename(
    columns={
        "id": "player_id"
    }
)

merged = history.merge(
    player_features,
    on="player_id",
    how="left"
)

merged.to_csv(
    "data/processed/model_v5_data.csv",
    index=False
)

print(merged.shape)
print(merged.columns.tolist())