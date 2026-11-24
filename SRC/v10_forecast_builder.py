import pandas as pd

forecast = pd.read_csv(
    "data/processed/forecast_dataset_v9.csv"
)

strength = pd.read_csv(
    "data/processed/team_strength.csv"
)

attack = strength[
    ["Team", "Attack_Strength"]
].rename(
    columns={
        "Team": "Opponent",
        "Attack_Strength": "Opponent_Attack_Strength"
    }
)

defence = strength[
    ["Team", "Defence_Strength"]
].rename(
    columns={
        "Team": "Opponent",
        "Defence_Strength": "Opponent_Defence_Strength"
    }
)

forecast = forecast.merge(
    attack,
    on="Opponent",
    how="left"
)

forecast = forecast.merge(
    defence,
    on="Opponent",
    how="left"
)

forecast.to_csv(
    "data/processed/forecast_v10.csv",
    index=False
)

print(forecast.shape)

print(
    forecast[
        [
            "player_id",
            "Opponent",
            "Opponent_Attack_Strength",
            "Opponent_Defence_Strength"
        ]
    ].head(20)
)
