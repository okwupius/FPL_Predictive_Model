import pandas as pd

mapping = pd.read_csv(
    "data/processed/player_mapping.csv"
)

print(mapping.columns.tolist())