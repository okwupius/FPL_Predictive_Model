import pandas as pd

df = pd.read_csv(
    "data/processed/all_player_history.csv"
)

# Sort by player and gameweek
df = df.sort_values(
    ["player_id", "round"]
)

# Rolling features

df["avg_points_last_3"] = (
    df.groupby("player_id")["total_points"]
    .transform(
        lambda x:
        x.shift(1).rolling(3).mean()
    )
)

df["avg_points_last_5"] = (
    df.groupby("player_id")["total_points"]
    .transform(
        lambda x:
        x.shift(1).rolling(5).mean()
    )
)

df["avg_minutes_last_5"] = (
    df.groupby("player_id")["minutes"]
    .transform(
        lambda x:
        x.shift(1).rolling(5).mean()
    )
)

training_data = df.dropna()

training_data.to_csv(
    "data/processed/training_data.csv",
    index=False
)

print("Training dataset created!")
print(training_data.shape)