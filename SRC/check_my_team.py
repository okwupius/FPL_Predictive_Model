import pandas as pd

# Your squad
my_team = pd.read_csv(
    "data/my_team.csv"
)

# Model rankings
rankings = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

# Merge squad with rankings
team = my_team.merge(
    rankings,
    on=["First_Name", "Last_Name"],
    how="left"
)

print("\nMY TEAM ANALYSIS\n")

print(
    team[
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

print("\nSUMMARY\n")

print(
    f"Players Found: "
    f"{team['Rank'].notna().sum()}"
    f"/{len(team)}"
)

missing = team[
    team["Rank"].isna()
]
