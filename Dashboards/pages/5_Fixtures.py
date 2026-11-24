import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Fixture Analysis",
    layout="wide"
)

st.title("📅 Fixture Analysis")

# =====================================
# LOAD DATA
# =====================================

my_team = pd.read_csv(
    "data/my_team.csv"
)

forecast = pd.read_csv(
    "data/processed/forecast_v11.csv"
)

rankings = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

# =====================================
# MERGE
# =====================================

team = my_team.merge(
    rankings,
    on=["First_Name", "Last_Name"],
    how="left"
)

team = team.merge(
    forecast[
        [
            "player_id",
            "Opponent",
            "Fixture_Difficulty",
            "Home_Game",
            "Opponent_Attack_Strength",
            "Opponent_Defence_Strength"
        ]
    ],
    on="player_id",
    how="left"
)

# =====================================
# METRICS
# =====================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Players",
    len(team)
)

col2.metric(
    "Average Fixture Difficulty",
    round(
        team["Fixture_Difficulty_y"].mean(),
        2
    )
)

col3.metric(
    "Average Projection",
    round(
        team["Projected_Points"].mean(),
        2
    )
)

# =====================================
# EASIEST FIXTURES
# =====================================

st.subheader("🟢 Easiest Fixtures")

easy = team.sort_values(
    "Fixture_Difficulty_y"
)

st.dataframe(
    easy[
        [
            "First_Name",
            "Last_Name",
            "Projected_Points",
            "Fixture_Difficulty_y",
            "Opponent_y",
            "Home_Game_y"
        ]
    ],
    width="stretch",
    hide_index=True
)

# =====================================
# HARDEST FIXTURES
# =====================================

st.subheader("🔴 Hardest Fixtures")

hard = team.sort_values(
    "Fixture_Difficulty_y",
    ascending=False
)

st.dataframe(
    hard[
        [
            "First_Name",
            "Last_Name",
            "Projected_Points",
            "Fixture_Difficulty_y",
            "Opponent_y",
            "Home_Game_y"
        ]
    ],
    width="stretch",
    hide_index=True
)

# =====================================
# PLAYER FIXTURE SCOUT
# =====================================

st.subheader("🔎 Fixture Scout")

player_name = st.selectbox(
    "Select Player",
    sorted(
        (
            team["First_Name"]
            + " "
            + team["Last_Name"]
        ).tolist()
    )
)

player = team[
    (
        team["First_Name"]
        + " "
        + team["Last_Name"]
    ) == player_name
].iloc[0]

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Projection",
    f"{player['Projected_Points']:.2f}"
)

c2.metric(
    "Difficulty",
    player["Fixture_Difficulty_y"]
)

c3.metric(
    "Opponent",
    player["Opponent_y"]
)

c4.metric(
    "Home",
    "Yes" if player["Home_Game_y"] == 1 else "No"
)

# =====================================
# CHART
# =====================================

st.subheader("📈 Fixture Difficulty Chart")

chart = team[
    [
        "First_Name",
        "Last_Name",
        "Fixture_Difficulty_y"
    ]
].copy()

chart["Player"] = (
    chart["First_Name"]
    + " "
    + chart["Last_Name"]
)

chart = chart.set_index("Player")

st.bar_chart(
    chart["Fixture_Difficulty_y"]
)