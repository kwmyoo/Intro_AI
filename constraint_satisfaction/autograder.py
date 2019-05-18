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

STUDENT_CODE = 'csp2.py'
TEST_DIR = 'tests'
TOTAL_POINTS = 20

def loadModuleFile(moduleName, filePath):
    with open(filePath, 'r') as f:
        return imp.load_module(moduleName, f, "%s.py" % moduleName, (".py", "r", imp.PY_SOURCE))

def parseWords(cryptStr):
    '''
    cryptStr is of the form 'TWO + TWO = FOUR'
    '''
    m = re.match(
        '([A-Za-z]*?) \+ ([A-Za-z]*?) = ([A-Za-z]*)',
        cryptStr)

    return m.group(1).strip(), m.group(2).strip(), m.group(3).strip()

def readTestFile(testFilePath):
    with open(testFilePath) as f:
        sList = f.readlines()
        cryptStr = sList[0]
        return parseWords(cryptStr)
        

def collectTestCases(testDir):
    testFiles = os.listdir(testDir)
    res = []
    for testFile in testFiles:
        fullPath = os.path.abspath('/'.join([testDir,testFile]))
        try:
            testCase = readTestFile(fullPath)
            res.append(testCase)
        except Exception as e:
            print('Exception raised!', e)
            continue
    return res

def decrypt(s, solDict, testCount):
    res = ''
    for c in s:
        digit = solDict.get(c, None)
        if digit is None:
            print('[Test %d]: %s not found in solution dictionary!' %
                  (testCount, c))
            print('| Solution dict:')
            pprint(solDict)
            return None
        digit = str(digit)
        if not digit.isdigit():
            print('[Test %d]: %s not mapped to a digit!' % (testCount, c))
            print('| %s mapped to %s' % (c, digit))
            print('| Solution dict:')
            pprint(solDict)
            return None
        res += digit
    return res
        

def gradeTestCase(CSP, crypt, a, b, c, testCount):
    solDict = CSP.backtracking_search(
        crypt,
        inference=CSP.mac,
        select_unassigned_variable=CSP.mrv
    )
    
    if not solDict:
        print('[Test %d]: Failed to solve problem "%s + %s = %s"\n' %
              (testCount, a, b, c))
        return 0
    
    aStr = decrypt(a, solDict, testCount)
    if not aStr:
        return 0
    bStr = decrypt(b, solDict, testCount)
    if not bStr:
        return 0
    cStr = decrypt(c, solDict, testCount)
    if not cStr:
        return 0

    aInt = int(aStr)
    bInt = int(bStr)
    cInt = int(cStr)

    if (aInt + bInt != cInt):
        print('[Test %d]: Solution failed!' % testCount)
        print('| %s -> %d, %s -> %d, %s -> %d' % (a, aInt, b, bInt, c, cInt))
        print('| Solution dict:')
        pprint(solDict)
        return 0
    else:
        print('[Test %d]: Solution passed!' % testCount)
        print('| %s -> %d, %s -> %d, %s -> %d' % (a, aInt, b, bInt, c, cInt))
        return 1
        
def adjustScore(totalScore, totalTests):
    ratio = float(totalScore) / max(1,float(totalTests))
    floatGrade = ratio * TOTAL_POINTS
    intGrade = int(floor(floatGrade))
    return intGrade

def grade(CSP):
    testCases = collectTestCases(TEST_DIR)
    totalTests = len(testCases)
    testCount = 0
    totalScore = 0
    for a, b, c in testCases:
        testCount += 1
        crypt = CSP.CryptCSP(a,b,c)
        totalScore += gradeTestCase(CSP, crypt, a, b, c, testCount)

    grade = adjustScore(totalScore, totalTests)
    print('Testing results: [%d / %d]' % (totalScore, totalTests))
    # print('Grade for this problem: %d / %d' % (grade, TOTAL_POINTS))
    

if __name__ == '__main__':
    moduleName = re.match('.*?([^/]*)\.py', STUDENT_CODE).group(1)
    cspModule = loadModuleFile(moduleName, os.path.abspath(STUDENT_CODE))
    grade(cspModule)
