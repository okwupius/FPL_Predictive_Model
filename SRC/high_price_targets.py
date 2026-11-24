import pandas as pd

df = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

expensive = df[
    df["Price"] >= 8.0
].sort_values(
    "Projected_Points",
    ascending=False
)

print("\nHIGH PRICE PLAYERS (£8.0m+)\n")

print(
    expensive[
        [
            "Rank",
            "First_Name",
            "Last_Name",
            "Price",
            "Projected_Points"
        ]
    ].head(30)
)