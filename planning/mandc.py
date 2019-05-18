from graphplan import *

# Types
PLACE = 'Place'
BOAT = 'Boat'

# Instances
i_boat1 = Instance('boat1', BOAT)
i_start = Instance('start', PLACE)
i_dest = Instance('dest', PLACE)
i_0 = Instance(0, INT)
i_1 = Instance(1, INT)
i_2 = Instance(2, INT)
i_3 = Instance(3, INT)

# Variables
v_b = Variable('boat', BOAT)
v_start_c = Variable('start_c', INT) # num of cannibals at starting bank
v_dest_c = Variable('dest_c', INT) # num of cannibals at dest bank
v_start_m = Variable('start_m', INT)
v_dest_m = Variable('dest_m', INT)
v_move_c = Variable('move_c', INT) # num of cannibals to move
v_move_m = Variable('move_m', INT) # num of missionaries to move

# num of cannibals after move at start bank
v_start_new_c = Variable('start_new_c', INT)
# num of cannibals after move at dest bank
v_dest_new_c = Variable('dest_new_c', INT)
v_start_new_m = Variable('start_new_m', INT)
v_dest_new_m = Variable('dest_new_m', INT)

# Operators
# Assume that left is starting place, and right is destination
# Number in middle shows how many person to move
# a: both bank has some m (after move)
# b: starting bank has no m
# c: desting bank has no m
# Move one person to dest
o_move_right_1_a = Operator(
    'move_right_1_a',
    # Preconditions
    [Proposition('at', v_b, i_start),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m),
     Proposition(SUM, v_move_c, v_move_m, i_1),
     Proposition(SUM, v_start_new_c, v_move_c, v_start_c),
     Proposition(SUM, v_start_new_m, v_move_m, v_start_m),
     Proposition(LESS_EQUAL, v_start_new_c, v_start_new_m),
     Proposition(SUM, v_move_c, v_dest_c, v_dest_new_c),
     Proposition(SUM, v_move_m, v_dest_m, v_dest_new_m),
     Proposition(LESS_EQUAL, v_dest_new_c, v_dest_new_m),
     Proposition(SUM, v_start_new_c, v_dest_new_c, i_3),
     Proposition(SUM, v_start_new_m, v_dest_new_m, i_3)],
    # Adds
    [Proposition('at', v_b, i_dest),
     Proposition('v_start_c', v_start_new_c),
     Proposition('v_dest_c', v_dest_new_c),
     Proposition('v_start_m', v_start_new_m),
     Proposition('v_dest_m', v_dest_new_m)],
    # Deletes
    [Proposition('at', v_b, i_start),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m)])

o_move_right_1_b = Operator(
    'move_right_1_b',
    # Preconditions
    [Proposition('at', v_b, i_start),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m),
     Proposition(SUM, v_move_c, v_move_m, i_1),
     Proposition(SUM, v_start_new_c, v_move_c, v_start_c),
     Proposition(SUM, v_start_new_m, v_move_m, v_start_m),
     Proposition(EQUAL, v_start_new_m, i_0),
     Proposition(SUM, v_move_c, v_dest_c, v_dest_new_c),
     Proposition(SUM, v_move_m, v_dest_m, v_dest_new_m),
     Proposition(LESS_EQUAL, v_dest_new_c, v_dest_new_m),
     Proposition(SUM, v_start_new_c, v_dest_new_c, i_3),
     Proposition(SUM, v_start_new_m, v_dest_new_m, i_3)],
    # Adds
    [Proposition('at', v_b, i_dest),
     Proposition('v_start_c', v_start_new_c),
     Proposition('v_dest_c', v_dest_new_c),
     Proposition('v_start_m', v_start_new_m),
     Proposition('v_dest_m', v_dest_new_m)],
    # Deletes
    [Proposition('at', v_b, i_start),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m)])

