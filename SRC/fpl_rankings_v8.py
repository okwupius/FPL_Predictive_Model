import pandas as pd

preds = pd.read_csv(
    "data/processed/v8_predictions.csv"
)

mapping = pd.read_csv(
    "data/processed/player_mapping.csv"
)

results = preds.merge(
    mapping,
    on="player_id",
    how="left"
)

results = results.rename(
    columns={
        "Price_x": "Price",
        "Position_x": "Position",
        "Team_x": "Team"
    }
)

results["Rank"] = range(
    1,
    len(results) + 1
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

positions = {
    1: "Goalkeepers",
    2: "Defenders",
    3: "Midfielders",
    4: "Forwards"
}

for pos_id, pos_name in positions.items():

    print(
        f"\nTOP {pos_name.upper()}\n"
    )

    filtered = (
        results[
            results["Position"] == pos_id
        ]
        .head(10)
    )

    print(
        filtered[
            [
                "Rank",
                "First_Name",
                "Last_Name",
                "Price",
                "Projected_Points"
            ]
        ]
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
    "data/processed/final_rankings_v8.csv",
    index=False
)
