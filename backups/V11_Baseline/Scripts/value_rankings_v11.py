import pandas as pd

df = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

df["Points_Per_Million"] = (
    df["Projected_Points"] /
    df["Price"]
)

value = df.sort_values(
    "Points_Per_Million",
    ascending=False
)

print("\nTOP 30 VALUE PLAYERS\n")

print(
    value[
        [
            "First_Name",
            "Last_Name",
            "Price",
            "Projected_Points",
            "Points_Per_Million"
        ]
    ].head(30)
)