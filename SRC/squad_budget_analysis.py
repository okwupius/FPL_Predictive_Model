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

print("\nPOSITION BUDGET BREAKDOWN\n")

print(
    f"GK Cost: £{goalkeepers['Price'].sum():.1f}"
)

print(
    f"DEF Cost: £{defenders['Price'].sum():.1f}"
)

print(
    f"MID Cost: £{midfielders['Price'].sum():.1f}"
)

print(
    f"FWD Cost: £{forwards['Price'].sum():.1f}"
)

print(
    f"\nTotal Cost: £{
        goalkeepers['Price'].sum()
        + defenders['Price'].sum()
        + midfielders['Price'].sum()
        + forwards['Price'].sum()
    :.1f}"
)