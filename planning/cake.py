# Have your cake and eat it too (bake another one).

from graphplan import *

# Types
CAKE = 'Cake'

# Instances
i_cake = Instance('cake', CAKE)

# Variables

# Operators

op_eat = Operator('eater',
    # Preconditions
    [Proposition('Have', i_cake)],
    # Adds
    [Proposition('Eaten', i_cake),
     ~Proposition('Have', i_cake)],
    # Deletes
    [Proposition('Have', i_cake)]
)

op_bake = Operator('baker',
    # Preconditions
    [~Proposition('Have', i_cake)],
    # Adds
    [Proposition('Have', i_cake)],
    # Deletes
    [~Proposition('Have', i_cake)]
)

prob1 = PlanningProblem('have_and_eat',
    # Instances
    [i_cake],
    # Operators
    [op_eat, op_bake],
    # Initial state
    [Proposition('Have', i_cake)],
    # Goals
    [Proposition('Have', i_cake),
     Proposition('Eaten', i_cake)]
)

prob1.solve()
prob1.dump()
print
prob1.display()
