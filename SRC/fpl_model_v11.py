import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

df = pd.read_csv(
    "data/processed/model_v11_data.csv"
)

features = [
    "avg_points_last_3",
    "avg_points_last_5",
    "avg_minutes_last_5",
    "avg_goals_last_5",
    "avg_assists_last_5",
    "avg_bonus_last_5",
    "home_game",
    "Price",
    "Ownership",
    "xG",
    "xA",
    "Attack_Strength",
    "Defence_Strength",
    "Opponent_Attack_Strength",
    "Opponent_Defence_Strength",
    "Total_Points",
    "Form"
]

X = df[features]

y = df["total_points"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=500,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

preds = model.predict(
    X_test
)

mae = mean_absolute_error(
    y_test,
    preds
)

print(f"\nV11 MAE: {mae:.2f}")

importance = pd.DataFrame(
    {
        "Feature": features,
        "Importance": model.feature_importances_
    }
)

print("\nFEATURE IMPORTANCE\n")

print(
    importance.sort_values(
        "Importance",
        ascending=False
    )
)
