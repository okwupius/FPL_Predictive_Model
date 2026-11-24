import pandas as pd

forecast = pd.read_csv(
    "data/processed/forecast_v10.csv"
)

players = pd.read_csv(
    "data/Raw/fpl_players.csv"
)

extra = players[
    [
        "id",
        "Total_Points",
        "Form"
    ]
].copy()

extra = extra.rename(
    columns={
        "id": "player_id"
    }
)

forecast = forecast.merge(
    extra,
    on="player_id",
    how="left"
)

forecast.to_csv(
    "data/processed/forecast_v11.csv",
    index=False
)

print(forecast.shape)

print(
    forecast[
        [
            "player_id",
            "Total_Points",
            "Form"
        ]
    ].head(20)
)

