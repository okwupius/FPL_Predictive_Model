# src/check_bootstrap_ids.py

import requests
import pandas as pd

data = requests.get(
    "https://fantasy.premierleague.com/api/bootstrap-static/"
).json()

elements = pd.DataFrame(
    data["elements"]
)

print(
    elements[
        [
            "id",
            "first_name",
            "second_name",
            "minutes",
            "total_points"
        ]
    ].tail(20)
)