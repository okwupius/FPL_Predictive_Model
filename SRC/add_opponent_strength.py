import pandas as pd

df = pd.read_csv(
    "data/processed/model_v7_data.csv"
)

strength = pd.read_csv(
    "data/processed/team_strength.csv"
)

strength_attack = strength[
    ["Team", "Attack_Strength"]
].rename(
    columns={
        "Team": "opponent_team",
        "Attack_Strength": "Opponent_Attack_Strength"
    }
)

strength_defence = strength[
    ["Team", "Defence_Strength"]
].rename(
    columns={
        "Team": "opponent_team",
        "Defence_Strength": "Opponent_Defence_Strength"
    }
)

df = df.merge(
    strength_attack,
    on="opponent_team",
    how="left"
)

df = df.merge(
    strength_defence,
    on="opponent_team",
    how="left"
)

df.to_csv(
    "data/processed/model_v10_data.csv",
    index=False
)

print(df.shape)

print(
    df[
        [
            "Team_x",
            "opponent_team",
            "Opponent_Attack_Strength",
            "Opponent_Defence_Strength"
        ]
    ].head(20)
)
