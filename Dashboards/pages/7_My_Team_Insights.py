import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="My Team Insights",
    layout="wide"
)

st.title("🧠 My Team Insights")

# ====================================
# LOAD DATA
# ====================================

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

# ====================================
# HEALTH SCORE
# ====================================

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
    status = "Excellent"
elif health_score >= 60:
    status = "Good"
elif health_score >= 40:
    status = "Average"
else:
    status = "Needs Attention"

col1, col2 = st.columns(2)

col1.metric(
    "Health Score",
    f"{health_score}/100"
)

col2.metric(
    "Team Status",
    status
)

# ====================================
# STRENGTHS
# ====================================

st.subheader("✅ Team Strengths")

strengths = (
    team.sort_values(
        "Projected_Points",
        ascending=False
    )
    .head(5)
)

st.dataframe(
    strengths[
        [
            "First_Name",
            "Last_Name",
            "Projected_Points",
            "Rank"
        ]
    ],
    width="stretch",
    hide_index=True
)

# ====================================
# WEAKNESSES
# ====================================

st.subheader("🚨 Team Weaknesses")

weaknesses = (
    team.sort_values(
        "Projected_Points"
    )
    .head(5)
)

st.dataframe(
    weaknesses[
        [
            "First_Name",
            "Last_Name",
            "Projected_Points",
            "Rank"
        ]
    ],
    width="stretch",
    hide_index=True
)

# ====================================
# POSITION ANALYSIS
# ====================================

st.subheader("📊 Position Analysis")

position_names = {
    1: "Goalkeepers",
    2: "Defenders",
    3: "Midfielders",
    4: "Forwards"
}

position_summary = (
    team.groupby("Position")
    .agg(
        Avg_Rank=("Rank", "mean"),
        Avg_Projection=(
            "Projected_Points",
            "mean"
        )
    )
    .reset_index()
)

position_summary["Position"] = (
    position_summary["Position"]
    .map(position_names)
)

st.dataframe(
    position_summary,
    width="stretch",
    hide_index=True
)

# ====================================
# RISK ALERTS
# ====================================

st.subheader("⚠ Risk Alerts")

alerts = []

for _, player in team.iterrows():

    if player["Rank"] > 200:

        alerts.append(
            {
                "Player":
                    f"{player['First_Name']} "
                    f"{player['Last_Name']}",
                "Issue":
                    "Ranked below 200"
            }
        )

    if player["Projected_Points"] < 2:

        alerts.append(
            {
                "Player":
                    f"{player['First_Name']} "
                    f"{player['Last_Name']}",
                "Issue":
                    "Projection below 2"
            }
        )

alerts_df = pd.DataFrame(alerts)

if len(alerts_df) > 0:

    st.dataframe(
        alerts_df,
        width="stretch",
        hide_index=True
    )

else:

    st.success(
        "No major risks detected."
    )

# ====================================
# RECOMMENDED ACTIONS
# ====================================

st.subheader("🎯 Recommended Actions")

owned = set(
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
            ) in owned,
            axis=1
        )
    ]

    replacements = replacements[
        replacements["Price"]
        <= player["Price"] + 1
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
                f"{player['First_Name']} "
                f"{player['Last_Name']}",
            "Buy":
                f"{replacement['First_Name']} "
                f"{replacement['Last_Name']}",
            "Gain":
                round(gain, 2),
            "Priority":
                round(priority, 2)
        }
    )

recommendations = (
    pd.DataFrame(
        recommendations
    )
    .sort_values(
        "Priority",
        ascending=False
    )
)

st.dataframe(
    recommendations.head(5),
    width="stretch",
    hide_index=True
)

# ====================================
# TEAM RATING VISUAL
# ====================================

st.subheader("📈 Projection Ranking")

chart = (
    team[
        [
            "First_Name",
            "Last_Name",
            "Projected_Points"
        ]
    ]
    .copy()
)

chart["Player"] = (
    chart["First_Name"]
    + " "
    + chart["Last_Name"]
)

chart = chart.set_index(
    "Player"
)

st.bar_chart(
    chart["Projected_Points"]
)