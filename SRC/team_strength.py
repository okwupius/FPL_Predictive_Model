import pandas as pd

fixtures = pd.read_csv(
    "data/processed/fixtures.csv"
)

completed = fixtures[
    fixtures["finished"] == True
]

strength_data = []

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

    goals_conceded = (
        home_games["team_a_score"].sum()
        +
        away_games["team_h_score"].sum()
    )

    games = len(home_games) + len(away_games)

    if games > 0:

        attack_strength = (
            goals_scored / games
        )

        defence_strength = (
            goals_conceded / games
        )

        strength_data.append(
            [
                team,
                attack_strength,
                defence_strength
            ]
        )

strength_df = pd.DataFrame(
    strength_data,
    columns=[
        "Team",
        "Attack_Strength",
        "Defence_Strength"
    ]
)

strength_df.to_csv(
    "data/processed/team_strength.csv",
    index=False
)

print(strength_df.sort_values(
    "Attack_Strength",
    ascending=False
))