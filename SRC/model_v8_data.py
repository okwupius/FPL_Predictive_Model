import pandas as pd

df = pd.read_csv(
    "data/processed/model_v7_data.csv"
)

# Only players who regularly play

df = df[
    df["avg_minutes_last_5"] >= 60
]

# Only players with meaningful ownership

df = df[
    df["Ownership"] >= 1
]

df.to_csv(
    "data/processed/model_v8_data.csv",
    index=False
)

print(df.shape)