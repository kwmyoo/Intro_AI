"""CSP (Constraint Satisfaction Problems) problems and solvers. (Chapter 6)."""

"""This file csp2.py is a modified subset of the csp.py file from the
AIMA code repository.  We've added an assignment_limit parameter to
backtracking_search, and modified both backtracking_search and
min_conflicts to print the number of assignments before returning, and
to indicate whether the search failed.
"""

from utils import *
import search
import copy

class CSP(search.Problem):
    """This class describes finite-domain Constraint Satisfaction Problems.
    A CSP is specified by the following inputs:
        vars        A list of variables; each is atomic (e.g. int or string).
        domains     A dict of {var:[possible_value, ...]} entries.
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b
    In the textbook and in most mathematical definitions, the
    constraints are specified as explicit pairs of allowable values,
    but the formulation here is easier to express and more compact for
    most cases. (For example, the n-Queens problem can be represented
    in O(n) space using this notation, instead of O(N^4) for the
    explicit representation.) In terms of describing the CSP as a
    problem, that's all there is.

    However, the class also supports data structures and methods that help you
    solve CSPs by calling a search function on the CSP.  Methods and slots are
    as follows, where the argument 'a' represents an assignment, which is a
    dict of {var:val} entries:
        assign(var, val, a)     Assign a[var] = val; do other bookkeeping
        unassign(var, a)        Do del a[var], plus other bookkeeping
        nconflicts(var, val, a) Return the number of other variables that
                                conflict with var=val
        curr_domains[var]       Slot: remaining consistent values for var
                                Used by constraint propagation routines.
    The following methods are used only by graph_search and tree_search:
        actions(state)          Return a list of actions
        result(state, action)   Return a successor of state
        goal_test(state)        Return true if all constraints satisfied
    The following are just for debugging purposes:
        nassigns                Slot: tracks the number of assignments made
        display(a)              Print a human-readable representation

    >>> search.depth_first_graph_search(australia)
    <Node (('WA', 'B'), ('Q', 'B'), ('T', 'B'), ('V', 'B'), ('SA', 'G'), ('NT', 'R'), ('NSW', 'R'))>
    """

    def __init__(self, vars, domains, neighbors, constraints, default_assignment_limit=None):
        "Construct a CSP problem. If vars is empty, it becomes domains.keys()."
        vars = vars or domains.keys()
        update(self, vars=vars, domains=domains,
               neighbors=neighbors, constraints=constraints,
               initial=(), curr_domains=None, nassigns=0,
               assignment_limit=default_assignment_limit,
               default_assignment_limit=default_assignment_limit)

    def assign(self, var, val, assignment):
        "Add {var: val} to assignment; Discard the old value if any."
        assignment[var] = val
        self.nassigns += 1
        if self.assignment_limit and self.nassigns > self.assignment_limit:
            raise ValueError('Assignment limit %d exceeded.' % self.assignment_limit)

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]

    def nconflicts(self, var, val, assignment):
        "Return the number of conflicts var=val has with other variables."
        # Subclasses may implement this more efficiently
        def conflict(var2):
            return (var2 in assignment
                    and not self.constraints(var, val, var2, assignment[var2]))
        return count_if(conflict, self.neighbors[var])

    def display(self, assignment):
        "Show a human-readable representation of the CSP."
        # Subclasses can print in a prettier way, or display with a GUI
        print 'CSP:', self, 'with assignment:', assignment

    ## These methods are for the tree- and graph-search interface:

    def actions(self, state):
        """Return a list of applicable actions: nonconflicting
        assignments to an unassigned variable."""
        if len(state) == len(self.vars):
            return []
        else:
            assignment = dict(state)
            var = find_if(lambda v: v not in assignment, self.vars)
            return [(var, val) for val in self.domains[var]
                    if self.nconflicts(var, val, assignment) == 0]

    def result(self, state, (var, val)):
        "Perform an action and return the new state."
        return state + ((var, val),)

    def goal_test(self, state):
        "The goal is to assign all vars, with all constraints satisfied."
        assignment = dict(state)
        return (len(assignment) == len(self.vars) and
                every(lambda var: self.nconflicts(var, assignment[var],
                                                  assignment) == 0,
                      self.vars))

    ## These are for constraint propagation

    def support_pruning(self):
        """Make sure we can prune values from domains. (We want to pay
        for this only if we use it.)"""
        if self.curr_domains is None:
            self.curr_domains = dict((v, list(self.domains[v]))
                                     for v in self.vars)

    def suppose(self, var, value):
        "Start accumulating inferences from assuming var=value."
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        "Rule out var=value."
        self.curr_domains[var].remove(value)
        if removals is not None: removals.append((var, value))

    def choices(self, var):
        "Return all values for var that aren't currently ruled out."
        return (self.curr_domains or self.domains)[var]

    def infer_assignment(self):
        "Return the partial assignment implied by the current inferences."
        self.support_pruning()
        return dict((v, self.curr_domains[v][0])
                    for v in self.vars if 1 == len(self.curr_domains[v]))

    def restore(self, removals):
        "Undo a supposition and all inferences from it."
        for B, b in removals:
            self.curr_domains[B].append(b)

    ## This is for min_conflicts search

    def conflicted_vars(self, current):
        "Return a list of variables in current assignment that are in conflict"
        return [var for var in self.vars
                if self.nconflicts(var, current[var], current) > 0]

