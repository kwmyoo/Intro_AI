
##########################################################
# INPUT description:
# Your algorithms receive 5 inputs:
# I <- [M, N, K]
# A <- a M by K matrix describing provider food stores.
#       Provider i has A[i][k] of food type k
# B <- a N length array describing community cumulative food needs
#       Community j needs a minimum of B[j] food (cumulative from all sources, of any type)
#       Example: If B[1] = 5, and community 1 receives a distribution of [2, 2, 3], the food needs are met
# C <- a N by K matrix describing individual community food needs
#       Community j needs a minimum of C[j][k] food of type k
# T <- a M by N matrix describing transport costs per unit of food
#       It costs T[i][j] to transport 1 unit of food from provider i to community j
#
# OUTPUT description:
# Your algorithm should return a Gurobi model m
# The autograder will be calling m.optimize() on your model, and checking if it provides the optimal result
#
# return the model with the statement: return m
##########################################################

##########################################################
# Implement the MILP representation of the problem here.
##########################################################

from gurobipy import *

def setup(I, A, B, C, T):
    m = Model("mip1")
    M, N, K = I[0], I[1], I[2]
    q = m.addVars(M, N, K, vtype=GRB.INTEGER)

    m.setObjective(quicksum([q[i,j,k] * T[i][j] for k in range(K)
                                       for j in range(N)
                                       for i in range(M)]), GRB.MINIMIZE)
    m.addConstrs((q[i,j,k] >= 0 for i in range(M)
                                for j in range(N)
                                for k in range(K)))
    m.addConstrs(((B[j] >= quicksum([q[i,j,k] for i in range(M)
                                         for k in range(K)]))
                            for j in range(N)))
    m.addConstrs(((C[j][k] >= quicksum([q[i,j,k] for i in range(M)]))
                                for j in range(N)
                                for k in range(K)))
    m.addConstrs(((A[i][k] >= quicksum([q[i,j,k] for j in range(N)]))
                                for i in range(M)
                                for k in range(K)))

    return m
    
