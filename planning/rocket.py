# Rocket planning problem from GraphPlan paper.

from graphplan import *

# Types
ROCKET = 'Rocket'
PLACE = 'Place'
CARGO = 'Cargo'

# Instances
i_rocket1 = Instance('rocket1', ROCKET)
i_london = Instance('london', PLACE)
i_paris = Instance('paris', PLACE)
i_pkgA = Instance('pkgA', CARGO)
i_pkgB = Instance('pkgB', CARGO)

# Variables
v_r = Variable('r', ROCKET)
v_from = Variable('from', PLACE)
v_to = Variable('to', PLACE)
v_place = Variable('place', PLACE)
v_c = Variable('c', CARGO)

# Operators

o_move = Operator('move',
    # Preconditions
    [Proposition('not_equal', v_from, v_to),
     Proposition('at', v_r, v_from),
     Proposition('has_fuel', v_r)],
    # Adds
    [Proposition('at', v_r, v_to)],
    # Deletes
    [Proposition('at', v_r, v_from),
     Proposition('has_fuel', v_r)])

o_unload = Operator('unload',
    # Preconditions
    [Proposition('at', v_r, v_place),
     Proposition('in', v_c, v_r)],
    # Adds
    [Proposition('at', v_c, v_place)],
    # Deletes
    [Proposition('in', v_c, v_r)])

o_load = Operator('load',
    # Preconditions
    [Proposition('at', v_r, v_place),
     Proposition('at', v_c, v_place)],
    # Adds
    [Proposition('in', v_c, v_r)],
    # Deletes
    [Proposition('at', v_c, v_place)])

prob1 = PlanningProblem('prob1',
    # Instances
    [i_rocket1, i_london, i_paris, i_pkgA, i_pkgB],
    # Operators
    [o_move, o_unload, o_load],
    # Initial state
    [Proposition('at', i_pkgA, i_london),
     Proposition('at', i_pkgB, i_london),
     Proposition('at', i_rocket1, i_london),
     Proposition('has_fuel', i_rocket1)],
    # Goals
    [Proposition('at', i_pkgA, i_paris),
     Proposition('at', i_pkgB, i_paris)])

prob1.solve()
prob1.display()

print
prob1.dump()
