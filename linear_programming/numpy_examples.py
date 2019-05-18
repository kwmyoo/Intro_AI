import numpy as np

def example_numpy_function():
    m,n = 2,3
    i = 2

    # to create the unit vector e_i:
    v = np.zeros(n) # creates an all-zero vector of dimension n
    v[i] = 1

    # create an m-by-n vector with random real numbers.
    A = np.random.randn(m,n)

    # Create a numpy array of 0,1,...,m-1
    I = np.array([x for x in range(0,m)])

    # Compute the inverse of the A_I, where I is a subset of columns
    AI = np.linalg.inv(A[:,I])

    # create a random numpy vector
    a = np.random.rand(n)
    b = np.random.rand(n)

    # matrix-vector multiplication
    x = A.dot(b)

    # take the outer product of vectors a and b
    rank1_matrix = np.outer(a, b)

    # return two values
    return (1,2)

# assign the two returned values
v1,v2 = example_numpy_function()
