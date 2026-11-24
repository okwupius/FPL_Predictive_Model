import requests
import pandas as pd
import time

# Load player list

players = pd.read_csv(
    "data/Raw/fpl_players.csv"
)

all_history = []

for player_id in players["id"]:

    try:

        url = (
            f"https://fantasy.premierleague.com/api/"
            f"element-summary/{player_id}/"
        )

        data = requests.get(url).json()

        history = pd.DataFrame(
            data["history"]
        )

        if len(history) > 0:

            history["player_id"] = player_id

            all_history.append(history)

        print(
            f"Downloaded Player {player_id}"
        )

        time.sleep(0.25)

    except Exception as e:

        print(
            f"Failed Player {player_id}: {e}"
        )

master = pd.concat(
    all_history,
    ignore_index=True
)

master.to_csv(
    "data/processed/all_player_history.csv",
    index=False
)

print("\nDone!")
print(master.shape)
