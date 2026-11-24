import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Transfer Simulator",
    layout="wide"
)

st.title("🔄 Transfer Simulator")

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
# SELECT PLAYER TO SELL
# =====================================

team["Player"] = (
    team["First_Name"]
    + " "
    + team["Last_Name"]
)

sell_player = st.selectbox(
    "Select player to sell",
    sorted(team["Player"].tolist())
)

current_player = team[
    team["Player"] == sell_player
].iloc[0]

st.subheader("Current Player")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Price",
    f"£{current_player['Price']:.1f}"
)

col2.metric(
    "Projection",
    f"{current_player['Projected_Points']:.2f}"
)

col3.metric(
    "Rank",
    int(current_player["Rank"])
)

col4.metric(
    "Position",
    int(current_player["Position"])
)

# =====================================
# SETTINGS
# =====================================

st.subheader("Transfer Settings")

extra_budget = st.slider(
    "Extra Budget Available (£m)",
    min_value=0.0,
    max_value=10.0,
    value=1.0,
    step=0.1
)

# =====================================
# FIND REPLACEMENTS
# =====================================

replacements = rankings[
    rankings["Position"]
    == current_player["Position"]
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
    <= current_player["Price"] + extra_budget
]

replacements = replacements.copy()

replacements["Gain"] = (
    replacements["Projected_Points"]
    - current_player["Projected_Points"]
)

replacements = replacements.sort_values(
    "Gain",
    ascending=False
)

# =====================================
# BEST REPLACEMENT
# =====================================

if len(replacements) > 0:

    best = replacements.iloc[0]

    st.subheader("🏆 Best Replacement")

    st.success(
        f"{sell_player} ➜ "
        f"{best['First_Name']} "
        f"{best['Last_Name']}"
    )

    b1, b2, b3 = st.columns(3)

    b1.metric(
        "Point Gain",
        f"+{best['Gain']:.2f}"
    )

    b2.metric(
        "New Projection",
        f"{best['Projected_Points']:.2f}"
    )

    b3.metric(
        "Price",
        f"£{best['Price']:.1f}"
    )

# =====================================
# TOP REPLACEMENTS
# =====================================

st.subheader("📈 Top Replacement Options")

display_df = (
    replacements[
        [
            "First_Name",
            "Last_Name",
            "Price",
            "Projected_Points",
            "Points_Per_Million",
            "Gain",
            "Rank"
        ]
    ]
    .head(20)
)

st.dataframe(
    display_df,
    width="stretch",
    hide_index=True
)

# =====================================
# CHART
# =====================================

st.subheader("Projected Gain")

chart = (
    replacements[
        [
            "First_Name",
            "Last_Name",
            "Gain"
        ]
    ]
    .head(10)
    .copy()
)

chart["Player"] = (
    chart["First_Name"]
    + " "
    + chart["Last_Name"]
)

chart = chart.set_index(
    "Player"
)

st.bar_chart(
    chart["Gain"]
)
