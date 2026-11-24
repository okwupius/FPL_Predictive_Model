import pandas as pd

df = pd.read_csv(
    "data/processed/model_v7_data.csv"
)

print(df.columns.tolist())

print("\nTEAM SAMPLE\n")

print(
    df[
        [
            "player_id",
            "Team_x",
            "opponent_team",
            "home_game"
        ]
    ].head(20)
)
