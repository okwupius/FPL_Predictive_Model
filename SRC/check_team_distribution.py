import pandas as pd

df = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

top50 = df.head(50)

print(
    top50.groupby("Position")
         .agg(
             Count=("Position", "count"),
             AvgPrice=("Price", "mean"),
             AvgProjection=("Projected_Points", "mean")
         )
)
