import pandas as pd

fixtures = pd.read_csv(
    "data/processed/fixtures.csv"
)

future = fixtures[
    fixtures["finished"] == False
].copy()

rows = []

for team in range(1, 21):

    team_games = future[
        (future["team_h"] == team)
        |
        (future["team_a"] == team)
    ]

    team_games = (
        team_games
        .sort_values("event")
        .head(5)
    )

    gw_number = 1

    for _, game in team_games.iterrows():

        if game["team_h"] == team:

            rows.append({
                "Team": team,
                "GW": gw_number,
                "Opponent": game["team_a"],
                "Difficulty": game["team_h_difficulty"],
                "Home": 1
            })

        else:

            rows.append({
                "Team": team,
                "GW": gw_number,
                "Opponent": game["team_h"],
                "Difficulty": game["team_a_difficulty"],
                "Home": 0
            })

        gw_number += 1

fixture_runs = pd.DataFrame(rows)

fixture_runs.to_csv(
    "data/processed/fixture_runs.csv",
    index=False
)

print(fixture_runs.head(20))