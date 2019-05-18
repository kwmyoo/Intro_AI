# Kun Woo Yoo, October 2018
# kunwooy@andrew.cmu.edu

from graphplan import *

# Types
ROD = 'Rod'

# Instances
i_small = Instance(1, INT)
i_med = Instance(2, INT)
i_large = Instance(3, INT)
i_rodA = Instance('A', INT)
i_rodB = Instance('B', INT)
i_rodC = Instance('C', INT)

# Variables
v_obj = Variable('obj', INT) # moved disk
v_obj_from = Variable('obj_from', INT) # disk under the obj on original rod
v_obj_to = Variable('obj_to', INT) # disk that will be under obj after moving
v_from = Variable('from', INT) # the rod where the disk is moved from
v_to = Variable('to', INT) # rod where disk will be moved to

o_move = Operator('move',
    # Preconditions
    [Proposition(LESS_THAN, v_obj, i_rodA),
     Proposition(NOT_EQUAL, v_from, v_to),
     Proposition('on_top', v_obj, v_from),
     Proposition('on_top', v_obj_to, v_to),
     Proposition('on_table', v_obj, v_from),
     Proposition('on_table', v_obj_from, v_from),
     Proposition('on_table', v_obj_to, v_to),
     Proposition('on', v_obj, v_obj_from),
     Proposition(LESS_THAN, v_obj, v_obj_to)],
    # Adds
    [Proposition('on_top', v_obj, v_to),
     Proposition('on_top', v_obj_from, v_from),
     Proposition('on_table', v_obj, v_to),
     Proposition('not_on', v_obj, v_from),
     Proposition('on', v_obj, v_obj_to)],
    # Deletes
    [Proposition('on', v_obj, v_obj_from),
     Proposition('on_table', v_obj, v_from),
     Proposition('not_on', v_obj, v_to),
     Proposition('on_top', v_obj, v_obj_from),
     Proposition('on_top', v_obj_to, v_to)]
    )


"""
1 
3 2
A B C
"""
prob1 = PlanningProblem('tower_of_hanoi',
    # Instances
    [i_small, i_med, i_large, i_rodA, i_rodB, i_rodC],
    # Operators
    [o_move],
    # Initial state
    [Proposition('on', i_small, i_large),
     Proposition('on', i_med, i_rodB),
     Proposition('on', i_large, i_rodA),
     Proposition('on_top', i_small, i_rodA),
     Proposition('on_top', i_med, i_rodB),
     Proposition('on_top', i_rodC, i_rodC),
     Proposition('on_table', i_small, i_rodA),
     Proposition('on_table', i_med, i_rodB),
     Proposition('on_table', i_large, i_rodA),
     Proposition('on_table', i_rodA, i_rodA),
     Proposition('on_table', i_rodB, i_rodB),
     Proposition('on_table', i_rodC, i_rodC),
     Proposition('not_on', i_small, i_rodB),
     Proposition('not_on', i_small, i_rodC),
     Proposition('not_on', i_med, i_rodB),],
     # Goals
     [Proposition('on', i_small, i_med),
      Proposition('on', i_med, i_large)])


"""
  1
3 2
A B C
"""
prob2 = PlanningProblem('tower_of_hanoi2',
    # Instances
    [i_small, i_med, i_large, i_rodA, i_rodB, i_rodC],
    # Operators
    [o_move],
    # Initial state
    [Proposition('on', i_small, i_med),
     Proposition('on', i_med, i_rodB),
     Proposition('on', i_large, i_rodA),
     Proposition('on_top', i_large, i_rodA),
     Proposition('on_top', i_small, i_rodB),
     Proposition('on_top', i_rodC, i_rodC),
     Proposition('on_table', i_small, i_rodB),
     Proposition('on_table', i_med, i_rodB),
     Proposition('on_table', i_large, i_rodA),
     Proposition('on_table', i_rodA, i_rodA),
     Proposition('on_table', i_rodB, i_rodB),
     Proposition('on_table', i_rodC, i_rodC)],
     # Goals
     [Proposition('on', i_small, i_med),
      Proposition('on', i_med, i_large)])


"""
1
2
3
A B C
"""
prob3 = PlanningProblem('tower_of_hanoi3',
    # Instances
    [i_small, i_med, i_large, i_rodA, i_rodB, i_rodC],
    # Operators
    [o_move],
    # Initial state
    [Proposition('on', i_small, i_med),
     Proposition('on', i_med, i_large),
     Proposition('on', i_large, i_rodA),
     Proposition('on_top', i_small, i_rodA),
     Proposition('on_top', i_rodB, i_rodB),
     Proposition('on_top', i_rodC, i_rodC),
     Proposition('on_table', i_small, i_rodA),
     Proposition('on_table', i_med, i_rodA),
     Proposition('on_table', i_large, i_rodA),
     Proposition('on_table', i_rodA, i_rodA),
     Proposition('on_table', i_rodB, i_rodB),
     Proposition('on_table', i_rodC, i_rodC),
     Proposition('not_on', i_small, i_rodB),
     Proposition('not_on', i_small, i_rodC),
     Proposition('not_on', i_med, i_rodB),
     Proposition('not_on', i_med, i_rodC),
     Proposition('not_on', i_large, i_rodB),
     Proposition('not_on', i_large, i_rodC),],
     # Goals
     [Proposition('on', i_small, i_med),
      Proposition('on', i_med, i_large),
      Proposition('not_on', i_large, i_rodA)])

problem = prob3
problem.solve()
problem.display()