o_move_right_1_c = Operator(
    'move_right_1_c',
    # Preconditions
    [Proposition('at', v_b, i_start),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m),
     Proposition(SUM, v_move_c, v_move_m, i_1),
     Proposition(SUM, v_start_new_c, v_move_c, v_start_c),
     Proposition(SUM, v_start_new_m, v_move_m, v_start_m),
     Proposition(LESS_EQUAL, v_start_new_c, v_start_new_m),
     Proposition(SUM, v_move_c, v_dest_c, v_dest_new_c),
     Proposition(SUM, v_move_m, v_dest_m, v_dest_new_m),
     Proposition(EQUAL, v_dest_new_m, i_0),
     Proposition(SUM, v_start_new_c, v_dest_new_c, i_3),
     Proposition(SUM, v_start_new_m, v_dest_new_m, i_3)],
    # Adds
    [Proposition('at', v_b, i_dest),
     Proposition('v_start_c', v_start_new_c),
     Proposition('v_dest_c', v_dest_new_c),
     Proposition('v_start_m', v_start_new_m),
     Proposition('v_dest_m', v_dest_new_m)],
    # Deletes
    [Proposition('at', v_b, i_start),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m)])

o_move_left_1_a = Operator(
    'move_left_1_a',
    # Preconditions
    [Proposition('at', v_b, i_dest),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m),
     Proposition(SUM, v_move_c, v_move_m, i_1),
     Proposition(SUM, v_dest_new_c, v_move_c, v_dest_c),
     Proposition(SUM, v_dest_new_m, v_move_m, v_dest_m),
     Proposition(LESS_EQUAL, v_dest_new_c, v_dest_new_m),
     Proposition(SUM, v_move_c, v_start_c, v_start_new_c),
     Proposition(SUM, v_move_m, v_start_m, v_start_new_m),
     Proposition(LESS_EQUAL, v_start_new_c, v_start_new_m),
     Proposition(SUM, v_start_new_c, v_dest_new_c, i_3),
     Proposition(SUM, v_start_new_m, v_dest_new_m, i_3)],
    # Adds
    [Proposition('at', v_b, i_start),
     Proposition('v_start_c', v_start_new_c),
     Proposition('v_dest_c', v_dest_new_c),
     Proposition('v_start_m', v_start_new_m),
     Proposition('v_dest_m', v_dest_new_m)],
    # Deletes
    [Proposition('at', v_b, i_dest),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m)])

o_move_left_1_b = Operator(
    'move_left_1_b',
    # Preconditions
    [Proposition('at', v_b, i_dest),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m),
     Proposition(SUM, v_move_c, v_move_m, i_1),
     Proposition(SUM, v_dest_new_c, v_move_c, v_dest_c),
     Proposition(SUM, v_dest_new_m, v_move_m, v_dest_m),
     Proposition(EQUAL, v_dest_new_m, i_0),
     Proposition(SUM, v_move_c, v_start_c, v_start_new_c),
     Proposition(SUM, v_move_m, v_start_m, v_start_new_m),
     Proposition(LESS_EQUAL, v_start_new_c, v_start_new_m),
     Proposition(SUM, v_start_new_c, v_dest_new_c, i_3),
     Proposition(SUM, v_start_new_m, v_dest_new_m, i_3)],
    # Adds
    [Proposition('at', v_b, i_start),
     Proposition('v_start_c', v_start_new_c),
     Proposition('v_dest_c', v_dest_new_c),
     Proposition('v_start_m', v_start_new_m),
     Proposition('v_dest_m', v_dest_new_m)],
    # Deletes
    [Proposition('at', v_b, i_dest),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m)])

o_move_left_1_c = Operator(
    'move_left_1_c',
    # Preconditions
    [Proposition('at', v_b, i_dest),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m),
     Proposition(SUM, v_move_c, v_move_m, i_1),
     Proposition(SUM, v_dest_new_c, v_move_c, v_dest_c),
     Proposition(SUM, v_dest_new_m, v_move_m, v_dest_m),
     Proposition(LESS_EQUAL, v_dest_new_c, v_dest_new_m),
     Proposition(SUM, v_move_c, v_start_c, v_start_new_c),
     Proposition(SUM, v_move_m, v_start_m, v_start_new_m),
     Proposition(EQUAL, i_0, v_start_new_m),
     Proposition(SUM, v_start_new_c, v_dest_new_c, i_3),
     Proposition(SUM, v_start_new_m, v_dest_new_m, i_3)],
    # Adds
    [Proposition('at', v_b, i_start),
     Proposition('v_start_c', v_start_new_c),
     Proposition('v_dest_c', v_dest_new_c),
     Proposition('v_start_m', v_start_new_m),
     Proposition('v_dest_m', v_dest_new_m)],
    # Deletes
    [Proposition('at', v_b, i_dest),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m)])

