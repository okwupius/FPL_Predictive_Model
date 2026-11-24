import pandas as pd
from datetime import datetime

df = pd.read_csv(
    "data/processed/final_rankings_v11.csv"
)

today = datetime.now().strftime(
    "%Y_%m_%d"
)

filename = (
    f"data/history/rankings_{today}.csv"
)

df.to_csv(
    filename,
    index=False
)

print(
    f"Snapshot saved:\n{filename}"
)