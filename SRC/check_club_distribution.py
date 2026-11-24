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

print("\nCLUB DISTRIBUTION\n")

print(
    squad["Team"]
    .value_counts()
    .sort_index()
)

print("\nMAX CLUB COUNT:")

print(
    squad["Team"]
    .value_counts()
    .max()
)
