import pandas as pd

df = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

goalkeepers = (
    df[df["Position"] == 1]
    .sort_values(
        "Projected_Points",
        ascending=False
    )
    .head(2)
)

defenders = (
    df[df["Position"] == 2]
    .sort_values(
        "Projected_Points",
        ascending=False
    )
    .head(5)
)

midfielders = (
    df[df["Position"] == 3]
    .sort_values(
        "Projected_Points",
        ascending=False
    )
    .head(5)
)

forwards = (
    df[df["Position"] == 4]
    .sort_values(
        "Projected_Points",
        ascending=False
    )
    .head(3)
)

squad = pd.concat(
    [
        goalkeepers,
        defenders,
        midfielders,
        forwards
    ]
)

print("\nOPTIMAL SQUAD (V11)\n")

print(
    squad[
        [
            "First_Name",
            "Last_Name",
            "Position",
            "Price",
            "Projected_Points"
        ]
    ]
)

print("\nSUMMARY\n")

print(
    f"Total Cost: £{squad['Price'].sum():.1f}m"
)

print(
    f"Projected Points: {squad['Projected_Points'].sum():.2f}"
)