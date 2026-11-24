import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Player Rankings",
    layout="wide"
)

st.title("📊 Player Rankings")

# ====================================
# LOAD DATA
# ====================================

rankings = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

rankings["Points_Per_Million"] = (
    rankings["Projected_Points"]
    / rankings["Price"]
)

# ====================================
# SIDEBAR FILTERS
# ====================================

st.sidebar.header("Filters")

position_map = {
    1: "Goalkeeper",
    2: "Defender",
    3: "Midfielder",
    4: "Forward"
}

position_filter = st.sidebar.selectbox(
    "Position",
    ["All"] + list(position_map.values())
)

max_price = float(
    rankings["Price"].max()
)

price_filter = st.sidebar.slider(
    "Maximum Price (£m)",
    min_value=3.5,
    max_value=max_price,
    value=max_price
)

search_player = st.sidebar.text_input(
    "Search Player"
)

# ====================================
# APPLY FILTERS
# ====================================

filtered = rankings.copy()

if position_filter != "All":

    reverse_map = {
        v: k for k, v in position_map.items()
    }

    filtered = filtered[
        filtered["Position"]
        == reverse_map[position_filter]
    ]

filtered = filtered[
    filtered["Price"] <= price_filter
]

if search_player:

    filtered = filtered[
        (
            filtered["First_Name"]
            .str.contains(
                search_player,
                case=False,
                na=False
            )
        )
        |
        (
            filtered["Last_Name"]
            .str.contains(
                search_player,
                case=False,
                na=False
            )
        )
    ]

# ====================================
# TOP METRICS
# ====================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Players",
    len(filtered)
)

col2.metric(
    "Highest Projection",
    f"{filtered['Projected_Points'].max():.2f}"
)

col3.metric(
    "Highest Value",
    f"{filtered['Points_Per_Million'].max():.2f}"
)

# ====================================
# TOP PLAYERS
# ====================================

st.subheader("🏆 Top 25 Projected Players")

top_players = (
    filtered.sort_values(
        "Projected_Points",
        ascending=False
    )
    [
        [
            "First_Name",
            "Last_Name",
            "Position",
            "Price",
            "Projected_Points",
            "Rank"
        ]
    ]
    .head(25)
)

st.dataframe(
    top_players,
    width="stretch",
    hide_index=True
)

# ====================================
# BEST VALUE PLAYERS
# ====================================

st.subheader("💰 Top 25 Value Players")

value_players = (
    filtered.sort_values(
        "Points_Per_Million",
        ascending=False
    )
    [
        [
            "First_Name",
            "Last_Name",
            "Position",
            "Price",
            "Projected_Points",
            "Points_Per_Million"
        ]
    ]
    .head(25)
)

st.dataframe(
    value_players,
    width="stretch",
    hide_index=True
)

# ====================================
# PLAYER EXPLORER
# ====================================

st.subheader("🔎 Player Explorer")

player_name = st.selectbox(
    "Select a Player",
    sorted(
        (
            filtered["First_Name"]
            + " "
            + filtered["Last_Name"]
        ).unique()
    )
)

player = filtered[
    (
        filtered["First_Name"]
        + " "
        + filtered["Last_Name"]
    ) == player_name
].iloc[0]

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Price",
    f"£{player['Price']:.1f}"
)

c2.metric(
    "Projection",
    f"{player['Projected_Points']:.2f}"
)

c3.metric(
    "Rank",
    int(player["Rank"])
)

c4.metric(
    "Value",
    f"{player['Points_Per_Million']:.2f}"
)

# ====================================
# CHARTS
# ====================================

st.subheader("📈 Top 15 Projections")

chart_df = (
    filtered.sort_values(
        "Projected_Points",
        ascending=False
    )
    .head(15)
)

chart_df = chart_df.set_index(
    chart_df["First_Name"]
    + " "
    + chart_df["Last_Name"]
)

st.bar_chart(
    chart_df["Projected_Points"]
)

st.subheader("📈 Top 15 Value Players")

value_chart = (
    filtered.sort_values(
        "Points_Per_Million",
        ascending=False
    )
    .head(15)
)

value_chart = value_chart.set_index(
    value_chart["First_Name"]
    + " "
    + value_chart["Last_Name"]
)

st.bar_chart(
    value_chart["Points_Per_Million"]
)