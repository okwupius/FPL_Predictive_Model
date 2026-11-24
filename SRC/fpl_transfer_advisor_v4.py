import pandas as pd

# Load squad

my_team = pd.read_csv(
    "data/my_team.csv"
)

# Load model rankings

rankings = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

# Merge squad with rankings

current = my_team.merge(
    rankings,
    on=["First_Name", "Last_Name"],
    how="left"
)

owned_players = set(
    zip(
        current["First_Name"],
        current["Last_Name"]
    )
)

recommendations = []

for _, player in current.iterrows():

    replacements = rankings[
        rankings["Position"] == player["Position"]
    ].copy()

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

    replacements = replacements[
        replacements["Price"]
        <= player["Price"] + 1.0
    ]

    if len(replacements) == 0:
        continue

    best_replacement = (
        replacements
        .sort_values(
            "Projected_Points",
            ascending=False
        )
        .iloc[0]
    )

    gain = (
        best_replacement["Projected_Points"]
        - player["Projected_Points"]
    )

    recommendations.append(
        {
            "Sell":
                f"{player['First_Name']} {player['Last_Name']}",
            "Buy":
                f"{best_replacement['First_Name']} {best_replacement['Last_Name']}",
            "Position":
                player["Position"],
            "Point_Gain":
                round(gain, 2)
        }
    )

recommendations = pd.DataFrame(
    recommendations
)

recommendations = recommendations.sort_values(
    "Point_Gain",
    ascending=False
)

print("\nBEST TRANSFERS THIS WEEK\n")

print(recommendations.head(10))
