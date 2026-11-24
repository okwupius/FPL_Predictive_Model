import pandas as pd

preds = pd.read_csv(
    "data/processed/v10_predictions.csv"
)

mapping = pd.read_csv(
    "data/processed/player_mapping.csv"
)

mapping = mapping[
    [
        "player_id",
        "First_Name",
        "Last_Name"
    ]
]

results = preds.merge(
    mapping,
    on="player_id",
    how="left"
)

results = results.sort_values(
    "Projected_Points",
    ascending=False
)

results["Rank"] = range(
    1,
    len(results) + 1
)

print("\nTOP 30 PLAYERS\n")

print(
    results[
        [
            "Rank",
            "First_Name",
            "Last_Name",
            "Price",
            "Projected_Points"
        ]
    ].head(30)
)

elite = results[
    (
        (results["Last_Name"] == "Haaland")
        |
        (results["Last_Name"] == "Saka")
        |
        (results["Last_Name"] == "Isak")
        |
        (
            (results["First_Name"] == "Cole")
            &
            (results["Last_Name"] == "Palmer")
        )
    )
]

print("\nELITE PLAYER CHECK\n")

print(
    elite[
        [
            "Rank",
            "First_Name",
            "Last_Name",
            "Price",
            "Projected_Points"
        ]
    ]
)

results.to_csv(
    "data/processed/final_rankings_v10.csv",
    index=False
)