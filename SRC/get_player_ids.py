import pandas as pd

players = pd.read_csv("data/Raw/fpl_players.csv")

players.reset_index(inplace=True)

players["Player_ID"] = players.index + 1

print(
    players[
        [
            "Player_ID",
            "First_Name",
            "Last_Name"
        ]
    ].head(20)
)
