import pandas as pd

df = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

df["Points_Per_Million"] = (
    df["Projected_Points"] /
    df["Price"]
)

positions = {
    1: "GOALKEEPERS",
    2: "DEFENDERS",
    3: "MIDFIELDERS",
    4: "FORWARDS"
}

for pos_id, pos_name in positions.items():

    print(f"\nTOP 15 {pos_name} BY VALUE\n")

    filtered = (
        df[
            df["Position"] == pos_id
        ]
        .sort_values(
            "Points_Per_Million",
            ascending=False
        )
        .head(15)
    )

    print(
        filtered[
            [
                "Rank",
                "First_Name",
                "Last_Name",
                "Price",
                "Projected_Points",
                "Points_Per_Million"
            ]
        ]
    )