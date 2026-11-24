from pulp import *

x = LpVariable(
    "x",
    lowBound=0,
    upBound=1,
    cat=LpBinary
)

print("SUCCESS")
