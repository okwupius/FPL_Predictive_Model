import pandas as pd

df = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

df["Points_Per_Million"] = (
    df["Projected_Points"] /
    df["Price"]
)

sell = (
    df.sort_values(
        "Points_Per_Million",
        ascending=True
    )
)

print("\nTOP 20 SELL CANDIDATES\n")

print(
    sell[
        [
            "Rank",
            "First_Name",
            "Last_Name",
            "Position",
            "Price",
            "Projected_Points",
            "Points_Per_Million"
        ]
    ].head(20)
)
