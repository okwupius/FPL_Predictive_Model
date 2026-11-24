import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Fixture Heatmap",
    layout="wide"
)

st.title("🔥 Fixture Difficulty Heatmap")

# ====================================
# LOAD DATA
# ====================================

my_team = pd.read_csv(
    "data/my_team.csv"
)

forecast = pd.read_csv(
    "data/processed/forecast_v11.csv"
)

rankings = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

# ====================================
# MERGE DATA
# ====================================

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
            "Home_Game"
        ]
    ],
    on="player_id",
    how="left"
)

# Use the merged columns created in your environment

team = team.rename(
    columns={
        "Opponent_y": "Opponent",
        "Fixture_Difficulty_y": "Difficulty",
        "Home_Game_y": "Home_Game"
    }
)

# ====================================
# DIFFICULTY COLOUR FUNCTION
# ====================================

def difficulty_icon(value):

    if value <= 2:
        return "🟢 Easy"

    elif value == 3:
        return "🟡 Medium"

    else:
        return "🔴 Hard"

# ====================================
# DISPLAY TABLE
# ====================================

heatmap = team[
    [
        "First_Name",
        "Last_Name",
        "Opponent",
        "Difficulty",
        "Home_Game",
        "Projected_Points"
    ]
].copy()

heatmap["Player"] = (
    heatmap["First_Name"]
    + " "
    + heatmap["Last_Name"]
)

heatmap["Fixture Rating"] = (
    heatmap["Difficulty"]
    .apply(difficulty_icon)
)

heatmap["Venue"] = (
    heatmap["Home_Game"]
    .apply(
        lambda x:
        "🏠 Home"
        if x == 1
        else "✈️ Away"
    )
)

heatmap = heatmap[
    [
        "Player",
        "Opponent",
        "Venue",
        "Difficulty",
        "Fixture Rating",
        "Projected_Points"
    ]
].sort_values(
    "Difficulty"
)

st.subheader("Fixture Overview")

st.dataframe(
    heatmap,
    width="stretch",
    hide_index=True
)

# ====================================
# EASIEST FIXTURES
# ====================================

st.subheader("🟢 Best Fixtures")

best = heatmap.head(5)

st.dataframe(
    best,
    width="stretch",
    hide_index=True
)

# ====================================
# HARDEST FIXTURES
# ====================================

st.subheader("🔴 Worst Fixtures")

worst = heatmap.tail(5)

st.dataframe(
    worst,
    width="stretch",
    hide_index=True
)

# ====================================
# CHART
# ====================================

st.subheader("Fixture Difficulty Chart")

chart = heatmap.copy()

chart = chart.set_index(
    "Player"
)

st.bar_chart(
    chart["Difficulty"]
)

# ====================================
# FIXTURE ALERTS
# ====================================

st.subheader("🚨 Fixture Alerts")

easy_players = team[
    team["Difficulty"] <= 2
]

hard_players = team[
    team["Difficulty"] >= 4
]

if len(easy_players) > 0:

    st.success(
        f"{len(easy_players)} player(s) have favourable fixtures."
    )

if len(hard_players) > 0:

    st.warning(
        f"{len(hard_players)} player(s) have difficult fixtures."
    )

# ====================================
# TOP CAPTAINCY OPTIONS
# ====================================

st.subheader("👑 Fixture-Based Captaincy")

captains = team.sort_values(
    [
        "Difficulty",
        "Projected_Points"
    ],
    ascending=[True, False]
)

st.dataframe(
    captains[
        [
            "First_Name",
            "Last_Name",
            "Difficulty",
            "Projected_Points"
        ]
    ].head(5),
    width="stretch",
    hide_index=True
)