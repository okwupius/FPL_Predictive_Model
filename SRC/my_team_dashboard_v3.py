import pandas as pd

# ==================================================
# LOAD DATA
# ==================================================

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

# ==================================================
# SQUAD HEALTH
# ==================================================

avg_rank = team["Rank"].mean()

health_score = max(
    0,
    min(
        100,
        round(
            100 - (avg_rank / 4),
            1
        )
    )
)

if health_score >= 80:
    health_status = "Excellent"
elif health_score >= 60:
    health_status = "Good"
elif health_score >= 40:
    health_status = "Average"
else:
    health_status = "Needs Attention"

# ==================================================
# TRANSFER ANALYSIS
# ==================================================

recommendations = []

for _, player in team.iterrows():

    position = player["Position"]

    replacements = rankings[
        rankings["Position"] == position
    ].copy()

    # Remove owned players

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

    # Affordability

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

    # Priority score rewards:
    # large gain
    # poor current rank

    priority_score = (
        gain
        + (player["Rank"] / 100)
    )

    recommendations.append(
        {
            "Sell":
                f"{player['First_Name']} {player['Last_Name']}",
            "Buy":
                f"{replacement['First_Name']} {replacement['Last_Name']}",
            "Position":
                player["Position"],
            "Sell_Rank":
                int(player["Rank"]),
            "Gain":
                round(gain, 2),
            "Priority_Score":
                round(priority_score, 2)
        }
    )

recommendations = pd.DataFrame(
    recommendations
)

recommendations = recommendations.sort_values(
    "Priority_Score",
    ascending=False
)

# ==================================================
# BEST XI
# ==================================================

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

    if (
        len(defs) < d
        or len(mids) < m
        or len(fwds) < f
    ):
        continue

    xi = pd.concat(
        [
            gk.head(1),
            defs.head(d),
            mids.head(m),
            fwds.head(f)
        ]
    )

    points = xi[
        "Projected_Points"
    ].sum()

    if points > best_points:

        best_points = points
        best_xi = xi.copy()
        best_formation = f"{d}-{m}-{f}"

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

# ==================================================
# POSITION SPECIFIC TRANSFERS
# ==================================================

best_def = (
    recommendations[
        recommendations["Position"] == 2
    ]
    .head(1)
)

best_mid = (
    recommendations[
        recommendations["Position"] == 3
    ]
    .head(1)
)

best_fwd = (
    recommendations[
        recommendations["Position"] == 4
    ]
    .head(1)
)

# ==================================================
# OUTPUT
# ==================================================

print("\n" + "=" * 70)
print(" FPL DASHBOARD V3 ")
print("=" * 70)

print("\nSQUAD HEALTH")

print(
    f"\nScore: {health_score}/100"
)

print(
    f"Status: {health_status}"
)

print(
    f"Average Rank: {avg_rank:.1f}"
)

print(
    f"Squad Value: £{team['Price'].sum():.1f}m"
)

# --------------------------------------------------

print("\n" + "=" * 70)
print(" BEST SINGLE TRANSFER ")
print("=" * 70)

print(
    recommendations.head(1)
)

# --------------------------------------------------

print("\n" + "=" * 70)
print(" BEST TWO TRANSFERS ")
print("=" * 70)

print(
    recommendations.head(2)
)

# --------------------------------------------------

print("\n" + "=" * 70)
print(" BEST DEFENDER TRANSFER ")
print("=" * 70)

print(best_def)

# --------------------------------------------------

print("\n" + "=" * 70)
print(" BEST MIDFIELDER TRANSFER ")
print("=" * 70)

print(best_mid)

# --------------------------------------------------

print("\n" + "=" * 70)
print(" BEST FORWARD TRANSFER ")
print("=" * 70)

print(best_fwd)

# --------------------------------------------------

print("\n" + "=" * 70)
print(" TOP 10 TRANSFER PRIORITIES ")
print("=" * 70)

print(
    recommendations[
        [
            "Sell",
            "Buy",
            "Sell_Rank",
            "Gain",
            "Priority_Score"
        ]
    ]
    .head(10)
)

# --------------------------------------------------

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
    f"Projected Points: {best_points:.2f}"
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