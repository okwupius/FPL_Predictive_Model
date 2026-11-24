import pandas as pd

df = pd.read_csv(
    "data/processed/model_v10_data.csv"
)

print(df.columns.tolist())

if "Total_Points" in df.columns:
    print("\nTOTAL POINTS EXISTS")
else:
    print("\nTOTAL POINTS MISSING")