from pulp import LpVariable
import inspect

print(
    inspect.signature(
        LpVariable.__init__
    )
)