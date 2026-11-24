import pandas as pd

players = pd.read_csv(
    "data/Raw/fpl_players.csv"
)

elite = players[
    players["Last_Name"].isin(
        ["Haaland", "Saka", "Isak", "Palmer"]
    )
]

print(
    elite[
        [
            "First_Name",
            "Last_Name",
            "Price",
            "Total_Points",
            "Form",
            "Ownership",
            "xG",
            "xA"
        ]
    ]
)