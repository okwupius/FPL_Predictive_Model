import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Transfer Centre",
    layout="wide"
)

st.title("🔄 Transfer Centre")

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

owned_players = set(
    zip(
        team["First_Name"],
        team["Last_Name"]
    )
)

# =====================================
# BUILD RECOMMENDATIONS
# =====================================

recommendations = []

for _, player in team.iterrows():

    position = player["Position"]

    replacements = rankings[
        rankings["Position"] == position
    ].copy()

    # Remove owned players
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

    # Budget filter
    replacements = replacements[
        replacements["Price"]
        <= player["Price"] + 1.0
    ]

    if len(replacements) == 0:
        continue

    replacement = (
        replacements
        .sort_values(
            "Projected_Points",
            ascending=False
        )
        .iloc[0]
    )

    gain = (
        replacement["Projected_Points"]
        - player["Projected_Points"]
    )

    priority_score = (
        gain
        + (player["Rank"] / 100)
    )

    recommendations.append(
        {
            "Sell":
                f"{player['First_Name']} {player['Last_Name']}",
            "Buy":
                f"{replacement['First_Name']} {replacement['Last_Name']}",
            "Position":
                player["Position"],
            "Sell Rank":
                int(player["Rank"]),
            "Sell Projection":
                round(player["Projected_Points"], 2),
            "Buy Projection":
                round(replacement["Projected_Points"], 2),
            "Gain":
                round(gain, 2),
            "Priority Score":
                round(priority_score, 2)
        }
    )

transfers = pd.DataFrame(
    recommendations
)

transfers = transfers.sort_values(
    "Priority Score",
    ascending=False
)

# =====================================
# TOP METRICS
# =====================================

best_transfer = transfers.iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Best Gain",
    f"+{best_transfer['Gain']:.2f}"
)

col2.metric(
    "Priority Score",
    f"{best_transfer['Priority Score']:.2f}"
)

col3.metric(
    "Transfer Count",
    len(transfers)
)

# =====================================
# BEST TRANSFER
# =====================================

st.subheader("🏆 Best Transfer")

st.success(
    f"SELL: {best_transfer['Sell']}  →  BUY: {best_transfer['Buy']}"
)

# =====================================
# TOP 10 TRANSFERS
# =====================================

st.subheader("📈 Top 10 Transfer Priorities")

st.dataframe(
    transfers.head(10),
    width="stretch"
)

# =====================================
# POSITION FILTER
# =====================================

st.subheader("🎯 Position-Specific Transfers")

position_map = {
    1: "Goalkeepers",
    2: "Defenders",
    3: "Midfielders",
    4: "Forwards"
}

selected_position = st.selectbox(
    "Choose Position",
    options=[
        1,
        2,
        3,
        4
    ],
    format_func=lambda x:
    position_map[x]
)

filtered = transfers[
    transfers["Position"]
    == selected_position
]

st.dataframe(
    filtered,
    width="stretch"
)

# =====================================
# SELL CANDIDATES
# =====================================

st.subheader("🚨 Sell Candidates")

sell_candidates = (
    team.sort_values(
        "Projected_Points"
    )
    [
        [
            "First_Name",
            "Last_Name",
            "Price",
            "Rank",
            "Projected_Points"
        ]
    ]
)

st.dataframe(
    sell_candidates.head(10),
    width="stretch"
)