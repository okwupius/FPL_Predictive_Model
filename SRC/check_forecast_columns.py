import pandas as pd

forecast = pd.read_csv(
    "data/processed/forecast_dataset.csv"
)

print(forecast.columns.tolist())