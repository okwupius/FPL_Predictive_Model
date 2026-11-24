import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Fixture Runs",
    layout="wide"
)

st.title("🗓️ 5-Game Fixture Planner")

# ====================================
# LOAD DATA
# ====================================

my_team = pd.read_csv(
    "data/my_team.csv"
)

rankings = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

fixture_runs = pd.read_csv(
    "data/processed/fixture_runs.csv"
)

# ====================================
# MERGE TEAM
# ====================================

team = my_team.merge(
    rankings,
    on=["First_Name", "Last_Name"],
    how="left"
)

# ====================================
# DIFFICULTY ICONS
# ====================================

def fixture_icon(value):

    if value <= 2:
        return "🟢"

    elif value == 3:
        return "🟡"

    else:
        return "🔴"

# ====================================
# BUILD FIXTURE MATRIX
# ====================================

rows = []

for _, player in team.iterrows():

    team_id = player["Team"]

    fixtures = (
        fixture_runs[
            fixture_runs["Team"] == team_id
        ]
        .sort_values("GW")
    )

    row = {
        "Player":
            f"{player['First_Name']} "
            f"{player['Last_Name']}",
        "Projection":
            round(
                player["Projected_Points"],
                2
            )
    }

    for _, fixture in fixtures.iterrows():

        row[
            f"GW{int(fixture['GW'])}"
        ] = fixture_icon(
            fixture["Difficulty"]
        )

    rows.append(row)

heatmap = pd.DataFrame(rows)

# ====================================
# DISPLAY
# ====================================

st.subheader(
    "Next 5 Fixtures"
)

st.dataframe(
    heatmap,
    width="stretch",
    hide_index=True
)

# ====================================
# PLAYER LOOKUP
# ====================================

st.subheader(
    "Fixture Run Explorer"
)

player_name = st.selectbox(
    "Select Player",
    heatmap["Player"]
)

selected = heatmap[
    heatmap["Player"]
    == player_name
]

st.dataframe(
    selected,
    width="stretch",
    hide_index=True
)

# ====================================
# EASIEST RUNS
# ====================================

st.subheader(
    "Players With Best Fixture Runs"
)

def run_score(team_id):

    fixtures = fixture_runs[
        fixture_runs["Team"] == team_id
    ]

    return fixtures[
        "Difficulty"
    ].mean()

team["Run_Score"] = (
    team["Team"]
    .apply(run_score)
)

best_runs = (
    team.sort_values(
        "Run_Score"
    )
)

st.dataframe(
    best_runs[
        [
            "First_Name",
            "Last_Name",
            "Run_Score",
            "Projected_Points"
        ]
    ].head(10),
    width="stretch",
    hide_index=True
)

# ====================================
# HARDEST RUNS
# ====================================

st.subheader(
    "Players With Worst Fixture Runs"
)

st.dataframe(
    best_runs[
        [
            "First_Name",
            "Last_Name",
            "Run_Score",
            "Projected_Points"
        ]
    ].tail(10),
    width="stretch",
    hide_index=True
)
