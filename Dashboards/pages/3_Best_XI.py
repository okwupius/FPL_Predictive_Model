import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Best XI",
    layout="wide"
)

st.title("🏆 Best XI Optimizer")

# ====================================
# LOAD DATA
# ====================================

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

# ====================================
# FORMATIONS
# ====================================

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
        best_xi = xi.copy()

# ====================================
# BENCH
# ====================================

bench = team[
    ~team.index.isin(
        best_xi.index
    )
].sort_values(
    "Projected_Points",
    ascending=False
)

# ====================================
# CAPTAINS
# ====================================

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

# ====================================
# METRICS
# ====================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Formation",
    best_formation
)

col2.metric(
    "Projected Points",
    f"{best_points:.2f}"
)

col3.metric(
    "With Captain",
    f"{best_points + captain['Projected_Points']:.2f}"
)

# ====================================
# CAPTAIN INFO
# ====================================

st.success(
    f"Captain: {captain['First_Name']} "
    f"{captain['Last_Name']}"
)

st.info(
    f"Vice-Captain: {vice['First_Name']} "
    f"{vice['Last_Name']}"
)

# ====================================
# STARTING XI
# ====================================

st.subheader("Starting XI")

display_xi = (
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

st.dataframe(
    display_xi,
    width="stretch",
    hide_index=True
)

# ====================================
# BENCH
# ====================================

st.subheader("Bench Order")

st.dataframe(
    bench[
        [
            "First_Name",
            "Last_Name",
            "Position",
            "Projected_Points"
        ]
    ],
    width="stretch",
    hide_index=True
)

# ====================================
# POSITION BREAKDOWN
# ====================================

st.subheader("Position Breakdown")

position_map = {
    1: "Goalkeepers",
    2: "Defenders",
    3: "Midfielders",
    4: "Forwards"
}

position_counts = (
    best_xi["Position"]
    .map(position_map)
    .value_counts()
)

st.bar_chart(position_counts)