o_move_right_2_a = Operator(
    'move_right_2_a',
    # Preconditions
    [Proposition('at', v_b, i_start),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m),
     Proposition(SUM, v_move_c, v_move_m, i_2),
     Proposition(SUM, v_start_new_c, v_move_c, v_start_c),
     Proposition(SUM, v_start_new_m, v_move_m, v_start_m),
     Proposition(LESS_EQUAL, v_start_new_c, v_start_new_m),
     Proposition(SUM, v_move_c, v_dest_c, v_dest_new_c),
     Proposition(SUM, v_move_m, v_dest_m, v_dest_new_m),
     Proposition(LESS_EQUAL, v_dest_new_c, v_dest_new_m),
     Proposition(SUM, v_start_new_c, v_dest_new_c, i_3),
     Proposition(SUM, v_start_new_m, v_dest_new_m, i_3)],
    # Adds
    [Proposition('at', v_b, i_dest),
     Proposition('v_start_c', v_start_new_c),
     Proposition('v_dest_c', v_dest_new_c),
     Proposition('v_start_m', v_start_new_m),
     Proposition('v_dest_m', v_dest_new_m)],
    # Deletes
    [Proposition('at', v_b, i_start),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m)])

o_move_right_2_b = Operator(
    'move_right_2_b',
    # Preconditions
    [Proposition('at', v_b, i_start),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m),
     Proposition(SUM, v_move_c, v_move_m, i_2),
     Proposition(SUM, v_start_new_c, v_move_c, v_start_c),
     Proposition(SUM, v_start_new_m, v_move_m, v_start_m),
     Proposition(EQUAL, i_0, v_start_new_m),
     Proposition(SUM, v_move_c, v_dest_c, v_dest_new_c),
     Proposition(SUM, v_move_m, v_dest_m, v_dest_new_m),
     Proposition(LESS_EQUAL, v_dest_new_c, v_dest_new_m),
     Proposition(SUM, v_start_new_c, v_dest_new_c, i_3),
     Proposition(SUM, v_start_new_m, v_dest_new_m, i_3)],
    # Adds
    [Proposition('at', v_b, i_dest),
     Proposition('v_start_c', v_start_new_c),
     Proposition('v_dest_c', v_dest_new_c),
     Proposition('v_start_m', v_start_new_m),
     Proposition('v_dest_m', v_dest_new_m)],
    # Deletes
    [Proposition('at', v_b, i_start),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m)])

o_move_right_2_c = Operator(
    'move_right_2_c',
    # Preconditions
    [Proposition('at', v_b, i_start),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m),
     Proposition(SUM, v_move_c, v_move_m, i_2),
     Proposition(SUM, v_start_new_c, v_move_c, v_start_c),
     Proposition(SUM, v_start_new_m, v_move_m, v_start_m),
     Proposition(LESS_EQUAL, v_start_new_c, v_start_new_m),
     Proposition(SUM, v_move_c, v_dest_c, v_dest_new_c),
     Proposition(SUM, v_move_m, v_dest_m, v_dest_new_m),
     Proposition(EQUAL, i_0, v_dest_new_m),
     Proposition(SUM, v_start_new_c, v_dest_new_c, i_3),
     Proposition(SUM, v_start_new_m, v_dest_new_m, i_3)],
    # Adds
    [Proposition('at', v_b, i_dest),
     Proposition('v_start_c', v_start_new_c),
     Proposition('v_dest_c', v_dest_new_c),
     Proposition('v_start_m', v_start_new_m),
     Proposition('v_dest_m', v_dest_new_m)],
    # Deletes
    [Proposition('at', v_b, i_start),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m)])

