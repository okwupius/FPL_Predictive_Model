import pandas as pd

df = pd.read_csv(
    "data/processed/all_player_history.csv"
)

df = df.sort_values(
    ["player_id", "round"]
)

# Existing features

df["avg_points_last_3"] = (
    df.groupby("player_id")["total_points"]
      .transform(lambda x: x.shift(1).rolling(3).mean())
)

df["avg_points_last_5"] = (
    df.groupby("player_id")["total_points"]
      .transform(lambda x: x.shift(1).rolling(5).mean())
)

df["avg_minutes_last_5"] = (
    df.groupby("player_id")["minutes"]
      .transform(lambda x: x.shift(1).rolling(5).mean())
)

df["avg_goals_last_5"] = (
    df.groupby("player_id")["goals_scored"]
      .transform(lambda x: x.shift(1).rolling(5).mean())
)

df["avg_assists_last_5"] = (
    df.groupby("player_id")["assists"]
      .transform(lambda x: x.shift(1).rolling(5).mean())
)

df["avg_bonus_last_5"] = (
    df.groupby("player_id")["bonus"]
      .transform(lambda x: x.shift(1).rolling(5).mean())
)

df["home_game"] = (
    df["was_home"].astype(int)
)

# New feature
# opponent_team already exists in player history

df["fixture_difficulty"] = (
    df["opponent_team"]
)

training_data = df.dropna()

training_data.to_csv(
    "data/processed/enhanced_training_data_v2.csv",
    index=False
)

print(training_data.shape)
