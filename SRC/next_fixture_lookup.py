import pandas as pd

fixtures = pd.read_csv(
    "data/processed/fixtures.csv"
)

future = fixtures[
    fixtures["finished"] == False
].copy()

next_fixtures = []

for team in range(1, 21):

    team_games = future[
        (future["team_h"] == team)
        |
        (future["team_a"] == team)
    ]

    if len(team_games) == 0:
        continue

    next_game = (
        team_games
        .sort_values("event")
        .iloc[0]
    )

    if next_game["team_h"] == team:

        next_fixtures.append({
            "Team": team,
            "Home_Game": 1,
            "Opponent": next_game["team_a"],
            "Fixture_Difficulty":
                next_game["team_h_difficulty"]
        })

    else:

        next_fixtures.append({
            "Team": team,
            "Home_Game": 0,
            "Opponent": next_game["team_h"],
            "Fixture_Difficulty":
                next_game["team_a_difficulty"]
        })

next_fixtures = pd.DataFrame(
    next_fixtures
)

next_fixtures.to_csv(
    "data/processed/next_fixtures.csv",
    index=False
)

print(next_fixtures)
