import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Team Sheet",
    layout="wide"
)

st.title("⚽ Team Sheet")

# =====================================
# LOAD DATA
# =====================================

my_team = pd.read_csv(
    "data/my_team.csv"
)

rankings = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

forecast = pd.read_csv(
    "data/processed/forecast_v11.csv"
)

team = my_team.merge(
    rankings,
    on=["First_Name", "Last_Name"],
    how="left"
)

# Add fixture data if available

if "player_id" in team.columns:

    team = team.merge(
        forecast[
            [
                "player_id",
                "Fixture_Difficulty"
            ]
        ],
        on="player_id",
        how="left"
    )

# =====================================
# FIND BEST XI
# =====================================

formations = [
    (3,4,3),
    (3,5,2),
    (4,4,2),
    (4,3,3),
    (4,5,1),
    (5,3,2),
    (5,4,1)
]

best_points = -999
best_xi = None
best_formation = None

gk = team[team["Position"] == 1].sort_values(
    "Projected_Points",
    ascending=False
)

defs = team[team["Position"] == 2].sort_values(
    "Projected_Points",
    ascending=False
)

mids = team[team["Position"] == 3].sort_values(
    "Projected_Points",
    ascending=False
)

fwds = team[team["Position"] == 4].sort_values(
    "Projected_Points",
    ascending=False
)

for d, m, f in formations:

    if (
        len(defs) < d
        or len(mids) < m
        or len(fwds) < f
    ):
        continue

    xi = pd.concat(
        [
            gk.head(1),
            defs.head(d),
            mids.head(m),
            fwds.head(f)
        ]
    )

    points = xi["Projected_Points"].sum()

    if points > best_points:

        best_points = points
        best_xi = xi.copy()
        best_formation = (d, m, f)

# =====================================
# CAPTAINS
# =====================================

captain = (
    best_xi
    .sort_values(
        "Projected_Points",
        ascending=False
    )
    .iloc[0]
)

vice = (
    best_xi
    .sort_values(
        "Projected_Points",
        ascending=False
    )
    .iloc[1]
)

# =====================================
# BENCH
# =====================================

bench = team[
    ~team.index.isin(best_xi.index)
].sort_values(
    "Projected_Points",
    ascending=False
)

# =====================================
# POSITION GROUPS
# =====================================

gk = best_xi[
    best_xi["Position"] == 1
]

defs = best_xi[
    best_xi["Position"] == 2
]

mids = best_xi[
    best_xi["Position"] == 3
]

fwds = best_xi[
    best_xi["Position"] == 4
]

# =====================================
# PITCH
# =====================================

fig = go.Figure()

fig.update_layout(
    plot_bgcolor="#0B6E0B",
    paper_bgcolor="#0B6E0B",
    height=850,
    xaxis=dict(
        visible=False,
        range=[0,100]
    ),
    yaxis=dict(
        visible=False,
        range=[0,100]
    ),
    margin=dict(
        l=10,
        r=10,
        t=10,
        b=10
    )
)

# OUTER PITCH

fig.add_shape(
    type="rect",
    x0=5,
    y0=5,
    x1=95,
    y1=95,
    line=dict(
        color="white",
        width=3
    )
)

# HALFWAY LINE

fig.add_shape(
    type="line",
    x0=5,
    y0=50,
    x1=95,
    y1=50,
    line=dict(
        color="white",
        width=2
    )
)

# CENTRE CIRCLE

fig.add_shape(
    type="circle",
    x0=40,
    y0=40,
    x1=60,
    y1=60,
    line=dict(
        color="white",
        width=2
    )
)

# =====================================
# PLAYER PLOTTING
# =====================================

def plot_line(players, y_value):

    count = len(players)

    if count == 1:
        xs = [50]

    elif count == 2:
        xs = [35,65]

    elif count == 3:
        xs = [25,50,75]

    elif count == 4:
        xs = [15,38,62,85]

    elif count == 5:
        xs = [10,30,50,70,90]

    else:
        xs = []

    for x, (_, player) in zip(xs, players.iterrows()):

        short_name = player["Last_Name"]

        marker_color = "Red"

        if (
            player["First_Name"] == captain["First_Name"]
            and
            player["Last_Name"] == captain["Last_Name"]
        ):
            short_name += " (C)"
            marker_color = "gold"

        elif (
            player["First_Name"] == vice["First_Name"]
            and
            player["Last_Name"] == vice["Last_Name"]
        ):
            short_name += " (VC)"
            marker_color = "silver"

        fixture_text = ""

        if "Fixture_Difficulty" in player.index:
            fixture_text = (
                f"<br>FDR "
                f"{player['Fixture_Difficulty']}"
            )

        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y_value],
                mode="markers+text",

                marker=dict(
                    size=42,
                    color=marker_color,
                    line=dict(
                        color="black",
                        width=2
                    )
                ),

                text=[
                    f"{short_name}"
                    f"<br>{player['Projected_Points']:.1f}"
                    f"{fixture_text}"
                ],

                textfont=dict(
                    color="white",
                    size=13
                ),

                textposition="bottom center",

                hovertext=(
                    f"{player['First_Name']} "
                    f"{player['Last_Name']}"
                ),

                hoverinfo="text",

                showlegend=False
            )
        )

# =====================================
# FORMATION LINES
# =====================================

plot_line(gk, 10)
plot_line(defs, 30)
plot_line(mids, 55)
plot_line(fwds, 78)

# =====================================
# SUMMARY
# =====================================

c1, c2, c3 = st.columns(3)

c1.metric(
    "Formation",
    f"{best_formation[0]}-"
    f"{best_formation[1]}-"
    f"{best_formation[2]}"
)

c2.metric(
    "Projected Points",
    f"{best_points:.2f}"
)

c3.metric(
    "Captain",
    captain["Last_Name"]
)

# =====================================
# DISPLAY PITCH
# =====================================

st.plotly_chart(
    fig,
    width="stretch"
)

# =====================================
# BENCH
# =====================================

st.subheader("🪑 Bench")

st.dataframe(
    bench[
        [
            "First_Name",
            "Last_Name",
            "Projected_Points"
        ]
    ],
    width="stretch",
    hide_index=True
)