import pandas as pd

df = pd.read_csv(
    "data/processed/model_v7_data.csv"
)

players = ["Haaland", "Palmer", "Saka", "Isak"]

check = df[
    df["player_id"].isin(
        [109, 406]  # replace with actual IDs later
    )
]

print(check.tail())