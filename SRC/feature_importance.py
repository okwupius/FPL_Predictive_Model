import pandas as pd
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv(
    "data/processed/training_data.csv"
)

features = [
    "avg_points_last_3",
    "avg_points_last_5",
    "avg_minutes_last_5"
]

X = df[features]
y = df["total_points"]

model = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)

model.fit(X, y)

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    "Importance",
    ascending=False
)

print(importance)
