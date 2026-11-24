import pandas as pd

fixtures = pd.read_csv(
    "data/processed/fixtures.csv"
)

print(
    fixtures[
        [
            "event",
            "team_h",
            "team_a",
            "team_h_difficulty",
            "team_a_difficulty"
        ]
    ].head(20)
)