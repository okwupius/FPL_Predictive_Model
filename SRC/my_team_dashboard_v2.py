import pandas as pd

# =====================================
# LOAD DATA
# =====================================

my_team = pd.read_csv(
    "data/my_team.csv"
)

rankings = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

rankings["Points_Per_Million"] = (
    rankings["Projected_Points"]
    / rankings["Price"]
)

team = my_team.merge(
    rankings,
    on=["First_Name", "Last_Name"],
    how="left"
)

owned_players = set(
    zip(
        team["First_Name"],
        team["Last_Name"]
    )
)

# =====================================
# TITLE
# =====================================

print("\n" + "=" * 70)
print(" FPL DASHBOARD V2 ")
print("=" * 70)

# =====================================
# TRANSFER PRIORITIES
# =====================================

recommendations = []

for _, player in team.iterrows():

    position = player["Position"]

    replacements = rankings[
        rankings["Position"] == position
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

    replacement = (
        replacements
        .sort_values(
            "Projected_Points",
            ascending=False
        )
        .iloc[0]
    )

    gain = (
        replacement["Projected_Points"]
        - player["Projected_Points"]
    )

    recommendations.append(
        {
            "Sell":
                f"{player['First_Name']} "
                f"{player['Last_Name']}",

            "Buy":
                f"{replacement['First_Name']} "
                f"{replacement['Last_Name']}",

            "Position":
                player["Position"],

            "Sell_Points":
                player["Projected_Points"],

            "Buy_Points":
                replacement["Projected_Points"],

            "Gain":
                round(gain, 2)
        }
    )

recommendations = pd.DataFrame(
    recommendations
)

recommendations = recommendations.sort_values(
    "Gain",
    ascending=False
)

# =====================================
# SQUAD HEALTH
# =====================================

avg_rank = team["Rank"].mean()

if avg_rank < 50:
    health = "Excellent"
elif avg_rank < 100:
    health = "Good"
elif avg_rank < 200:
    health = "Average"
else:
    health = "Needs Attention"

# =====================================
# BEST TRANSFERS
# =====================================

best_one = recommendations.head(1)

best_two = recommendations.head(2)

# =====================================
# BEST XI
# =====================================

formations = [
    (3, 4, 3),
    (3, 5, 2),
    (4, 4, 2),
    (4, 3, 3),
    (4, 5, 1),
    (5, 3, 2),
    (5, 4, 1)
]

best_points = -999
best_xi = None
best_formation = None

gk = team[
    team["Position"] == 1
].sort_values(
    "Projected_Points",
    ascending=False
)

defs = team[
    team["Position"] == 2
].sort_values(
    "Projected_Points",
    ascending=False
)

mids = team[
    team["Position"] == 3
].sort_values(
    "Projected_Points",
    ascending=False
)

fwds = team[
    team["Position"] == 4
].sort_values(
    "Projected_Points",
    ascending=False
)

for d, m, f in formations:

    xi = pd.concat(
        [
            gk.head(1),
            defs.head(d),
            mids.head(m),
            fwds.head(f)
        ]
    )

    pts = xi["Projected_Points"].sum()

    if pts > best_points:

        best_points = pts
        best_formation = f"{d}-{m}-{f}"
        best_xi = xi

captain = (
    best_xi
    .sort_values(
        "Projected_Points",
        ascending=False
    )
    .iloc[0]
)

vice = (
    best_xi
    .sort_values(
        "Projected_Points",
        ascending=False
    )
    .iloc[1]
)

# =====================================
# OUTPUT
# =====================================

print("\nSQUAD HEALTH")

print(
    f"\nStatus: {health}"
)

print(
    f"Average Rank: "
    f"{avg_rank:.1f}"
)

print(
    f"Squad Value: "
    f"£{team['Price'].sum():.1f}m"
)

print("\n" + "=" * 70)
print(" BEST SINGLE TRANSFER ")
print("=" * 70)

print(best_one)

print("\n" + "=" * 70)
print(" BEST TWO TRANSFERS ")
print("=" * 70)

print(best_two)

print("\n" + "=" * 70)
print(" TOP 10 TRANSFER PRIORITIES ")
print("=" * 70)

print(
    recommendations.head(10)
)

print("\n" + "=" * 70)
print(" BEST XI ")
print("=" * 70)

print(
    best_xi[
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

print(
    f"\nFormation: {best_formation}"
)

print(
    f"Projected Points: "
    f"{best_points:.2f}"
)

print(
    f"With Captain: "
    f"{best_points + captain['Projected_Points']:.2f}"
)

print(
    f"\nCaptain: "
    f"{captain['First_Name']} "
    f"{captain['Last_Name']}"
)

print(
    f"Vice Captain: "
    f"{vice['First_Name']} "
    f"{vice['Last_Name']}"
)
