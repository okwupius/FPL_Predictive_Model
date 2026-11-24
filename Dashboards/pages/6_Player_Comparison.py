import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Player Comparison",
    layout="wide"
)

st.title("⚔️ Player Comparison Tool")

# ====================================
# LOAD DATA
# ====================================

rankings = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

rankings["Points_Per_Million"] = (
    rankings["Projected_Points"] /
    rankings["Price"]
)

rankings["Player"] = (
    rankings["First_Name"]
    + " "
    + rankings["Last_Name"]
)

# ====================================
# PLAYER SELECTORS
# ====================================

players = sorted(
    rankings["Player"].unique()
)

col1, col2 = st.columns(2)

with col1:
    player1_name = st.selectbox(
        "Player 1",
        players,
        index=0
    )

with col2:
    player2_name = st.selectbox(
        "Player 2",
        players,
        index=1
    )

player1 = rankings[
    rankings["Player"] == player1_name
].iloc[0]

player2 = rankings[
    rankings["Player"] == player2_name
].iloc[0]

# ====================================
# HEADER METRICS
# ====================================

st.subheader("Comparison Summary")

c1, c2 = st.columns(2)

with c1:

    st.metric(
        player1_name,
        f"{player1['Projected_Points']:.2f} pts",
        help="Projected Points"
    )

with c2:

    st.metric(
        player2_name,
        f"{player2['Projected_Points']:.2f} pts",
        help="Projected Points"
    )

# ====================================
# DETAILED COMPARISON
# ====================================

comparison = pd.DataFrame(
    {
        "Metric": [
            "Rank",
            "Price",
            "Projected Points",
            "Points Per Million",
            "Position"
        ],

        player1_name: [
            int(player1["Rank"]),
            round(player1["Price"], 1),
            round(player1["Projected_Points"], 2),
            round(player1["Points_Per_Million"], 2),
            int(player1["Position"])
        ],

        player2_name: [
            int(player2["Rank"]),
            round(player2["Price"], 1),
            round(player2["Projected_Points"], 2),
            round(player2["Points_Per_Million"], 2),
            int(player2["Position"])
        ]
    }
)

st.subheader("Detailed Comparison")

st.dataframe(
    comparison,
    width="stretch",
    hide_index=True
)

# ====================================
# WINNER ANALYSIS
# ====================================

st.subheader("Winner Analysis")

winner_projection = (
    player1_name
    if player1["Projected_Points"]
       > player2["Projected_Points"]
    else player2_name
)

winner_value = (
    player1_name
    if player1["Points_Per_Million"]
       > player2["Points_Per_Million"]
    else player2_name
)

winner_rank = (
    player1_name
    if player1["Rank"]
       < player2["Rank"]
    else player2_name
)

st.success(
    f"Best Projection: {winner_projection}"
)

st.success(
    f"Best Value: {winner_value}"
)

st.success(
    f"Best Rank: {winner_rank}"
)

# ====================================
# VISUAL CHARTS
# ====================================

st.subheader("Projection Comparison")

projection_chart = pd.DataFrame(
    {
        "Projected Points": [
            player1["Projected_Points"],
            player2["Projected_Points"]
        ]
    },
    index=[
        player1_name,
        player2_name
    ]
)

st.bar_chart(
    projection_chart
)

st.subheader("Value Comparison")

value_chart = pd.DataFrame(
    {
        "Points Per Million": [
            player1["Points_Per_Million"],
            player2["Points_Per_Million"]
        ]
    },
    index=[
        player1_name,
        player2_name
    ]
)

st.bar_chart(
    value_chart
)

# ====================================
# TRANSFER RECOMMENDATION
# ====================================

st.subheader("Transfer Verdict")

projection_gain = (
    player2["Projected_Points"]
    - player1["Projected_Points"]
)

if projection_gain > 0:

    st.success(
        f"Moving from {player1_name} "
        f"to {player2_name} gains "
        f"{projection_gain:.2f} projected points."
    )

elif projection_gain < 0:

    st.warning(
        f"Moving from {player1_name} "
        f"to {player2_name} loses "
        f"{abs(projection_gain):.2f} projected points."
    )

else:

    st.info(
        "Both players are projected equally."
    )
    