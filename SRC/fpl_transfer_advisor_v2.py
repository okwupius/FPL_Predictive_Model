import pandas as pd

df = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

df["Points_Per_Million"] = (
    df["Projected_Points"] /
    df["Price"]
)

positions = {
    1: "GOALKEEPER",
    2: "DEFENDER",
    3: "MIDFIELDER",
    4: "FORWARD"
}

for pos_id, pos_name in positions.items():

    print(f"\n{pos_name} RECOMMENDATIONS\n")

    pos_df = df[
        df["Position"] == pos_id
    ]

    buy = (
        pos_df
        .sort_values(
            "Points_Per_Million",
            ascending=False
        )
        .head(3)
    )

    sell = (
        pos_df
        .sort_values(
            "Points_Per_Million",
            ascending=True
        )
        .head(3)
    )

    for i in range(
        min(len(buy), len(sell))
    ):

        sell_player = sell.iloc[i]
        buy_player = buy.iloc[i]

        gain = (
            buy_player["Projected_Points"]
            - sell_player["Projected_Points"]
        )

        print(
            f"\nOUT: "
            f"{sell_player['First_Name']} "
            f"{sell_player['Last_Name']}"
        )

        print(
            f" IN: "
            f"{buy_player['First_Name']} "
            f"{buy_player['Last_Name']}"
        )

        print(
            f"GAIN: +{gain:.2f} projected points"
        )
        