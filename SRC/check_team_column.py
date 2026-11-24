import pandas as pd

df = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

print(
    [
        col
        for col in df.columns
        if "Team" in col
    ]
)