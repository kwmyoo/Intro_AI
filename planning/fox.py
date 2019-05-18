from graphplan import *

# Types
BOAT = 'Boat'
PLACE = 'Place'

# Instances
i_fox = Instance(1, INT)
i_goose = Instance(5, INT)
i_bean = Instance(2, INT)
i_fox_goose = Instance(6, INT)
i_goose_bean = Instance(7, INT)
i_start = Instance('start', PLACE)
i_end = Instance('end', PLACE)
i_boat1 = Instance('boat1', BOAT)

# Variables
v_obj = Variable('o', INT)
v_obj1 = Variable('o1', INT)
v_obj2 = Variable('o2', INT)
v_obj3 = Variable('o3', INT)
v_b = Variable('b', BOAT)
v_place = Variable('place', PLACE)
v_from = Variable('from', PLACE)
v_to = Variable('to', PLACE)

# Operators
# Move boat with no items behind
o_move_0 = Operator(
    'move_0',
    # Preconditions
    [Proposition(NOT_EQUAL, v_from, v_to),
     Proposition(NOT_EQUAL, v_obj1, v_obj2),
     Proposition(NOT_EQUAL, v_obj2, v_obj3),
     Proposition(NOT_EQUAL, v_obj1, v_obj3),
     Proposition('at', v_b, v_from),
     Proposition('not_in', v_obj1, v_from),
     Proposition('not_in', v_obj2, v_from),
     Proposition('not_in', v_obj3, v_from)],
    # Adds
    [Proposition('at', v_b, v_to)],
    # Deletes
    [Proposition('at', v_b, v_from)]
)

# Move with one item behind
o_move_1 = Operator(
    'move_1',
    # Preconditions
    [Proposition(NOT_EQUAL, v_from, v_to),
     Proposition(NOT_EQUAL, v_obj2, v_obj3),
     Proposition('at', v_b, v_from),
     Proposition('in', v_obj1, v_from),
     Proposition('not_in', v_obj2, v_from),
     Proposition('not_in', v_obj3, v_from)],
    # Adds
    [Proposition('at', v_b, v_to)],
    # Deletes
    [Proposition('at', v_b, v_from)]
)

# Move with two items behind
o_move_2 = Operator(
    'move_2',
    # Preconditions
    [Proposition(NOT_EQUAL, v_from, v_to),
     Proposition(NOT_EQUAL, v_obj1, v_obj2),
     Proposition('at', v_b, v_from),
     Proposition('in', v_obj1, v_from),
     Proposition('in', v_obj2, v_from),
     Proposition('not_in', v_obj3, v_from),
     ~Proposition(SUM, v_obj1, v_obj2, i_fox_goose),
     ~Proposition(SUM, v_obj1, v_obj2, i_goose_bean)],
    # Adds
    [Proposition('at', v_b, v_to)],
    # Deletes
    [Proposition('at', v_b, v_from)]
)

o_load = Operator(
    'load',
    # Preconditions
    [Proposition('is_empty', v_b),
     Proposition('at', v_b, v_place),
     Proposition('in', v_obj, v_place)],
    # Adds
    [Proposition('is_loaded', v_b),
     Proposition('in', v_obj, v_b),
     Proposition('not_in', v_obj, v_place)],
    # Deletes
    [Proposition('is_empty', v_b),
     Proposition('in', v_obj, v_place)]
)

o_unload = Operator(
    'unload',
    # Preconditions
    [Proposition('is_loaded', v_b),
     Proposition('at', v_b, v_place),
     Proposition('in', v_obj, v_b)],
    # Adds
    [Proposition('is_empty', v_b),
     Proposition('in', v_obj, v_place)],
    # Deletes
    [Proposition('is_loaded', v_b),
     Proposition('in', v_obj, v_b),
     Proposition('not_in', v_obj, v_place)]
)

problem = PlanningProblem('fox_goose_and_beans',
    # Instances
    [i_fox, i_goose, i_bean, i_start, i_end, i_boat1,
     i_fox_goose, i_goose_bean],
    # Operators
    [o_move_0, o_move_1, o_move_2, o_load, o_unload],
    # Initial State
    [Proposition('in', i_fox, i_start),
     Proposition('in', i_goose, i_start),
     Proposition('in', i_bean, i_start),
     Proposition('at', i_boat1, i_start),
     Proposition('not_in', i_fox, i_end),
     Proposition('not_in', i_goose, i_end),
     Proposition('not_in', i_bean, i_end),
     Proposition('is_empty', i_boat1)],
     # Goals
     [Proposition('in', i_fox, i_end),
      Proposition('in', i_goose, i_end),
      Proposition('in', i_bean, i_end)]
    
    
    )

problem.solve()
problem.display()

