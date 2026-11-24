import pandas as pd

fixtures = pd.read_csv(
    "data/processed/fixtures.csv"
)

future = fixtures[
    fixtures["finished"] == False
]

print("\nFUTURE FIXTURES\n")

print(
    future[
        [
            "event",
            "team_h",
            "team_a",
            "team_h_difficulty",
            "team_a_difficulty"
        ]
    ].head(20)
)

print("\nTOTAL FUTURE FIXTURES:")

print(len(future))
