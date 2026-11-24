import pandas as pd

df = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

df["Points_Per_Million"] = (
    df["Projected_Points"] /
    df["Price"]
)

# Best targets

buys = (
    df.sort_values(
        "Points_Per_Million",
        ascending=False
    )
    .head(10)
)

# Worst assets

sells = (
    df.sort_values(
        "Points_Per_Million",
        ascending=True
    )
    .head(10)
)

print("\nTOP BUY TARGETS\n")

print(
    buys[
        [
            "First_Name",
            "Last_Name",
            "Position",
            "Price",
            "Projected_Points",
            "Points_Per_Million"
        ]
    ]
)

print("\nTOP SELL CANDIDATES\n")

print(
    sells[
        [
            "First_Name",
            "Last_Name",
            "Position",
            "Price",
            "Projected_Points",
            "Points_Per_Million"
        ]
    ]
)

print("\nSUGGESTED UPGRADES\n")

for i in range(min(5, len(buys), len(sells))):

    sell = sells.iloc[i]
    buy = buys.iloc[i]

    gain = (
        buy["Projected_Points"]
        - sell["Projected_Points"]
    )

    print(
        f"OUT: {sell['First_Name']} "
        f"{sell['Last_Name']} "
        f"({sell['Projected_Points']:.2f})"
    )

    print(
        f" IN: {buy['First_Name']} "
        f"{buy['Last_Name']} "
        f"({buy['Projected_Points']:.2f})"
    )

    print(
        f"GAIN: +{gain:.2f} projected points\n"
    )
    