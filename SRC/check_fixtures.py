import pandas as pd

fixtures = pd.read_csv(
    "data/processed/fixtures.csv"
)

print("\nCOLUMNS\n")

print(
    fixtures.columns.tolist()
)

print("\nFIRST 10 ROWS\n")

print(
    fixtures.head(10)
)
