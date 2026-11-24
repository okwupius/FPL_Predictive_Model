import streamlit as st
import pandas as pd
from itertools import combinations

st.set_page_config(
    page_title="Transfer Command Center",
    layout="wide"
)

st.title("🎯 Transfer Command Center")

# ==================================================
# LOAD DATA
# ==================================================

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

rankings["Player"] = (
    rankings["First_Name"]
    + " "
    + rankings["Last_Name"]
)

owned_players = set(
    zip(
        team["First_Name"],
        team["Last_Name"]
    )
)

# ==================================================
# BUILD TRANSFER LIST
# ==================================================

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

    priority = (
        gain
        + player["Rank"] / 100
    )

    transfer_options.append(
        {
            "Sell": player["Player"],
            "Buy": f"{best['First_Name']} {best['Last_Name']}",
            "Gain": round(gain, 2),
            "Priority": round(priority, 2),
            "Sell_Price": player["Price"],
            "Buy_Price": best["Price"]
        }
    )

transfers = pd.DataFrame(
    transfer_options
)

transfers = transfers.sort_values(
    "Priority",
    ascending=False
)

# ==================================================
# TOP METRICS
# ==================================================

best_transfer = transfers.iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Best Gain",
    f"+{best_transfer['Gain']:.2f}"
)

col2.metric(
    "Priority Score",
    f"{best_transfer['Priority']:.2f}"
)

col3.metric(
    "Transfer Options",
    len(transfers)
)

# ==================================================
# BEST SINGLE TRANSFER
# ==================================================

st.subheader("🏆 Best Single Transfer")

st.success(
    f"SELL: {best_transfer['Sell']} → BUY: {best_transfer['Buy']}"
)

st.dataframe(
    transfers.head(1),
    width="stretch",
    hide_index=True
)

# ==================================================
# BEST DOUBLE TRANSFER
# ==================================================

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

# ==================================================
# BEST TRIPLE TRANSFER
# ==================================================

best_three_gain = -999
best_three = None

for combo in combinations(
    transfers.index,
    3
):

    rows = transfers.loc[list(combo)]

    if rows["Buy"].nunique() < len(rows):
        continue

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

# ==================================================
# SELL CANDIDATES
# ==================================================

st.subheader("🚨 Sell Candidates")

sell_candidates = (
    team.sort_values(
        "Projected_Points"
    )
)

st.dataframe(
    sell_candidates[
        [
            "Player",
            "Projected_Points",
            "Rank",
            "Price"
        ]
    ].head(5),
    width="stretch",
    hide_index=True
)

# ==================================================
# TOP TRANSFER TARGETS
# ==================================================

st.subheader("⭐ Top Transfer Targets")

display = (
    transfers[
        [
            "Sell",
            "Buy",
            "Gain",
            "Priority"
        ]
    ]
    .head(10)
    .copy()
)

display["Gain"] = display["Gain"].apply(
    lambda x:
    f"🟢 +{x:.2f}"
    if x >= 5
    else (
        f"🟡 +{x:.2f}"
        if x > 0
        else f"🔴 {x:.2f}"
    )
)

st.dataframe(
    display,
    width="stretch",
    hide_index=True
)

# ==================================================
# HIT ANALYSIS
# ==================================================

st.subheader("⚡ Hit Calculator")

free_transfers = st.slider(
    "Free Transfers Available",
    0,
    3,
    1
)

for transfer_count, gain in [
    (1, transfers.head(1)["Gain"].sum()),
    (2, best_two_gain),
    (3, best_three_gain)
]:

    cost = (
        max(
            0,
            transfer_count - free_transfers
        ) * 4
    )

    net = gain - cost

    if net > 0:

        st.success(
            f"{transfer_count} Transfer(s) → "
            f"Gain +{gain:.2f} | "
            f"Hit -{cost} | "
            f"Net +{net:.2f}"
        )

    else:

        st.error(
            f"{transfer_count} Transfer(s) → "
            f"Gain +{gain:.2f} | "
            f"Hit -{cost} | "
            f"Net {net:.2f}"
        )

# ==================================================
# GAIN CHART
# ==================================================

st.subheader("📈 Transfer Gain Chart")

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