#______________________________________________________________________________
# Constraint Propagation with AC-3

def AC3(csp, queue=None, removals=None):
    """[Fig. 6.3]"""
    if queue is None:
        queue = [(Xi, Xk) for Xi in csp.vars for Xk in csp.neighbors[Xi]]
    csp.support_pruning()
    while queue:
        (Xi, Xj) = queue.pop()
        if revise(csp, Xi, Xj, removals):
            if not csp.curr_domains[Xi]:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xi:
                    queue.append((Xk, Xi))
    return True

def revise(csp, Xi, Xj, removals):
    "Return true if we remove a value."
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if every(lambda y: not csp.constraints(Xi, x, Xj, y),
                 csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
    return revised

#______________________________________________________________________________
# CSP Backtracking Search

# Variable ordering

def first_unassigned_variable(assignment, csp):
    "The default variable order."
    return find_if(lambda var: var not in assignment, csp.vars)

def mrv(assignment, csp):
    "Minimum-remaining-values heuristic."
    return argmin_random_tie(
        [v for v in csp.vars if v not in assignment],
        lambda var: num_legal_values(csp, var, assignment))

def num_legal_values(csp, var, assignment):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        return count_if(lambda val: csp.nconflicts(var, val, assignment) == 0,
                        csp.domains[var])

# Value ordering

def unordered_domain_values(var, assignment, csp):
    "The default value order."
    return csp.choices(var)

def lcv(var, assignment, csp):
    "Least-constraining-values heuristic."
    return sorted(csp.choices(var),
                  key=lambda val: csp.nconflicts(var, val, assignment))

# Inference

def no_inference(csp, var, value, assignment, removals):
    return True

def forward_checking(csp, var, value, assignment, removals):
    "Prune neighbor values inconsistent with var=value."
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                return False
    return True

def mac(csp, var, value, assignment, removals):
    "Maintain arc consistency."
    return AC3(csp, [(X, var) for X in csp.neighbors[var]], removals)

# The search, proper

def backtracking_search(csp,
                        select_unassigned_variable = first_unassigned_variable,
                        order_domain_values = unordered_domain_values,
                        inference = no_inference,
                        assignment_limit = None):
    """[Fig. 6.5]
    >>> backtracking_search(australia) is not None
    True
    >>> backtracking_search(australia, select_unassigned_variable=mrv) is not None
    True
    >>> backtracking_search(australia, order_domain_values=lcv) is not None
    True
    >>> backtracking_search(australia, select_unassigned_variable=mrv, order_domain_values=lcv) is not None
    True
    >>> backtracking_search(australia, inference=forward_checking) is not None
    True
    >>> backtracking_search(australia, inference=mac) is not None
    True
    >>> backtracking_search(usa, select_unassigned_variable=mrv, order_domain_values=lcv, inference=mac) is not None
    True
    """

    def backtrack(assignment):
        if len(assignment) == len(csp.vars):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    # Reset the problem state in case we are reusing a previously solved instance.
    csp.nassigns = 0
    csp.curr_domains = None
    csp.assignment_limit = assignment_limit or csp.default_assignment_limit

    result = backtrack(dict())
    if result is None:
        fail_string = 'Failed. '
    else:
        fail_string = ''
    print fail_string+'nassigns =', csp.nassigns
    assert result is None or csp.goal_test(result)
    return result

#______________________________________________________________________________
# Min-conflicts hillclimbing search for CSPs

def min_conflicts(csp, max_steps=100000):
    """Solve a CSP by stochastic hillclimbing on the number of conflicts."""
    # Reset the problem state in case we are reusing a previously solved instance.
    csp.nassigns = 0
    csp.curr_domains = None
    # Generate a complete assignment for all vars (probably with conflicts)
    csp.current = current = {}
    for var in csp.vars:
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
    # Now repeatedly choose a random conflicted variable and change it
    for i in range(max_steps):
        conflicted = csp.conflicted_vars(current)
        if not conflicted:
            print 'nassigns =', csp.nassigns
            return current
        var = random.choice(conflicted)
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
    print 'Failed. nassigns =', csp.nassigns
    return None

def min_conflicts_value(csp, var, current):
    """Return the value that will give var the least number of conflicts.
    If there is a tie, choose at random."""
    return argmin_random_tie(csp.domains[var],
                             lambda val: csp.nconflicts(var, val, current))

#______________________________________________________________________________
# Map-Coloring Problems

class UniversalDict:
    """A universal dict maps any key to the same value. We use it here
    as the domains dict for CSPs in which all vars have the same domain.
    >>> d = UniversalDict(42)
    >>> d['life']
    42
    """
    def __init__(self, value): self.value = value
    def __getitem__(self, key): return self.value
    def __repr__(self): return '{Any: %r}' % self.value

def different_values_constraint(A, a, B, b):
    "A constraint saying two neighboring variables must differ in value."
    return a != b

def MapColoringCSP(colors, neighbors):
    """Make a CSP for the problem of coloring a map with different colors
    for any two adjacent regions.  Arguments are a list of colors, and a
    dict of {region: [neighbor,...]} entries.  This dict may also be
    specified as a string of the form defined by parse_neighbors."""
    if isinstance(neighbors, str):
        neighbors = parse_neighbors(neighbors)
    return CSP(neighbors.keys(), UniversalDict(colors), neighbors,
               different_values_constraint)

def parse_neighbors(neighbors, vars=[]):
    """Convert a string of the form 'X: Y Z; Y: Z' into a dict mapping
    regions to neighbors.  The syntax is a region name followed by a ':'
    followed by zero or more region names, followed by ';', repeated for
    each region name.  If you say 'X: Y' you don't need 'Y: X'.
    >>> parse_neighbors('X: Y Z; Y: Z')
    {'Y': ['X', 'Z'], 'X': ['Y', 'Z'], 'Z': ['X', 'Y']}
    """
    dict = DefaultDict([])
    for var in vars:
        dict[var] = []
    specs = [spec.split(':') for spec in neighbors.split(';')]
    for (A, Aneighbors) in specs:
        A = A.strip()
        dict.setdefault(A, [])
        for B in Aneighbors.split():
            if B not in dict[A]: dict[A].append(B)
            if A not in dict[B]: dict[B].append(A)
    return dict

australia = MapColoringCSP(list('RGB'),
                           'SA: WA NT Q NSW V; NT: WA Q; NSW: Q V; T: ')

usa = MapColoringCSP(list('RGBY'),
        """WA: OR ID; OR: ID NV CA; CA: NV AZ; NV: ID UT AZ; ID: MT WY UT;
        UT: WY CO AZ; MT: ND SD WY; WY: SD NE CO; CO: NE KA OK NM; NM: OK TX;
        ND: MN SD; SD: MN IA NE; NE: IA MO KA; KA: MO OK; OK: MO AR TX;
        TX: AR LA; MN: WI IA; IA: WI IL MO; MO: IL KY TN AR; AR: MS TN LA;
        LA: MS; WI: MI IL; IL: IN KY; IN: OH KY; MS: TN AL; AL: TN GA FL;
        MI: OH IN; OH: PA WV KY; KY: WV VA TN; TN: VA NC GA; GA: NC SC FL;
        PA: NY NJ DE MD WV; WV: MD VA; VA: MD DC NC; NC: SC; NY: VT MA CT NJ;
        NJ: DE; DE: MD; MD: DC; VT: NH MA; MA: NH RI CT; CT: RI; ME: NH;
        HI: ; AK: """)

france = MapColoringCSP(list('RGBY'),
        """AL: LO FC; AQ: MP LI PC; AU: LI CE BO RA LR MP; BO: CE IF CA FC RA
        AU; BR: NB PL; CA: IF PI LO FC BO; CE: PL NB NH IF BO AU LI PC; FC: BO
        CA LO AL RA; IF: NH PI CA BO CE; LI: PC CE AU MP AQ; LO: CA AL FC; LR:
        MP AU RA PA; MP: AQ LI AU LR; NB: NH CE PL BR; NH: PI IF CE NB; NO:
        PI; PA: LR RA; PC: PL CE LI AQ; PI: NH NO CA IF; PL: BR NB CE PC; RA:
        AU BO FC PA LR""")

france3 = MapColoringCSP(list('RGB'),
        """AL: LO FC; AQ: MP LI PC; AU: LI CE BO RA LR MP; BO: CE IF CA FC RA
        AU; BR: NB PL; CA: IF PI LO FC BO; CE: PL NB NH IF BO AU LI PC; FC: BO
        CA LO AL RA; IF: NH PI CA BO CE; LI: PC CE AU MP AQ; LO: CA AL FC; LR:
        MP AU RA PA; MP: AQ LI AU LR; NB: NH CE PL BR; NH: PI IF CE NB; NO:
        PI; PA: LR RA; PC: PL CE LI AQ; PI: NH NO CA IF; PL: BR NB CE PC; RA:
        AU BO FC PA LR""")

southam = MapColoringCSP(list('RGBY'),
            """CO: EC PE BR VE; EC: PE; PE: CH BR BO; BR: VE GU SU FG BO PA AR
            UR; VE: GU; GU: SU; SU: FG; BO: CH AR PA; CH: AR; AR: PA UR;
            FA: """)

southam3 = MapColoringCSP(list('RGB'),
            """CO: EC PE BR VE; EC: PE; PE: CH BR BO; BR: VE GU SU FG BO PA AR
            UR; VE: GU; GU: SU; SU: FG; BO: CH AR PA; CH: AR; AR: PA UR;
            FA: """)


#______________________________________________________________________________
# Cryptoarithmetic problem

def generateBinConstraint(strList1, strList2, strList3, i):
    apprList = []
    domainDict = {}
    neighString = ""

    if i == len(strList3):
        temp = {('C' + str(i)): 0}
        apprList.append(temp)
        domainDict[('U' + str(i))] = apprList
        domainDict[('C' + str(i))] = range(2)
        neighString = 'U' + str(i) + ": "
        neighString += ('C' + str(i))
        neighString += '; '
        return domainDict, neighString

    if (len(strList1) > i) and (len(strList2) > i):
        if (strList1[i] != strList2[i]):
            for x in range(10):
                for y in range(10):
                    for ci in range(2):
                        z = (x + y + ci) % 10
                        ci1 = (x + y + ci) / 10
                        temp = {strList1[i]: x}
                        if (not(strList2[i] in temp)) or (temp[strList2[i]] == y):
                            temp[strList2[i]] = y
                            if (not (strList3[i] in temp)) or (temp[strList3[i]] == z):
                                temp[strList3[i]] = z
                                temp[('C' + str(i))] = ci
                                temp[('C' + str(i+1))] = ci1
                                apprList.append(temp)

            neighString = 'U' + str(i) + ": "
            neighString += (strList1[i] + ' ')
            neighString += (strList2[i] + ' ')

        else:
            for x in range(10):
                for ci in range(2):
                    z = (2 * x + ci) % 10
                    ci1 = (2 * x + ci) / 10
                    temp = {strList1[i]: x}
                    if (not (strList3[i] in temp)) or (temp[strList3[i]] == z):
                        temp[strList3[i]] = z
                        temp[('C' + str(i))] = ci
                        temp[('C' + str(i+1))] = ci1
                        apprList.append(temp)

            neighString = 'U' + str(i) + ": "
            neighString += (strList1[i] + ' ')

        domainDict[strList1[i]] = range(10)
        domainDict[strList2[i]] = range(10)
        domainDict[strList3[i]] = range(10)
        domainDict[('C' + str(i))] = range(2)
        domainDict[('C' + str(i+1))] = range(2)

        neighString += (strList3[i] + ' ')
        neighString += ('C' + str(i) + ' ')
        neighString += ('C' + str(i+1) + '; ')

    elif (len(strList1) > i) and (len(strList2) <= i):
        for x in range(10):
            for ci in range(2):
                z = (x + ci) % 10
                ci1 = (x + ci) / 10
                temp = {strList1[i]: x}
                if (not (strList3[i] in temp)) or (temp[strList3[i]] == z):
                    temp[strList3[i]] = z
                    temp[('C' + str(i))] = ci
                    temp[('C' + str(i+1))] = ci1
                    apprList.append(temp)

        domainDict[strList1[i]] = range(10)
        domainDict[strList3[i]] = range(10)
        domainDict[('C' + str(i))] = range(2)
        domainDict[('C' + str(i+1))] = range(2)

        neighString = 'U' + str(i) + ': '
        neighString += (strList1[i] + ' ')
        neighString += (strList3[i] + ' ')
        neighString += ('C' + str(i) + ' ')
        neighString += ('C' + str(i+1) + '; ')

    elif (len(strList1) <= i) and (len(strList2) > i):
        for y in range(10):
            for ci in range(2):
                z = (y + ci) % 10
                ci1 = (y + ci) / 10
                temp = {strList2[i]: y}
                if (not (strList3[i] in temp)) or (temp[strList3[i]] == z):
                    temp[strList3[i]] = z
                    temp[('C' + str(i))] = ci
                    temp[('C' + str(i+1))] = ci1
                    apprList.append(temp)

        domainDict[strList2[i]] = range(10)
        domainDict[strList3[i]] = range(10)
        domainDict[('C' + str(i))] = range(2)
        domainDict[('C' + str(i+1))] = range(2)

        neighString = 'U' + str(i) + ': '
        neighString += (strList2[i] + ' ')
        neighString += (strList3[i] + ' ')
        neighString += ('C' + str(i) + ' ')
        neighString += ('C' + str(i+1) + '; ')

    else:
        for ci in range(2):
            z = ci % 10
            ci1 = ci / 10
            temp = {strList3[i]: z, ('C' + str(i)): ci,
                    ('C' + str(i+1)): ci1}
            apprList.append(temp)

        domainDict[strList3[i]] = range(10)
        domainDict[('C' + str(i))] = range(2)
        domainDict[('C' + str(i+1))] = range(2)

        neighString = 'U' + str(i) + ': '
        neighString += (strList3[i] + ' ')
        neighString += ('C' + str(i) + ' ')
        neighString += ('C' + str(i+1) + '; ')

    domainDict[('U' + str(i))] = apprList
    return domainDict, neighString

def CryptConstraint(A, a, B, b):
    if (len(A) == 1) and (len(B) == 1):
        return a != b
    
    elif (len(A) > 1) and (len(B) == 1):
        return a[B] == b

    elif (len(A) == 1) and (len(B) > 1):
        return b[A] == a

    else:
        if 'C' in A:
            return b[A] == a
        elif 'C' in B:
            return a[B] == b
        else:
            for val in a.keys():
                if (val in b):
                    if a[val] != b[val]:
                        return False
            return True

def allDiff(strList1, strList2, strList3):
    neighString = ""
    totalList = copy.copy(strList1)
    totalList.extend(strList2)
    totalList.extend(strList3)
    totalList = list(set(totalList))

    for i in range(len(totalList) - 1):
        temp = totalList[i]
        neighString += (temp + ': ')

        for j in range((i + 1), len(totalList)):
            neighString += totalList[j]
            if j == (len(totalList) - 1):
                neighString += '; '
            else:
                neighString += ' '

    return neighString

def CryptCSP(str1, str2, str3):
    strList1 = list(str1)
    strList1.reverse()
    strList2 = list(str2)
    strList2.reverse()
    strList3 = list(str3)
    strList3.reverse()

    variables = []
    domain = {}
    neighbors = ""
    tempList = []

    for i in range(len(strList3) + 1):
        (newDomain, neighString) = generateBinConstraint(strList1,
                                                         strList2, strList3, i)
        newVariables = newDomain.keys()

        for j in range(len(newVariables)):
            tempVar = newVariables[j]

            if not(tempVar in variables):
                variables.append(tempVar)
                domain[tempVar] = newDomain[tempVar]

        neighbors += neighString

    variables.extend(['L1', 'L2', 'L3', 'L4'])
    domain['L1'] = []
    domain['L2'] = []
    domain['L3'] = []
    domain['L4'] = [{'C0': 0}]

    for i in [1,2,3,4,5,6,7,8,9]:
        domain['L1'].append({strList1[(len(strList1) - 1)]: i})
        domain['L2'].append({strList2[(len(strList2) - 1)]: i})
        domain['L3'].append({strList3[(len(strList3) - 1)]: i})

    neighbors += ('L1: ' + strList1[(len(strList1) - 1)] + '; ')
    neighbors += ('L2: ' + strList2[(len(strList2) - 1)] + '; ')
    neighbors += ('L3: ' + strList3[(len(strList3) - 1)] + '; ')
    neighbors += allDiff(strList1, strList2, strList3)

    neighbors += "L4: C0"
    neighbors = parse_neighbors(neighbors)

    return CSP(variables, domain, neighbors, CryptConstraint)
