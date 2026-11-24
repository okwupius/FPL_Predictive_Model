import pandas as pd
from pulp import *

# -------------------------
# LOAD DATA
# -------------------------

df = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

# We'll optimize on the top 200 players
# to keep solve time fast

df = df.head(200).copy()

# -------------------------
# MODEL
# -------------------------

model = LpProblem(
    "FPL_Squad_Optimizer",
    LpMaximize
)

# Decision variable for each player

player_vars = {
    i: LpVariable(
        f"player_{i}",
        lowBound=0,
        upBound=1,
        cat="Integer"
    )
    for i in df.index:
    model += player_vars[i] <= 1
}

# -------------------------
# OBJECTIVE
# -------------------------

model += lpSum(
    player_vars[i] * df.loc[i, "Projected_Points"]
    for i in df.index
)

# -------------------------
# SQUAD SIZE
# -------------------------

model += lpSum(
    player_vars[i]
    for i in df.index
) == 15

# -------------------------
# BUDGET
# -------------------------

model += lpSum(
    player_vars[i] * df.loc[i, "Price"]
    for i in df.index
) <= 100

# -------------------------
# POSITION CONSTRAINTS
# -------------------------

model += lpSum(
    player_vars[i]
    for i in df.index
    if df.loc[i, "Position"] == 1
) == 2

model += lpSum(
    player_vars[i]
    for i in df.index
    if df.loc[i, "Position"] == 2
) == 5

model += lpSum(
    player_vars[i]
    for i in df.index
    if df.loc[i, "Position"] == 3
) == 5

model += lpSum(
    player_vars[i]
    for i in df.index
    if df.loc[i, "Position"] == 4
) == 3

# -------------------------
# MAX 3 PER CLUB
# -------------------------

for team in df["Team"].dropna().unique():

    model += lpSum(
        player_vars[i]
        for i in df.index
        if df.loc[i, "Team"] == team
    ) <= 3

# -------------------------
# SOLVE
# -------------------------

model.solve()

selected = []

for i in df.index:

    if value(player_vars[i]) == 1:

        selected.append(
            df.loc[i]
        )

squad = pd.DataFrame(selected)

print("\nOPTIMAL FPL SQUAD\n")

print(
    squad[
        [
            "First_Name",
            "Last_Name",
            "Position",
            "Team",
            "Price",
            "Projected_Points"
        ]
    ]
    .sort_values(
        ["Position", "Projected_Points"],
        ascending=[True, False]
    )
)

print("\nSUMMARY\n")

print(
    f"Total Cost: £{squad['Price'].sum():.1f}"
)

print(
    f"Projected Points: {squad['Projected_Points'].sum():.2f}"
)

print(
    f"Players: {len(squad)}"
)
