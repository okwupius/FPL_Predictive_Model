import pandas as pd

# Current squad

my_team = pd.read_csv(
    "data/my_team.csv"
)

# Model rankings

rankings = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

rankings["Points_Per_Million"] = (
    rankings["Projected_Points"] /
    rankings["Price"]
)

# Merge current squad

current = my_team.merge(
    rankings,
    on=["First_Name", "Last_Name"],
    how="left"
)

print("\nYOUR CURRENT SQUAD\n")

print(
    current[
        [
            "First_Name",
            "Last_Name",
            "Position",
            "Price",
            "Rank",
            "Projected_Points"
        ]
    ]
)

# Players already owned

owned_players = set(
    zip(
        current["First_Name"],
        current["Last_Name"]
    )
)

# Worst players in your squad

worst = (
    current
    .sort_values(
        "Projected_Points"
    )
    .head(5)
)

print("\nPLAYERS TO CONSIDER SELLING\n")

print(
    worst[
        [
            "First_Name",
            "Last_Name",
            "Rank",
            "Projected_Points"
        ]
    ]
)

print("\nREPLACEMENT OPTIONS\n")

for _, player in worst.iterrows():

    position = player["Position"]

    # Same position
    replacements = rankings[
        rankings["Position"] == position
    ].copy()

    # Exclude players already owned
    replacements = replacements[
        ~replacements.apply(
            lambda row:
            (
                row["First_Name"],
                row["Last_Name"]
            ) in owned_players,
            axis=1
        )
    ]

    # Keep affordable options
    replacements = replacements[
        replacements["Price"]
        <= player["Price"] + 1.0
    ]

    # Best projected replacements
    replacements = (
        replacements
        .sort_values(
            "Projected_Points",
            ascending=False
        )
        .head(3)
    )

    print(
        f"\nREPLACE: "
        f"{player['First_Name']} "
        f"{player['Last_Name']}"
    )

    print(
        replacements[
            [
                "First_Name",
                "Last_Name",
                "Price",
                "Projected_Points"
            ]
        ]
    )