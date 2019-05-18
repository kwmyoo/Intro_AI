import numpy as np

##########################################################
# INPUT description:
# Your algorithms receive 4 inputs:
# I <- an initial feasible basis
# c <- a numpy array that you will use as your objective function
# A,b <- a matrix and vector describing the constraint
#
#      A.dot(x) = b
#
# OUTPUT description:
# You algorithms should return two things:
# 1. the value of the optimal solution v.
#     - Assuming an optimal solution x, get this with c.dot(x).
#     - Alternatively, you can use c[I].dot(xI), where xI
#       is the vector obtained from the optimal basis.
# 2. an optimal solution x
#     - This should be in the form of a numpy array.
#     - Assuming an optimal basis I and associated
#       inverse of A restricted to index set I, called AI,
#       you can construct it with:
#
#       x = np.zeros(c.shape[0])
#       x[I] = AI.dot(b)
#
# return them with the statement: return (v, x)
##########################################################

##########################################################
# Implement the simplex algorithm here.
##########################################################
def simplex(I, c, A, b):
    rows = len(A)
    cols = len(A[0])
    zero = -(10 ** (-12))
    AI = np.linalg.inv(A[:,I])
    x = AI.dot(b)
    found = False
    n = 0

    while True:
        AI = np.linalg.inv(A[:,I])
        for j in range(cols):
            temp = c[:,I].dot(AI)
            temp = temp.dot(A[:,j])
            temp = c[j] - temp

            if (temp < zero):
                found = True
                break

        if not(found):
            break

        found = False
        dJ = -(AI.dot(A[:,j]))
        for i in range(len(I)):
            if (dJ[i] < zero):
                iStar = i
                aStar =  -(x[i] / dJ[i])
                break

        for i in range(len(I)):
            temp = -(x[i] / dJ[i])

            if (temp < aStar) and (dJ[i] < zero):
                iStar = i
                aStar = temp
        for i in range(len(I)):
            x[i] = x[i] + (aStar * dJ[i])

        x[iStar] = aStar
        I[iStar] = j

    x = np.zeros(c.shape[0])
    AI = np.linalg.inv(A[:,I])
    x[I] = AI.dot(b)
    v = c.dot(x)
    return (v, x)
