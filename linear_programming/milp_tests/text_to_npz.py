import sys
import numpy as np
import re

def main():
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    else:
        print "Provide the path to the test case from the current directory"
        return 0
    iterator = 0
    test_num = 0

    I = []
    A = []
    B = []
    C = []
    T = []
    R = 0

    # I: 3
    # A: M x K
    # B: N
    # C: N x K
    # T: M x N


    lines = [line.rstrip('\n') for line in open(filename)]
    lines = [a.split("=") for a in lines]
    fixed_lines = [line[1] for line in lines if len(line) == 2]
    fixed_lines = [line.replace('[', '') for line in fixed_lines]
    fixed_lines = [line.replace(']', '') for line in fixed_lines]

    for line in fixed_lines:
        localiterator = 0
        entries = re.split('; |, ', line)
        M, N, K = 0, 0, 0
        if len(I) > 0:
            M = I[0]
            N = I[1]
            K = I[2]
        if iterator == 0:
            M = int(entries[0])
            N = int(entries[1])
            K = int(entries[2])
            I = [M, N, K]
            A = [[0 for k in xrange(K)] for i in xrange(M)]
            B = [0 for j in xrange(N)]
            C = [[0 for k in xrange(K)] for j in xrange(N)]
            T = [[0 for j in xrange(N)] for i in xrange(M)]
        elif iterator == 1:
            for i in xrange(M):
                for k in xrange(K):
                    A[i][k] = int(entries[localiterator])
                    localiterator += 1

        elif iterator == 2:
            for j in xrange(N):
                B[j] = int(entries[localiterator])
                localiterator += 1

        elif iterator == 3:
            for j in xrange(N):
                for k in xrange(K):
                    C[j][k] = int(entries[localiterator])
                    localiterator += 1

        elif iterator == 4:
            for i in xrange(M):
                for j in xrange(N):
                    T[i][j] = int(entries[localiterator])
                    localiterator += 1
        elif iterator == 5:
            R = int(entries[0])
            np.savez("custom_test_"+str(test_num)+".npz", I=I, A=A, B=B, C=C, T=T, R=R)
            test_num += 1
        iterator += 1
        iterator %= 6

if __name__ == "__main__":
    main()