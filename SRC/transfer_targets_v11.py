import pandas as pd

df = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

df["Points_Per_Million"] = (
    df["Projected_Points"] /
    df["Price"]
)

targets = (
    df.sort_values(
        "Points_Per_Million",
        ascending=False
    )
    .head(50)
)

print("\nTOP 20 TRANSFER TARGETS\n")

print(
    targets[
        [
            "Rank",
            "First_Name",
            "Last_Name",
            "Position",
            "Price",
            "Projected_Points",
            "Points_Per_Million"
        ]
    ]
    .head(20)
)
