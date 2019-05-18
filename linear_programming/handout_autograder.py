import argparse
import json
import os
import os.path
import signal

import sys
import time
import timeit
import traceback

import copy as copy
import numpy as np

autoDir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, autoDir)

maxRunTime = 10 # Max number of seconds per sub-test.

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--solutionDir', default='.')
    args = parser.parse_args()

    print("=== Homework 3 ===")
    sys.path.insert(1, args.solutionDir)
    try:
        global simplex
        global used_cvxpy
        global used_gurobi
        import simplex as simplex
        used_cvxpy = check_for_cvxpy()
        used_gurobi = check_for_gurobi()
        global milp
        import milp
        global gpy
        import gurobipy as gpy
    except Exception as e:
        print("""
The following error occurred when trying to load one of your modules:

------
{}
------

Check to see if your tgz was created properly without
a directory structure. Listing the contents like this
should result in the following output.
If you see a directory structure here, re-create a
tgz without the directory structure and submit again.

    $ tar tf handin.tgz
    writeup.pdf
    search.py""".format(e))
        sys.exit(-1)

    scores = {}
    scores['Simplex'] = test_simplex()
    scores['MILP'] = test_milp()
    out = {'scores': scores}
    print(json.dumps(out))

def test(tag, maxScore):
    def test_decorator(func):
        def func_wrapper():
            print("\n=== Start {} Test ===".format(tag))
            score = func()
            print("=== End {} Test. Score: {}/{} ===\n".format(tag, score, maxScore))
            return score

        return func_wrapper
    return test_decorator

def run_test_simplex(test_id, primal, simplex_method, two_phase = False):
    data=np.load('simplex_tests/test{0}.npz'.format(test_id))
    I,I_dual,A,b,c,f,x = data['I'], data['I_dual'], data['A'], data['b'], data['c'], data['f'], data['x']

    try:
        if not two_phase:
            f1,x1 = simplex_method(I, c, A, b)
        elif two_phase:
            f1,x1 = simplex_method(c, A, b)
    except Exception as e:
        print(e.__doc__)
        print(str(e))
        print(traceback.format_exc())
        return False

    if np.linalg.norm(x1 - x) < 1e-10:
        print("  + simplex passed test {0}".format(test_id))
        return True
    else:
        print("  + simplex failed test {0}".format(test_id))
        return False

def run_test_milp(test_id, milp_method):
    data=np.load('milp_tests/test{0}.npz'.format(test_id))
    I, A, B, C, T, R = data['I'], data['A'], data['B'], data['C'], data['T'], data['R']

    model = milp_method(I, A, B, C, T)
    model.setParam('OutputFlag',0)
    model.optimize()

    if model.status == gpy.GRB.Status.OPTIMAL:
        if model.objVal == R:
            print("  + milp passed test {0}".format(test_id))
            return True
        elif R == -1:
            print("  + milp failed test {0}: LP should not converge to an integer solution".format(test_id))
            print('  +       Your answer: {0}'.format(model.objVal))
            return False
        else:
            print("  + milp failed test {0}: LP does not converge to the integer solution that your implementation returns".format(test_id))
            print('  +   Expected answer: {0}'.format(R))
            print('  +       Your answer: {0}'.format(model.objVal))
            return False

    elif model.status == gpy.GRB.Status.INFEASIBLE:
        if R == -1:
            print("  + milp passed test {0}".format(test_id))
            return True
        else:
            print("  + milp failed test {0}: LP does not converge to an integer solution with your constraints".format(test_id))
            print('  +   Expected answer: {0}'.format(R))
            return False
    elif model.status == gpy.GRB.Status.UNBOUNDED:
        print("  + milp failed test {0}: your constraints are unbounded.".format(test_id))
        return False
    else:
        print("  + milp failed test {0}: Optimization was stopped with status %d".format(test_id) % model.status)
        return False

def check_for_cvxpy():
    used_cvxpy = False
    for line in open("simplex.py", "r"):
        if "cvxpy" in line:
            used_cvxpy = True
    if "cvxpy" in sys.modules:
        used_cvxpy = True
    if used_cvxpy:
        print("""
You are not allowed to use cvxpy in simplex.py!
Please make sure you do not import the library
or reference cvxpy anywhere in simplex.py.
""")
    return used_cvxpy

def check_for_gurobi():
    used_gurobi = False
    for line in open("simplex.py", "r"):
        if "gurobi" in line:
            used_gurobi = True
    if "gurobi" in sys.modules:
        used_gurobi = True
    if used_gurobi:
        print("""
You are not allowed to use gurobi in simplex.py!
Please make sure you do not import the library
or reference gurobi anywhere in simplex.py.
""")
    return used_gurobi

@test('simplex', 25)
def test_simplex():
    if used_cvxpy:
        return 0
    elif used_gurobi:
        return 0
    score = 0
    for t in xrange(25):
        try:
            if run_test_simplex(t, True, simplex.simplex):
                score += 1
        except Exception as e:
            print("""
                The following error occurred when trying to run your solution:

                ------
                {}
                ------""".format(e))
            continue
    return score


@test('milp', 15)
def test_milp():
    score = 0

    for t in xrange(15):
        try:
            if run_test_milp(t, milp.setup):
                score += 1
        except Exception as e:
            print("""
                The following error occurred when trying to run your solution:

                ------
                {}
                ------""".format(e))
            continue

    return score

if __name__=='__main__':
    main()
