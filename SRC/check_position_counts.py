import pandas as pd

df = pd.read_csv(
    "data/processed/model_v11_data.csv"
)

print(
    df["Position"]
    .value_counts()
    .sort_index()
)
