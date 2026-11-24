import pandas as pd

df = pd.read_csv(
    "data/processed/all_player_history.csv"
)

df = df.sort_values(
    ["player_id", "round"]
)

# Rolling points

df["avg_points_last_3"] = (
    df.groupby("player_id")["total_points"]
      .transform(lambda x: x.shift(1).rolling(3).mean())
)

df["avg_points_last_5"] = (
    df.groupby("player_id")["total_points"]
      .transform(lambda x: x.shift(1).rolling(5).mean())
)

# Rolling minutes

df["avg_minutes_last_5"] = (
    df.groupby("player_id")["minutes"]
      .transform(lambda x: x.shift(1).rolling(5).mean())
)

# Rolling goals

df["avg_goals_last_5"] = (
    df.groupby("player_id")["goals_scored"]
      .transform(lambda x: x.shift(1).rolling(5).mean())
)

# Rolling assists

df["avg_assists_last_5"] = (
    df.groupby("player_id")["assists"]
      .transform(lambda x: x.shift(1).rolling(5).mean())
)

# Rolling bonus

df["avg_bonus_last_5"] = (
    df.groupby("player_id")["bonus"]
      .transform(lambda x: x.shift(1).rolling(5).mean())
)

# Home/Away

df["home_game"] = (
    df["was_home"].astype(int)
)

training_data = df.dropna()

training_data.to_csv(
    "data/processed/enhanced_training_data.csv",
    index=False
)

print(training_data.shape)
print(training_data.columns.tolist())