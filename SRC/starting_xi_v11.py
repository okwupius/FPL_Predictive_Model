import pandas as pd

df = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

# Use the Projection Squad

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

# STARTING XI

starting_gk = (
    squad[squad["Position"] == 1]
    .sort_values(
        "Projected_Points",
        ascending=False
    )
    .head(1)
)

starting_def = (
    squad[squad["Position"] == 2]
    .sort_values(
        "Projected_Points",
        ascending=False
    )
    .head(3)
)

starting_mid = (
    squad[squad["Position"] == 3]
    .sort_values(
        "Projected_Points",
        ascending=False
    )
    .head(4)
)

starting_fwd = (
    squad[squad["Position"] == 4]
    .sort_values(
        "Projected_Points",
        ascending=False
    )
    .head(3)
)

starting_xi = pd.concat(
    [
        starting_gk,
        starting_def,
        starting_mid,
        starting_fwd
    ]
)

bench = squad[
    ~squad.index.isin(starting_xi.index)
]

# Captain and VC

captain = (
    starting_xi
    .sort_values(
        "Projected_Points",
        ascending=False
    )
    .head(1)
)

vice = (
    starting_xi
    .sort_values(
        "Projected_Points",
        ascending=False
    )
    .iloc[[1]]
)

print("\nSTARTING XI\n")

print(
    starting_xi[
        [
            "First_Name",
            "Last_Name",
            "Position",
            "Projected_Points"
        ]
    ]
    .sort_values(
        "Projected_Points",
        ascending=False
    )
)

print("\nBENCH\n")

print(
    bench[
        [
            "First_Name",
            "Last_Name",
            "Position",
            "Projected_Points"
        ]
    ]
)

print("\nCAPTAIN\n")

print(
    captain[
        [
            "First_Name",
            "Last_Name",
            "Projected_Points"
        ]
    ]
)

print("\nVICE CAPTAIN\n")

print(
    vice[
        [
            "First_Name",
            "Last_Name",
            "Projected_Points"
        ]
    ]
)