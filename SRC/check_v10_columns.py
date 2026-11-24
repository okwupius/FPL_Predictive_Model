import pandas as pd

df = pd.read_csv(
    "data/processed/v10_predictions.csv"
)

print(df.columns.tolist())
