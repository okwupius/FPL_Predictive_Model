import pandas as pd

# --------------------------------
# LOAD TEAM
# --------------------------------

my_team = pd.read_csv(
    "data/my_team.csv"
)

rankings = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

team = my_team.merge(
    rankings,
    on=["First_Name", "Last_Name"],
    how="left"
)

# --------------------------------
# FORMATIONS TO TEST
# DEF, MID, FWD
# --------------------------------

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
best_formation = None
best_xi = None

gk = (
    team[team["Position"] == 1]
    .sort_values(
        "Projected_Points",
        ascending=False
    )
)

defs = (
    team[team["Position"] == 2]
    .sort_values(
        "Projected_Points",
        ascending=False
    )
)

mids = (
    team[team["Position"] == 3]
    .sort_values(
        "Projected_Points",
        ascending=False
    )
)

fwds = (
    team[team["Position"] == 4]
    .sort_values(
        "Projected_Points",
        ascending=False
    )
)

for d, m, f in formations:

    if (
        len(defs) < d
        or len(mids) < m
        or len(fwds) < f
    ):
        continue

    lineup = pd.concat(
        [
            gk.head(1),
            defs.head(d),
            mids.head(m),
            fwds.head(f)
        ]
    )

    points = lineup[
        "Projected_Points"
    ].sum()

    if points > best_points:

        best_points = points
        best_formation = f"{d}-{m}-{f}"
        best_xi = lineup.copy()

# --------------------------------
# BENCH
# --------------------------------

bench = team[
    ~team.index.isin(
        best_xi.index
    )
]

bench = bench.sort_values(
    "Projected_Points",
    ascending=False
)

# --------------------------------
# CAPTAIN
# --------------------------------

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

# --------------------------------
# OUTPUT
# --------------------------------

print("\nBEST FORMATION\n")
print(best_formation)

print("\nSTARTING XI\n")

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

print("\nTOTAL PROJECTED POINTS\n")
print(round(best_points, 2))

print("\nCAPTAIN\n")
print(
    f"{captain['First_Name']} "
    f"{captain['Last_Name']} "
    f"({captain['Projected_Points']:.2f})"
)

print("\nVICE CAPTAIN\n")
print(
    f"{vice['First_Name']} "
    f"{vice['Last_Name']} "
    f"({vice['Projected_Points']:.2f})"
)

print("\nBENCH ORDER\n")

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
