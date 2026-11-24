import pandas as pd

results = pd.read_csv(
    "data/processed/latest_predictions.csv"
)

captains = results.sort_values(
    "Predicted_Points",
    ascending=False
)

print("\nCAPTAINCY RANKINGS\n")

print(
    captains[
        [
            "First_Name",
            "Last_Name",
            "Predicted_Points"
        ]
    ].head(10)
)