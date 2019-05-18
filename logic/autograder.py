# autograder.py
# -------------
# A simple grading script inspired by the scripts provided by UC Berkeley
# at http://ai.berkeley.edu. The full notice is copied below:
# -------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
# -------------

import imp
import os
import re
import sys
from math import floor
from pprint import pprint

STUDENT_CODE = 'logic2.py'
TEST_DIR = 'tests'
TEST_FUNCTIONS = ['to_cnf', 'pl_resolution','pl_nature',]

class NullWriter():

    def write(self, arg):
        pass

def loadModuleFile(moduleName, filePath):
    with open(filePath, 'r') as f:
        return imp.load_module(moduleName, f,
                               "%s.py" % moduleName,
                               (".py", "r", imp.PY_SOURCE))

def readTestFile(LOGIC, testFilePath):
    with open(testFilePath) as f:
        sList = f.readlines()
        e = sList[0][:-1] # get rid of the newline character
        out = sList[1]
        return e, out

def readResolutionTestFile(LOGIC, testFilePath):
    with open(testFilePath) as f:
        sList = f.readlines()
        rules = eval(sList[0][:-1])
        e = sList[1][:-1]
        out = sList[2]
        kb = LOGIC.PropKB()
        print(rules)
        for rule in rules:
            kb.tell(rule)
        return (kb, e), out

READ_TEST_FILE = {
    'to_cnf': readTestFile,
    'pl_resolution': readResolutionTestFile,
    'pl_nature': readTestFile
}
    
def collectTestCases(LOGIC, testDir, func):
    testFiles = os.listdir(testDir)
    res = []
    for testFile in testFiles:
        if not testFile.startswith(func):
            continue
        fullPath = os.path.abspath('/'.join([testDir,testFile]))
        try:
            testCase, testOut = READ_TEST_FILE[func](LOGIC, fullPath)
            res.append((testCase, testOut))
        except Exception as e:
            print('Exception raised!', e)
            continue
    return res

def gradeToCNF(LOGIC, res, testOut):

    # testOut is a string that needs to be converted to a list of expressions
    fail = False

    if (res.op != '&'):
        # the only cases where this is legal is if we have a
        # singleton disjunctive clause, true or false
        if res.op in ['TRUE', 'FALSE']:
            return res.op == testOut
        elif res.op == '|':
            # it should be a singleton clause
            testOutSet = set([LOGIC.expr(p)
                               for p in testOut.strip()[1:-1].split('|')])
            return testOutSet == set(res.args)
        else:
            # can't have any other top-level operators
            return False
            
    else:
        # we can assume that res is in cnf, otherwise they'll fail
        # the test case: make a set of the clauses, iterate over
        # them, make a set of the arguments
        testOutArgs = testOut.split('&')
        # x.strip() removes whitespace,
        #          [1:-1] removes beginning and ending parentheses
        testOutSets = [set([LOGIC.expr(p) for p in x.strip()[1:-1].split('|')])
                       for x in testOutArgs]
        for arg in res.args:
            if arg.op != '|':
                fail = True
                break
            else:
                argSet = set([x for x in arg.args])
                if argSet not in testOutSets:
                    fail = True
                    break
    return (not fail)

def gradeDefault(LOGIC, res, testOut):
    return str(res) == str(testOut)

GRADE_FUNC = {
    'to_cnf': gradeToCNF,
    'pl_resolution': gradeDefault,
    'pl_nature': gradeDefault
}

def gradeTestCase(LOGIC, func, res, testCase, testOut, testCount):
    if (GRADE_FUNC[func](LOGIC, res, testOut)):
        print('[Test %d]: Solution passed!' % testCount)
        return 1
    else:
        print('[Test %d]: Solution failed!' % testCount)
        print('| Expected: %s' % testOut)
        print('| Result: %s' % res)
        return 0        

def grade(LOGIC):
    grade = dict()
    stdout = sys.stdout
    for f in TEST_FUNCTIONS:
        print('------------------')        
        print('Testing %s...' % f)
        testCases = collectTestCases(LOGIC, TEST_DIR, f)
        totalTests = len(testCases)
        testCount = 0
        totalScore = 0
        for testCase, testOut in testCases:
            testCount += 1
            testFunc = getattr(LOGIC, f)
            print("Testing case: %s" % str(testCase))
            # redirect stdout while calling student function
            nullWrite = NullWriter()
            sys.stdout = nullWrite

            if type(testCase) == tuple:
                res = testFunc(*testCase)
            else:
                res = testFunc(testCase)

            # re-redirect stdout back to normal
            sys.stdout = stdout
            
            totalScore += gradeTestCase(LOGIC, f, res,
                                        testCase, testOut, testCount)
        grade[f] = totalScore

if __name__ == '__main__':
    moduleName = re.match('.*?([^/]*)\.py', STUDENT_CODE).group(1)
    logicModule = loadModuleFile(moduleName, os.path.abspath(STUDENT_CODE))
    grade(logicModule)