o_move_left_2_a = Operator(
    'move_left_2_a',
    # Preconditions
    [Proposition('at', v_b, i_dest),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m),
     Proposition(SUM, v_move_c, v_move_m, i_2),
     Proposition(SUM, v_dest_new_c, v_move_c, v_dest_c),
     Proposition(SUM, v_dest_new_m, v_move_m, v_dest_m),
     Proposition(LESS_EQUAL, v_dest_new_c, v_dest_new_m),
     Proposition(SUM, v_move_c, v_start_c, v_start_new_c),
     Proposition(SUM, v_move_m, v_start_m, v_start_new_m),
     Proposition(LESS_EQUAL, v_start_new_c, v_start_new_m),
     Proposition(SUM, v_start_new_c, v_dest_new_c, i_3),
     Proposition(SUM, v_start_new_m, v_dest_new_m, i_3)],
    # Adds
    [Proposition('at', v_b, i_start),
     Proposition('v_start_c', v_start_new_c),
     Proposition('v_dest_c', v_dest_new_c),
     Proposition('v_start_m', v_start_new_m),
     Proposition('v_dest_m', v_dest_new_m)],
    # Deletes
    [Proposition('at', v_b, i_dest),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m)])

o_move_left_2_b = Operator(
    'move_left_2_b',
    # Preconditions
    [Proposition('at', v_b, i_dest),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m),
     Proposition(SUM, v_move_c, v_move_m, i_2),
     Proposition(SUM, v_dest_new_c, v_move_c, v_dest_c),
     Proposition(SUM, v_dest_new_m, v_move_m, v_dest_m),
     Proposition(EQUAL, i_0, v_dest_new_m),
     Proposition(SUM, v_move_c, v_start_c, v_start_new_c),
     Proposition(SUM, v_move_m, v_start_m, v_start_new_m),
     Proposition(LESS_EQUAL, v_start_new_c, v_start_new_m),
     Proposition(SUM, v_start_new_c, v_dest_new_c, i_3),
     Proposition(SUM, v_start_new_m, v_dest_new_m, i_3)],
    # Adds
    [Proposition('at', v_b, i_start),
     Proposition('v_start_c', v_start_new_c),
     Proposition('v_dest_c', v_dest_new_c),
     Proposition('v_start_m', v_start_new_m),
     Proposition('v_dest_m', v_dest_new_m)],
    # Deletes
    [Proposition('at', v_b, i_dest),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m)])

o_move_left_2_c = Operator(
    'move_left_2_c',
    # Preconditions
    [Proposition('at', v_b, i_dest),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m),
     Proposition(SUM, v_move_c, v_move_m, i_2),
     Proposition(SUM, v_dest_new_c, v_move_c, v_dest_c),
     Proposition(SUM, v_dest_new_m, v_move_m, v_dest_m),
     Proposition(LESS_EQUAL, v_dest_new_c, v_dest_new_m),
     Proposition(SUM, v_move_c, v_start_c, v_start_new_c),
     Proposition(SUM, v_move_m, v_start_m, v_start_new_m),
     Proposition(EQUAL, i_0, v_start_new_m),
     Proposition(SUM, v_start_new_c, v_dest_new_c, i_3),
     Proposition(SUM, v_start_new_m, v_dest_new_m, i_3)],
    # Adds
    [Proposition('at', v_b, i_start),
     Proposition('v_start_c', v_start_new_c),
     Proposition('v_dest_c', v_dest_new_c),
     Proposition('v_start_m', v_start_new_m),
     Proposition('v_dest_m', v_dest_new_m)],
    # Deletes
    [Proposition('at', v_b, i_dest),
     Proposition('v_start_c', v_start_c),
     Proposition('v_dest_c', v_dest_c),
     Proposition('v_start_m', v_start_m),
     Proposition('v_dest_m', v_dest_m)])

problem = PlanningProblem(
    'missionaries_and_cannibals',
    # Instances
    [i_boat1, i_start, i_dest, i_0, i_1, i_2, i_3],
    # Operators
    [o_move_left_1_a, o_move_left_1_b, o_move_left_1_c, 
     o_move_left_2_a, o_move_left_2_b, o_move_left_2_c,
     o_move_right_1_a, o_move_right_1_b, o_move_right_1_c,
     o_move_right_2_a, o_move_right_2_b, o_move_right_2_c],
    # Initial State
    [Proposition('at', i_boat1, i_start),
     Proposition('v_start_c', i_3),
     Proposition('v_start_m', i_3),
     Proposition('v_dest_c', i_0),
     Proposition('v_dest_m', i_0)],
    # Goal State
    [Proposition('v_dest_c', i_3),
     Proposition('v_dest_m', i_3)]
)

problem.solve()
problem.display()
#problem.dump()