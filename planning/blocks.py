# Blocks world planning problem
# Translation from Dave Touretzky's Ruby implementation blocks.rb
# Jonathan Li, October 2018

from graphplan import *

# Types
BLOCK = 'Block'

# Instances
i_A = Instance('A', BLOCK)
i_B = Instance('B', BLOCK)
i_C = Instance('C', BLOCK)
i_D = Instance('D', BLOCK)

# Variables
v_obj = Variable('obj', BLOCK)
v_from = Variable('from', BLOCK)
v_to = Variable('to', BLOCK)

o_move = Operator('move',
    # Preconditions
    [Proposition('not_equal', v_obj, v_from),
     Proposition('not_equal', v_obj, v_to),
     Proposition('not_equal', v_from, v_to),
     Proposition('on', v_obj, v_from),
     Proposition('clear', v_obj),
     Proposition('clear', v_to)],
    # Adds
    [Proposition('on', v_obj, v_to),
     Proposition('clear', v_from)],
    # Deletes
    [Proposition('on', v_obj, v_from),
     Proposition('clear', v_to)])

o_move_to_table = Operator('move_to_table',
    # Preconditions
    [Proposition('not_equal', v_obj, v_from),
     Proposition('on', v_obj, v_from),
     Proposition('clear', v_obj)],
    # Adds
    [Proposition('on_table', v_obj),
     Proposition('clear', v_from)],
    # Deletes
    [Proposition('on', v_obj, v_from)])

o_move_from_table = Operator('move_from_table',
    # Preconditions
    [Proposition('not_equal', v_obj, v_to),
     Proposition('on_table', v_obj),
     Proposition('clear', v_obj),
     Proposition('clear', v_to)],
    # Adds
    [Proposition('on', v_obj, v_to)],
    # Deletes
    [Proposition('on_table', v_obj),
     Proposition('clear', v_to)])

prob1 = PlanningProblem('blocks_problem',
    # Instances
    [i_A, i_B, i_C],
    # Operators
    [o_move, o_move_to_table, o_move_from_table],
    # Initial state
    [Proposition('on', i_B, i_A),
     Proposition('on_table', i_A),
     Proposition('on_table', i_C),
     Proposition('clear', i_B),
     Proposition('clear', i_C)],
    # Goals
    [Proposition('on', i_A, i_B),
     Proposition('on', i_B, i_C)])

prob2 = PlanningProblem('blocks_problem2',
    # Instances
    [i_A, i_B, i_C],
    # Operators
    [o_move, o_move_to_table, o_move_from_table],
    # Initial state
    [Proposition('on', i_A, i_B),
     Proposition('on_table', i_B),
     Proposition('on_table', i_C),
     Proposition('clear', i_A),
     Proposition('clear', i_C)],
    # Goals
    [Proposition('on', i_A, i_B),
     Proposition('on', i_B, i_C)])

prob3 = PlanningProblem('blocks_problem2',
    # Instances
    [i_A, i_B, i_C, i_D],
    # Operators
    [o_move, o_move_to_table, o_move_from_table],
    # Initial state
    [Proposition('on', i_A, i_C),
     Proposition('on', i_C, i_B),
     Proposition('on', i_B, i_D),
     Proposition('on_table', i_D),
     Proposition('clear', i_A)],
    # Goals
    [Proposition('on', i_A, i_B),
     Proposition('on', i_B, i_C),
     Proposition('on', i_C, i_D)])

prob_unsolvable1 = PlanningProblem('blocks_problem',
    # Instances
    [i_A, i_B, i_C],
    # Operators
    [o_move, o_move_to_table, o_move_from_table],
    # Initial state
    [Proposition('on_table', i_A),
     Proposition('on_table', i_B),
     Proposition('on_table', i_C),
     Proposition('clear', i_A),
     Proposition('clear', i_B),
     Proposition('clear', i_C)],
    # Goals
    [Proposition('on', i_A, i_B),
     Proposition('on', i_B, i_C),
     Proposition('on', i_C, i_A)])

problem = prob3

problem.solve()
problem.display()
#problem.dump()
