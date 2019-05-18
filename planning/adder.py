from graphplan import *

# This is a simple planning problem that counts from 0 to 3 by adding
# 1 to a variable at each step.

# Types

# Instances
i_0 = Instance(0, INT)
i_1 = Instance(1, INT)
i_2 = Instance(2, INT)
i_3 = Instance(3, INT)

# Variables
v_old = Variable('old', INT)
v_new = Variable('new', INT)

# Operators
o_add1 = Operator('add1',
    # Preconditions
    [Proposition('got', v_old),
     Proposition(SUM, v_old, i_1, v_new)],
    # Adds
    [Proposition('got', v_new)],
    # Deletes
    [Proposition('got', v_old)]
)

# Problem
prob1 = PlanningProblem('add3x',
    # Instances
    [i_0, i_1, i_2, i_3],
    # Operators
    [o_add1],
    # Initial state
    [Proposition('got', i_0)],
    # Goal state
    [Proposition('got', i_3)]
)

prob1.solve()
print
prob1.dump()
prob1.display()
