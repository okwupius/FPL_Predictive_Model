import pandas as pd

# Load data
players = pd.read_csv("data/Raw/fpl_players.csv")

# Remove players with 0 minutes
players = players[players["Minutes"] > 0]

# Create value metric
players["Points_Per_Million"] = (
    players["Total_Points"] / players["Price"]
)

print("\nTOP 10 PLAYERS BY TOTAL POINTS")
print(
    players.sort_values(
        "Total_Points",
        ascending=False
    )[
        [
            "First_Name",
            "Last_Name",
            "Price",
            "Total_Points"
        ]
    ].head(10)
)

print("\nTOP 10 VALUE PLAYERS")
print(
    players.sort_values(
        "Points_Per_Million",
        ascending=False
    )[
        [
            "First_Name",
            "Last_Name",
            "Price",
            "Total_Points",
            "Points_Per_Million"
        ]
    ].head(10)
)