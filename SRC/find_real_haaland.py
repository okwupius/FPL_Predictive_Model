import pandas as pd

players = pd.read_csv(
    "data/Raw/fpl_players.csv"
)

print(
    players[
        players["Last_Name"]
        .str.contains(
            "Haaland",
            case=False,
            
            na=False
        )
    ]
)