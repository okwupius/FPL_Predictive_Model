import streamlit as st
import pandas as pd
from itertools import combinations

st.set_page_config(
    page_title="Smart Transfer Planner",
    layout="wide"
)

st.title("🧠 Smart Transfer Planner")

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

team["Player"] = (
    team["First_Name"]
    + " "
    + team["Last_Name"]
)

owned_players = set(
    zip(
        team["First_Name"],
        team["Last_Name"]
    )
)

# =====================================
# BUILD BEST TRANSFER FOR EACH PLAYER
# =====================================

transfer_options = []

for _, player in team.iterrows():

    replacements = rankings[
        rankings["Position"]
        == player["Position"]
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
        <= player["Price"] + 1.0
    ]

    if len(replacements) == 0:
        continue

    best = (
        replacements
        .sort_values(
            "Projected_Points",
            ascending=False
        )
        .iloc[0]
    )

    gain = (
        best["Projected_Points"]
        - player["Projected_Points"]
    )

    transfer_options.append(
        {
            "Sell":
                player["Player"],
            "Buy":
                f"{best['First_Name']} {best['Last_Name']}",
            "Gain":
                round(gain, 2),
            "Sell_Price":
                player["Price"],
            "Buy_Price":
                best["Price"]
        }
    )

transfers = pd.DataFrame(
    transfer_options
)

transfers = transfers.sort_values(
    "Gain",
    ascending=False
)

# =====================================
# METRICS
# =====================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Possible Transfers",
    len(transfers)
)

col2.metric(
    "Best Gain",
    f"+{transfers.iloc[0]['Gain']:.2f}"
)

col3.metric(
    "Team Projection",
    f"{team['Projected_Points'].sum():.2f}"
)

# =====================================
# BEST SINGLE TRANSFER
# =====================================

st.subheader("🏆 Best Single Transfer")

st.dataframe(
    transfers.head(1),
    width="stretch",
    hide_index=True
)

# =====================================
# BEST DOUBLE TRANSFER
# =====================================

best_two_gain = -999
best_two = None

for combo in combinations(
    transfers.index,
    2
):

    rows = transfers.loc[list(combo)]

    if rows["Buy"].nunique() < len(rows):
        continue

    if rows["Sell"].nunique() < len(rows):
        continue

    total_gain = rows["Gain"].sum()

    if total_gain > best_two_gain:

        best_two_gain = total_gain
        best_two = rows

st.subheader("🥈 Best Double Transfer")

st.dataframe(
    best_two,
    width="stretch",
    hide_index=True
)

st.success(
    f"Combined Gain: +{best_two_gain:.2f}"
)

# =====================================
# BEST TRIPLE TRANSFER
# =====================================

best_three_gain = -999
best_three = None

for combo in combinations(
    transfers.index,
    3
):

    rows = transfers.loc[list(combo)]

    # No duplicate buys

    if rows["Buy"].nunique() < len(rows):
        continue

    # No duplicate sells

    if rows["Sell"].nunique() < len(rows):
        continue

    total_gain = rows["Gain"].sum()

    if total_gain > best_three_gain:

        best_three_gain = total_gain
        best_three = rows

st.subheader("🥉 Best Triple Transfer")

st.dataframe(
    best_three,
    width="stretch",
    hide_index=True
)

st.success(
    f"Combined Gain: +{best_three_gain:.2f}"
)

# =====================================
# HIT CALCULATOR
# =====================================

st.subheader("🎯 Hit Analysis")

free_transfers = st.slider(
    "Available Free Transfers",
    0,
    3,
    1
)

for count, gain in [
    (1, transfers.head(1)["Gain"].sum()),
    (2, best_two_gain),
    (3, best_three_gain)
]:

    cost = max(
        0,
        count - free_transfers
    ) * 4

    net_gain = gain - cost

    st.write(
        f"**{count} Transfer(s)** | "
        f"Gain: +{gain:.2f} | "
        f"Hit: -{cost} | "
        f"Net: {net_gain:.2f}"
    )

# =====================================
# TOP 10 TRANSFERS
# =====================================

st.subheader("📈 Top Transfer Targets")

st.dataframe(
    transfers.head(10),
    width="stretch",
    hide_index=True
)

# =====================================
# CHART
# =====================================

st.subheader("Transfer Gain Rankings")

chart = (
    transfers
    .head(10)
    .copy()
)

chart["Transfer"] = (
    chart["Sell"]
    + " → "
    + chart["Buy"]
)

chart = chart.set_index(
    "Transfer"
)

st.bar_chart(
    chart["Gain"]
)