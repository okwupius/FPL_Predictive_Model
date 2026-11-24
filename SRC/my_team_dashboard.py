import pandas as pd

# ---------------------------------
# LOAD DATA
# ---------------------------------

my_team = pd.read_csv(
    "data/my_team.csv"
)

rankings = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

rankings["Points_Per_Million"] = (
    rankings["Projected_Points"] /
    rankings["Price"]
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

# ---------------------------------
# TEAM OVERVIEW
# ---------------------------------

print("\n" + "=" * 60)
print(" MY FPL DASHBOARD ")
print("=" * 60)

print("\nCURRENT SQUAD\n")

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

# ---------------------------------
# BEST XI
# ---------------------------------

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

    pts = xi["Projected_Points"].sum()

    if pts > best_points:

        best_points = pts
        best_xi = xi.copy()
        best_formation = f"{d}-{m}-{f}"

bench = team[
    ~team.index.isin(best_xi.index)
].sort_values(
    "Projected_Points",
    ascending=False
)

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

print("\n" + "=" * 60)
print(" BEST XI ")
print("=" * 60)

print(f"\nBest Formation: {best_formation}\n")

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
    f"\nProjected Points: {best_points:.2f}"
)

print(
    f"Projected With Captain: "
    f"{best_points + captain['Projected_Points']:.2f}"
)

print(
    f"\nCaptain: "
    f"{captain['First_Name']} {captain['Last_Name']}"
)

print(
    f"Vice Captain: "
    f"{vice['First_Name']} {vice['Last_Name']}"
)

print("\nBENCH ORDER\n")

print(
    bench[
        [
            "First_Name",
            "Last_Name",
            "Projected_Points"
        ]
    ]
)

# ---------------------------------
# SELL CANDIDATES
# ---------------------------------

worst = (
    team
    .sort_values(
        "Projected_Points"
    )
    .head(5)
)

print("\n" + "=" * 60)
print(" SELL CANDIDATES ")
print("=" * 60)

print(
    worst[
        [
            "First_Name",
            "Last_Name",
            "Projected_Points",
            "Rank"
        ]
    ]
)

# ---------------------------------
# TRANSFER RECOMMENDATIONS
# ---------------------------------

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

    best_replace = (
        replacements
        .sort_values(
            "Projected_Points",
            ascending=False
        )
        .iloc[0]
    )

    gain = (
        best_replace["Projected_Points"]
        - player["Projected_Points"]
    )

    recommendations.append(
        {
            "Sell":
                f"{player['First_Name']} {player['Last_Name']}",
            "Buy":
                f"{best_replace['First_Name']} "
                f"{best_replace['Last_Name']}",
            "Gain": round(gain, 2)
        }
    )

recommendations = pd.DataFrame(
    recommendations
)

recommendations = recommendations.sort_values(
    "Gain",
    ascending=False
)

print("\n" + "=" * 60)
print(" TOP TRANSFERS ")
print("=" * 60)

print(
    recommendations.head(10)
)

# ---------------------------------
# TEAM SUMMARY
# ---------------------------------

print("\n" + "=" * 60)
print(" TEAM SUMMARY ")
print("=" * 60)

print(
    f"Squad Value: £{team['Price'].sum():.1f}m"
)

print(
    f"Average Rank: "
    f"{team['Rank'].mean():.1f}"
)

print(
    f"Best Player: "
    f"{team.sort_values('Projected_Points', ascending=False).iloc[0]['First_Name']} "
    f"{team.sort_values('Projected_Points', ascending=False).iloc[0]['Last_Name']}"
)

print(
    f"Worst Player: "
    f"{team.sort_values('Projected_Points').iloc[0]['First_Name']} "
    f"{team.sort_values('Projected_Points').iloc[0]['Last_Name']}"
)
