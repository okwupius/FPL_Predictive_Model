import pandas as pd

fixtures = pd.read_csv(
    "data/processed/fixtures.csv"
)

# Only completed fixtures

completed = fixtures[
    fixtures["finished"] == True
]

team_strength = {}

for team in range(1, 21):

    home_games = completed[
        completed["team_h"] == team
    ]

    away_games = completed[
        completed["team_a"] == team
    ]

    goals_scored = (
        home_games["team_h_score"].sum()
        +
        away_games["team_a_score"].sum()
    )

    games = (
        len(home_games)
        +
        len(away_games)
    )

    if games > 0:

        strength = goals_scored / games

        team_strength[team] = strength

strength_df = pd.DataFrame({
    "Team": team_strength.keys(),
    "Attack_Strength": team_strength.values()
})

strength_df = strength_df.sort_values(
    "Attack_Strength",
    ascending=False
)

print(strength_df)