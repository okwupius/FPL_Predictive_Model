import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="FPL Command Center",
    layout="wide"
)

st.title("⚽ FPL Command Center")

# ==========================================
# LOAD DATA
# ==========================================

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

team["Player"] = (
    team["First_Name"]
    + " "
    + team["Last_Name"]
)

# ==========================================
# HEALTH
# ==========================================

avg_rank = team["Rank"].mean()

health_score = max(
    0,
    min(
        100,
        round(100 - avg_rank / 4, 1)
    )
)

# ==========================================
# BEST PLAYER / CAPTAIN
# ==========================================

captain = (
    team
    .sort_values(
        "Projected_Points",
        ascending=False
    )
    .iloc[0]
)

# ==========================================
# SELL CANDIDATE
# ==========================================

worst_player = (
    team
    .sort_values(
        "Projected_Points"
    )
    .iloc[0]
)

# ==========================================
# METRICS
# ==========================================

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Health Score",
    f"{health_score}/100"
)

m2.metric(
    "Squad Value",
    f"£{team['Price'].sum():.1f}m"
)

m3.metric(
    "Average Rank",
    f"{avg_rank:.1f}"
)

m4.metric(
    "Projected Score",
    f"{team['Projected_Points'].sum():.2f}"
)

# ==========================================
# GAMEWEEK SUMMARY
# ==========================================

st.subheader("🎯 This Week")

col1, col2 = st.columns(2)

with col1:

    st.success(
        f"👑 Captain: "
        f"{captain['First_Name']} "
        f"{captain['Last_Name']} "
        f"({captain['Projected_Points']:.2f} pts)"
    )

with col2:

    st.warning(
        f"🚨 Weakest Asset: "
        f"{worst_player['First_Name']} "
        f"{worst_player['Last_Name']} "
        f"({worst_player['Projected_Points']:.2f} pts)"
    )

# ==========================================
# ACTIONS
# ==========================================

st.subheader("✅ Weekly Workflow")

st.info(
    """
1. Open **Transfer Command Center**
2. Review **Smart Transfer Planner**
3. Check **Fixture Runs**
4. Review **Best XI**
5. Confirm Captain
"""
)

# ==========================================
# TOP PLAYERS
# ==========================================

st.subheader("🏆 Top Assets")

top_assets = (
    team[
        [
            "Player",
            "Projected_Points",
            "Rank",
            "Price"
        ]
    ]
    .sort_values(
        "Projected_Points",
        ascending=False
    )
    .head(5)
)

st.dataframe(
    top_assets,
    width="stretch",
    hide_index=True
)

# ==========================================
# PROBLEM PLAYERS
# ==========================================

st.subheader("🚨 Problem Players")

problem_players = (
    team[
        [
            "Player",
            "Projected_Points",
            "Rank",
            "Price"
        ]
    ]
    .sort_values(
        "Projected_Points"
    )
    .head(5)
)

st.dataframe(
    problem_players,
    width="stretch",
    hide_index=True
)