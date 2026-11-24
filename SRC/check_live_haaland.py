# src/check_live_haaland.py

import requests
import pandas as pd

data = requests.get(
    "https://fantasy.premierleague.com/api/bootstrap-static/"
).json()

elements = pd.DataFrame(
    data["elements"]
)

haaland = elements[
    elements["second_name"]
    .str.contains(
        "Haaland",
        case=False,
        na=False
    )
]

print(
    haaland[
        [
            "id",
            "first_name",
            "second_name",
            "minutes",
            "total_points"
        ]
    ]
)
