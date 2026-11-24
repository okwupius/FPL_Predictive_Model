import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Watchlist",
    layout="wide"
)

st.title("⭐ Transfer Watchlist")

# ====================================
# LOAD DATA
# ====================================

rankings = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

watchlist = pd.read_csv(
    "data/watchlist.csv"
)

# ====================================
# BUILD WATCHLIST
# ====================================

watch = watchlist.merge(
    rankings,
    on=["First_Name", "Last_Name"],
    how="left"
)

watch["Points_Per_Million"] = (
    watch["Projected_Points"]
    / watch["Price"]
)

watch["Player"] = (
    watch["First_Name"]
    + " "
    + watch["Last_Name"]
)

# ====================================
# METRICS
# ====================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Players Watched",
    len(watch)
)

col2.metric(
    "Best Projection",
    f"{watch['Projected_Points'].max():.2f}"
)

col3.metric(
    "Best Value",
    f"{watch['Points_Per_Million'].max():.2f}"
)

# ====================================
# WATCHLIST TABLE
# ====================================

st.subheader("Current Watchlist")

display = (
    watch[
        [
            "Player",
            "Price",
            "Projected_Points",
            "Rank",
            "Points_Per_Million"
        ]
    ]
    .sort_values(
        "Projected_Points",
        ascending=False
    )
)

st.dataframe(
    display,
    width="stretch",
    hide_index=True
)

# ====================================
# TOP TARGET
# ====================================

best = (
    watch.sort_values(
        "Projected_Points",
        ascending=False
    )
    .iloc[0]
)

st.success(
    f"Top Target: {best['First_Name']} "
    f"{best['Last_Name']} "
    f"({best['Projected_Points']:.2f} pts)"
)

# ====================================
# PLAYER SCOUT
# ====================================

st.subheader("Scout Watchlist Player")

player_name = st.selectbox(
    "Select Player",
    watch["Player"]
)

player = watch[
    watch["Player"] == player_name
].iloc[0]

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Rank",
    int(player["Rank"])
)

c2.metric(
    "Price",
    f"£{player['Price']:.1f}"
)

c3.metric(
    "Projection",
    f"{player['Projected_Points']:.2f}"
)

c4.metric(
    "Value",
    f"{player['Points_Per_Million']:.2f}"
)

# ====================================
# CHARTS
# ====================================

st.subheader("Projection Comparison")

chart = watch.set_index(
    "Player"
)

st.bar_chart(
    chart["Projected_Points"]
)

st.subheader("Value Comparison")

st.bar_chart(
    chart["Points_Per_Million"]
)