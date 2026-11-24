import pandas as pd

forecast = pd.read_csv(
    "data/processed/forecast_dataset.csv"
)

fixtures = pd.read_csv(
    "data/processed/next_fixtures.csv"
)

forecast = forecast.merge(
    fixtures,
    left_on="Team_x",
    right_on="Team",
    how="left"
)

forecast.to_csv(
    "data/processed/forecast_dataset_v9.csv",
    index=False
)

print(forecast.shape)

print(
    forecast[
        [
            "player_id",
            "Team_x",
            "Home_Game",
            "Fixture_Difficulty"
        ]
    ].head(20)
)