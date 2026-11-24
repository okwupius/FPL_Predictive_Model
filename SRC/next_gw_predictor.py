import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Load training dataset

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

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions
)

print(f"\nForecast MAE: {mae:.2f}")

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    "Importance",
    ascending=False
)

print("\nFeature Importance\n")
print(importance)

df["Predicted_Points"] = model.predict(X)

top_players = df.sort_values(
    "Predicted_Points",
    ascending=False
)

print("\nTop 20 Predicted Players\n")

print(
    top_players[
        [
            "player_id",
            "Predicted_Points"
        ]
    ].head(20)
)
