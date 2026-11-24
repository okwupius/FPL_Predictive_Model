import pandas as pd

model = pd.read_csv(
    "data/processed/model_v10_data.csv"
)

players = pd.read_csv(
    "data/Raw/fpl_players.csv"
)

season_points = players[
    [
        "id",
        "Total_Points",
        "Form"
    ]
].copy()

season_points = season_points.rename(
    columns={
        "id": "player_id"
    }
)

model = model.merge(
    season_points,
    on="player_id",
    how="left"
)

model.to_csv(
    "data/processed/model_v11_data.csv",
    index=False
)

print(model.shape)

print(
    model[
        [
            "player_id",
            "Total_Points",
            "Form"
        ]
    ].head(20)
)
