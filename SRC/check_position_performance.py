import pandas as pd

df = pd.read_csv(
    "data/processed/model_v11_data.csv"
)

print(
    df.groupby("Position")["total_points"]
      .agg(["count", "mean", "max"])
)
