import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="FPL Assistant",
    layout="wide"
)

st.title("🧠 FPL Assistant")

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

# =====================================
# HEALTH SCORE
# =====================================

avg_rank = team["Rank"].mean()

health_score = max(
    0,
    min(
        100,
        round(
            100 - (avg_rank / 4),
            1
        )
    )
)

if health_score >= 80:
    health_status = "🟢 Excellent"
elif health_score >= 60:
    health_status = "🟡 Good"
else:
    health_status = "🔴 Needs Attention"

# =====================================
# CAPTAIN & VICE
# =====================================

captain = (
    team
    .sort_values(
        "Projected_Points",
        ascending=False
    )
    .iloc[0]
)

vice = (
    team
    .sort_values(
        "Projected_Points",
        ascending=False
    )
    .iloc[1]
)

# =====================================
# BEST TRANSFER
# =====================================

owned_players = set(
    zip(
        team["First_Name"],
        team["Last_Name"]
    )
)

recommendations = []

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

    priority = (
        gain
        + player["Rank"] / 100
    )

    recommendations.append(
        {
            "Sell":
                player["Player"],
            "Buy":
                f"{replacement['First_Name']} "
                f"{replacement['Last_Name']}",
            "Gain":
                round(gain, 2),
            "Priority":
                round(priority, 2)
        }
    )

transfers = pd.DataFrame(
    recommendations
)

transfers = transfers.sort_values(
    "Priority",
    ascending=False
)

best_transfer = transfers.iloc[0]

# =====================================
# PROBLEM PLAYERS
# =====================================

weak_players = (
    team
    .sort_values(
        "Projected_Points"
    )
    .head(3)
)

# =====================================
# DASHBOARD
# =====================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Health Score",
    f"{health_score}/100"
)

col2.metric(
    "Projected Team Score",
    f"{team['Projected_Points'].sum():.2f}"
)

col3.metric(
    "Average Rank",
    f"{avg_rank:.1f}"
)

# =====================================
# WEEKLY SUMMARY
# =====================================

st.subheader("📋 Weekly Summary")

st.success(
    f"👑 Captain: "
    f"{captain['First_Name']} "
    f"{captain['Last_Name']} "
    f"({captain['Projected_Points']:.2f} pts)"
)

st.info(
    f"🛡 Vice-Captain: "
    f"{vice['First_Name']} "
    f"{vice['Last_Name']} "
    f"({vice['Projected_Points']:.2f} pts)"
)

st.warning(
    f"🎯 Recommended Transfer: "
    f"{best_transfer['Sell']} → "
    f"{best_transfer['Buy']} "
    f"(+{best_transfer['Gain']:.2f} pts)"
)

# =====================================
# TEAM STATUS
# =====================================

st.subheader("❤️ Team Health")

st.write(
    f"Current Status: {health_status}"
)

# =====================================
# WEAK PLAYERS
# =====================================

st.subheader("🚨 Weakest Assets")

for _, player in weak_players.iterrows():

    st.write(
        f"• {player['Player']} "
        f"({player['Projected_Points']:.2f} pts)"
    )

# =====================================
# ACTION PLAN
# =====================================

st.subheader("✅ Suggested Actions")

st.markdown(
    f"""
### This Week

1. Consider transferring **{best_transfer['Sell']}**
2. Target **{best_transfer['Buy']}**
3. Captain **{captain['First_Name']} {captain['Last_Name']}**
4. Review Fixture Runs page before deadline
5. Confirm Team Sheet before lockout

### Forecast

Projected Team Score:
**{team['Projected_Points'].sum():.2f}**
"""
)

# =====================================
# TOP PLAYERS
# =====================================

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

# =====================================
# FINAL VERDICT
# =====================================

st.subheader("🤖 Assistant Verdict")

if best_transfer["Gain"] >= 5:

    st.success(
        "Recommendation: Make a transfer this week."
    )

elif best_transfer["Gain"] >= 2:

    st.warning(
        "Recommendation: Transfer optional."
    )

else:

    st.info(
        "Recommendation: Roll the transfer."
    )
    