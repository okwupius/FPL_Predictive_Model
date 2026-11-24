import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Multi-Transfer Planner",
    layout="wide"
)

st.title("🧮 Multi-Transfer Planner")

# =====================================
# LOAD DATA
# =====================================

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

# =====================================
# CURRENT TEAM SCORE
# =====================================

current_score = team[
    "Projected_Points"
].sum()

team["Player"] = (
    team["First_Name"]
    + " "
    + team["Last_Name"]
)

rankings["Player"] = (
    rankings["First_Name"]
    + " "
    + rankings["Last_Name"]
)

# =====================================
# TRANSFER COUNT
# =====================================

num_transfers = st.slider(
    "Number of Transfers",
    min_value=1,
    max_value=3,
    value=2
)

transfers = []

st.subheader("Transfer Plan")

for i in range(num_transfers):

    st.markdown(
        f"### Transfer {i + 1}"
    )

    col1, col2 = st.columns(2)

    with col1:

        sell_player = st.selectbox(
            f"Sell Player {i+1}",
            team["Player"],
            key=f"sell_{i}"
        )

    seller = team[
        team["Player"] == sell_player
    ].iloc[0]

    same_position = rankings[
        rankings["Position"]
        == seller["Position"]
    ]

    owned = set(
        team["Player"]
    )

    same_position = same_position[
        ~same_position["Player"].isin(
            owned
        )
    ]

    with col2:

        buy_player = st.selectbox(
            f"Buy Player {i+1}",
            same_position[
                "Player"
            ].sort_values(),
            key=f"buy_{i}"
        )

    buyer = rankings[
        rankings["Player"] == buy_player
    ].iloc[0]

    transfers.append(
        (
            seller,
            buyer
        )
    )

# =====================================
# CALCULATIONS
# =====================================

new_score = current_score

current_value = team[
    "Price"
].sum()

new_value = current_value

total_gain = 0

transfer_summary = []

for seller, buyer in transfers:

    gain = (
        buyer["Projected_Points"]
        - seller["Projected_Points"]
    )

    value_change = (
        buyer["Price"]
        - seller["Price"]
    )

    total_gain += gain
    new_score += gain
    new_value += value_change

    transfer_summary.append(
        {
            "Sell":
                seller["Player"],
            "Buy":
                buyer["Player"],
            "Gain":
                round(gain, 2),
            "Price Change":
                round(value_change, 2)
        }
    )

summary_df = pd.DataFrame(
    transfer_summary
)

# =====================================
# METRICS
# =====================================

st.subheader("Impact Analysis")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Current Score",
    f"{current_score:.2f}"
)

col2.metric(
    "New Score",
    f"{new_score:.2f}"
)

col3.metric(
    "Total Gain",
    f"+{total_gain:.2f}"
)

col4.metric(
    "Team Value",
    f"£{new_value:.1f}m"
)

# =====================================
# TEAM COMPARISON
# =====================================

st.subheader(
    "Transfer Summary"
)

st.dataframe(
    summary_df,
    width="stretch",
    hide_index=True
)

# =====================================
# HIT CALCULATOR
# =====================================

st.subheader(
    "Points Hit Analysis"
)

free_transfers = st.slider(
    "Available Free Transfers",
    min_value=0,
    max_value=3,
    value=1
)

extra_transfers = max(
    0,
    num_transfers - free_transfers
)

hit_cost = extra_transfers * 4

net_gain = (
    total_gain - hit_cost
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Hit Cost",
    f"-{hit_cost}"
)

col2.metric(
    "Raw Gain",
    f"+{total_gain:.2f}"
)

col3.metric(
    "Net Gain",
    f"{net_gain:.2f}"
)

if net_gain > 4:

    st.success(
        "✅ Transfer plan appears worthwhile based on model projections."
    )

elif net_gain > 0:

    st.warning(
        "⚠ Positive gain, but benefit is modest."
    )

else:

    st.error(
        "❌ Hit cost outweighs projected benefit."
    )

# =====================================
# VISUAL COMPARISON
# =====================================

st.subheader("Before vs After")

comparison = pd.DataFrame(
    {
        "Score": [
            current_score,
            new_score
        ]
    },
    index=[
        "Current Team",
        "After Transfers"
    ]
)

st.bar_chart(comparison)