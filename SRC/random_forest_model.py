import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Load engineered data
players = pd.read_csv(
    "data/processed/fpl_features.csv"
)

features = [
    "Price",
    "Minutes",
    "Goals",
    "Assists",
    "Form",
    "Value_Score",
    "Goal_Involvement",
    "Points_Per_90"
]

X = players[features]

y = players["Total_Points"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions
)

print(f"\nMean Absolute Error: {mae:.2f}")