import pandas as pd

predictions = pd.read_csv(
    "data/processed/latest_predictions.csv"
)

predictions["Transfer_Score"] = (
    predictions["Predicted_Points"]
    / predictions["Price"]
)

results = predictions.sort_values(
    "Transfer_Score",
    ascending=False
)

print("\nBEST TRANSFER TARGETS\n")

print(
    results[
        [
            "First_Name",
            "Last_Name",
            "Price",
            "Predicted_Points",
            "Transfer_Score"
        ]
    ].head(20)
)