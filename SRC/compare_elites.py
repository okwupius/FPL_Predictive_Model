import pandas as pd

v10 = pd.read_csv(
    "data/processed/final_rankings_v10.csv"
)

v11 = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

elite_names = [
    "Haaland",
    "Saka",
    "Isak",
    "Palmer"
]

v10_elite = v10[
    v10["Last_Name"].isin(elite_names)
][
    [
        "First_Name",
        "Last_Name",
        "Rank",
        "Projected_Points"
    ]
]

v11_elite = v11[
    v11["Last_Name"].isin(elite_names)
][
    [
        "First_Name",
        "Last_Name",
        "Rank",
        "Projected_Points"
    ]
]

print("\nV10\n")
print(v10_elite)

print("\nV11\n")
print(v11_elite)
