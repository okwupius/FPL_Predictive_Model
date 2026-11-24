import pandas as pd
from datetime import datetime

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
# BUILD TRANSFER TABLE
# =====================================

recommendations = []

for _, player in team.iterrows():

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

    priority = gain + (
        player["Rank"] / 100
    )

    recommendations.append(
        {
            "Sell":
                f"{player['First_Name']} {player['Last_Name']}",
            "Buy":
                f"{replacement['First_Name']} {replacement['Last_Name']}",
            "Gain":
                round(gain, 2),
            "Priority_Score":
                round(priority, 2)
        }
    )

recommendations = pd.DataFrame(
    recommendations
).sort_values(
    "Priority_Score",
    ascending=False
)

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

# =====================================
# SUMMARY TAB
# =====================================

summary = pd.DataFrame(
    {
        "Metric": [
            "Squad Value",
            "Average Rank",
            "Best Formation",
            "Projected Points",
            "Projected With Captain",
            "Captain",
            "Vice Captain"
        ],
        "Value": [
            round(team["Price"].sum(), 1),
            round(team["Rank"].mean(), 1),
            best_formation,
            round(best_points, 2),
            round(
                best_points +
                captain["Projected_Points"],
                2
            ),
            f"{captain['First_Name']} {captain['Last_Name']}",
            f"{vice['First_Name']} {vice['Last_Name']}"
        ]
    }
)

# =====================================
# EXPORT EXCEL
# =====================================

today = datetime.now().strftime(
    "%Y_%m_%d"
)

filename = (
    f"reports/FPL_Report_{today}.xlsx"
)

with pd.ExcelWriter(
    filename,
    engine="openpyxl"
) as writer:

    summary.to_excel(
        writer,
        sheet_name="Summary",
        index=False
    )

    team.to_excel(
        writer,
        sheet_name="Current Squad",
        index=False
    )

    best_xi.to_excel(
        writer,
        sheet_name="Best XI",
        index=False
    )

    recommendations.head(20).to_excel(
        writer,
        sheet_name="Transfers",
        index=False
    )

print(
    f"\nReport saved:\n{filename}"
)
