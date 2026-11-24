import pandas as pd

hist = pd.read_csv(
    "data/processed/all_player_history.csv"
)

mapping = pd.read_csv(
    "data/processed/player_mapping.csv"
)

print("\nHaaland mapping\n")

print(
    mapping[
        mapping["Last_Name"] == "Haaland"
    ]
)

print("\nHistory rows for element 494\n")

print(
    hist[
        hist["player_id"] == 494
    ][
        [
            "player_id",
            "element",
            "round",
            "minutes",
            "total_points"
        ]
    ]
)
