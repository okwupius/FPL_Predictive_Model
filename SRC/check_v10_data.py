import pandas as pd

df = pd.read_csv(
    "data/processed/model_v10_data.csv"
)

print(df.columns.tolist())

print("\nNEW FEATURES\n")

print(
    df[
        [
            "Opponent_Attack_Strength",
            "Opponent_Defence_Strength"
        ]
    ].head(20)
)
