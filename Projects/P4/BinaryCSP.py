# Hint: from collections import deque
from Interface import *
from collections import deque

# = = = = = = = QUESTION 1  = = = = = = = #


def consistent(assignment, csp, var, value):
    """
    Checks if a value assigned to a variable is consistent with all binary constraints in a problem.
    Do not assign value to var.
    Only check if this value would be consistent or not.
    If the other variable for a constraint is not assigned,
    then the new value is consistent with the constraint.

    Args:
        assignment (Assignment): the partial assignment
        csp (ConstraintSatisfactionProblem): the problem definition
        var (string): the variable that would be assigned
        value (value): the value that would be assigned to the variable
    Returns:
        boolean
        True if the value would be consistent with all currently assigned values, False otherwise
    """
    # TODO: Question 1
    for constraint in csp.binaryConstraints:
        if constraint.affects(var):
            otherVariable = constraint.otherVariable(var)
            if assignment.isAssigned(otherVariable):
                if constraint.isSatisfied(value, assignment.assignedValues[otherVariable]):
                    continue
                else:
                    return False
    return True


def recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod):
    """
    Recursive backtracking algorithm.
    A new assignment should not be created.
    The assignment passed in should have its domains updated with inferences.
    In the case that a recursive call returns failure or a variable assignment is incorrect,
    the inferences made along the way should be reversed.
    See maintainArcConsistency and forwardChecking for the format of inferences.

    Examples of the functions to be passed in:
    orderValuesMethod: orderValues, leastConstrainingValuesHeuristic
    selectVariableMethod: chooseFirstVariable, minimumRemainingValuesHeuristic
    inferenceMethod: noInferences, maintainArcConsistency, forwardChecking

    Args:
        assignment (Assignment): a partial assignment to expand upon
        csp (ConstraintSatisfactionProblem): the problem definition
        orderValuesMethod (function<assignment, csp, variable> returns list<value>):
            a function to decide the next value to try
        selectVariableMethod (function<assignment, csp> returns variable):
            a function to decide which variable to assign next
        inferenceMethod (function<assignment, csp, variable, value> returns set<variable, value>):
            a function to specify what type of inferences to use
    Returns:
        Assignment
        A completed and consistent assignment. None if no solution exists.
    """
    # TODO: Question 1
    if assignment.isComplete():
        return assignment
    var = selectVariableMethod(assignment, csp)
    interences = set([])
    for value in orderValuesMethod(assignment, csp, var):
        if consistent(assignment, csp, var, value):
            assignment.assignedValues[var] = value
            inferences = inferenceMethod(assignment, csp, var, value)
            if inferences is not None:
                result = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod)
                if result is not None:
                    return result
                for i in inferences:
                    assignment.varDomains[i[0]].add(i[1])
        assignment.assignedValues[var] = None
        for i in interences:
            assignment.varDomains[i[0]].remove(i[1])
    return None


def eliminateUnaryConstraints(assignment, csp):
    """
    Uses unary constraints to eleminate values from an assignment.

    Args:
        assignment (Assignment): a partial assignment to expand upon
        csp (ConstraintSatisfactionProblem): the problem definition
    Returns:
        Assignment
        An assignment with domains restricted by unary constraints. None if no solution exists.
    """
    domains = assignment.varDomains
    for var in domains:
        for constraint in (c for c in csp.unaryConstraints if c.affects(var)):
            for value in (v for v in list(domains[var]) if not constraint.isSatisfied(v)):
                domains[var].remove(value)
                # Failure due to invalid assignment
                if len(domains[var]) == 0:
                    return None
    return assignment


def chooseFirstVariable(assignment, csp):
    """
    Trivial method for choosing the next variable to assign.
    Uses no heuristics.
    """
    for var in csp.varDomains:
        if not assignment.isAssigned(var):
            return var


# = = = = = = = QUESTION 2  = = = = = = = #


def minimumRemainingValuesHeuristic(assignment, csp):
    """
    Selects the next variable to try to give a value to in an assignment.
    Uses minimum remaining values heuristic to pick a variable. Use degree heuristic for breaking ties.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
    Returns:
        the next variable to assign
    """
    nextVar = None
    domains = assignment.varDomains

    # TODO: Question 2
    unassigned = []
    for var in domains:
        if not assignment.isAssigned(var):
            unassigned.append([var, len(domains[var]), degreeHeuristic(assignment, csp, var)])
    min = float("inf")
    degree = 0
    for i in unassigned:
        if i[1] < min or (i[1] == min and i[2] > degree):
            nextVar = i[0]
            min = i[1]
            degree = i[2]
    return nextVar

def degreeHeuristic(assignment, csp, var):
    ans = 0
    for constraint in csp.binaryConstraints:
        if constraint.affects(var):
            otherVariable = constraint.otherVariable(var)
            if not assignment.isAssigned(otherVariable):
                ans += 1
    return ans

def orderValues(assignment, csp, var):
    """
    Trivial method for ordering values to assign.
    Uses no heuristics.
    """
    return list(assignment.varDomains[var])


# = = = = = = = QUESTION 3  = = = = = = = #


def leastConstrainingValuesHeuristic(assignment, csp, var):
    """
    Creates an ordered list of the remaining values left for a given variable.
    Values should be attempted in the order returned.
    The least constraining value should be at the front of the list.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var (string): the variable to be assigned the values
    Returns:
        list<values>
        a list of the possible values ordered by the least constraining value heuristic
    """
    # TODO: Question 3
    ans = []
    temp =[]
    for value in assignment.varDomains[var]:
        ruleout = 0
        for constraint in csp.binaryConstraints:
            if constraint.affects(var):
                otherVariable = constraint.otherVariable(var)
                for otherValue in assignment.varDomains[otherVariable]:
                    if not constraint.isSatisfied(value, otherValue):
                        ruleout += 1
        temp.append((value, ruleout))
    temp.sort(key = takeSecond)
    for i in temp:
        ans.append(i[0])
    return ans

def takeSecond(element):
    return element[1]


def noInferences(assignment, csp, var, value):
    """
    Trivial method for making no inferences.
    """
    return set([])


# = = = = = = = QUESTION 4  = = = = = = = #


def forwardChecking(assignment, csp, var, value):
    """
    Implements the forward checking algorithm.
    Each inference should take the form of (variable, value)
    where the value is being removed from the domain of variable.
    This format is important so that the inferences can be reversed
    if they result in a conflicting partial assignment.
    If the algorithm reveals an inconsistency,
    any inferences made should be reversed before ending the function.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var (string): the variable that has just been assigned a value
        value (string): the value that has just been assigned
    Returns:
        set< tuple<variable, value> >
        the inferences made in this call or None if inconsistent assignment
    """
    inferences = set([])

    # TODO: Question 4
    for constraint in csp.binaryConstraints:
        if constraint.affects(var):
            otherVariable = constraint.otherVariable(var)
            if assignment.isAssigned(otherVariable):
                continue
            else:
                removed = set([])
                for otherValue in assignment.varDomains[otherVariable]:
                    if not constraint.isSatisfied(value, otherValue):
                        inferences.add((otherVariable, otherValue))
                        removed.add(otherValue)
                if removed == assignment.varDomains[otherVariable]:
                    return None
    for i in inferences:
        assignment.varDomains[i[0]].remove(i[1])
    return inferences


# = = = = = = = QUESTION 5  = = = = = = = #


def revise(assignment, csp, var1, var2, constraint):
    """
    Helper function to maintainArcConsistency and AC3.
    Remove values from var2 domain if constraint cannot be satisfied.
    Each inference should take the form of (variable, value)
    where the value is being removed from the domain of variable.
    This format is important so that the inferences can be reversed
    if they result in a conflicting partial assignment.
    If the algorithm reveals an inconsistency,
    any inferences made should be reversed before ending the function.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var1 (string): the variable with consistent values
        var2 (string): the variable that should have inconsistent values removed
        constraint (BinaryConstraint): the constraint connecting var1 and var2
    Returns:
        set<tuple<variable, value>>
        the inferences made in this call or None if inconsistent assignment
    """
    inferences = set([])

    # TODO: Question 5
    for value2 in assignment.varDomains[var2]:
        revised = True
        for value1 in assignment.varDomains[var1]:
            if constraint.isSatisfied(value1, value2):
                revised = False
                break
        if revised:
            inferences.add((var2, value2))
    if len(inferences) == len(assignment.varDomains[var2]):
        return None
    for i in inferences:
        assignment.varDomains[i[0]].remove(i[1])
    return inferences


def maintainArcConsistency(assignment, csp, var, value):
    """
    Implements the maintaining arc consistency algorithm.
    Inferences take the form of (variable, value)
    where the value is being removed from the domain of variable.
    This format is important so that the inferences can be reversed
    if they result in a conflicting partial assignment.
    If the algorithm reveals an inconsistency,
    and inferences made should be reversed before ending the function.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var (string): the variable that has just been assigned a value
        value (string): the value that has just been assigned
    Returns:
        set<<variable, value>>
        the inferences made in this call or None if inconsistent assignment
    """
    inferences = set([])
    domains = assignment.varDomains

    # TODO: Question 5
    #  Hint: implement revise first and use it as a helper function"""
    q = deque()
    for constraint in csp.binaryConstraints:
        if constraint.affects(var):
            otherVariable = constraint.otherVariable(var)
            if not assignment.isAssigned(otherVariable):
                q.append((var, otherVariable, constraint))
    while len(q) > 0:
        (xi, xj, constraint) = q.pop()
        r = revise(assignment, csp, xi, xj, constraint)
        if r is None:
            for i in inferences:
                domains[i[0]].add(i[1])
            return None
        if len(r):
            for constraint in csp.binaryConstraints:
                if constraint.affects(xj):
                    otherVariable = constraint.otherVariable(xj)
                    q.append((xj, otherVariable, constraint))
            for i in r:
                inferences.add(i)
    return inferences


# = = = = = = = QUESTION 6  = = = = = = = #


def AC3(assignment, csp):
    """
    AC3 algorithm for constraint propagation.
    Used as a pre-processing step to reduce the problem
    before running recursive backtracking.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
    Returns:
        Assignment
        the updated assignment after inferences are made or None if an inconsistent assignment
    """
    inferences = set([])

    # TODO: Question 6
    #  Hint: implement revise first and use it as a helper function"""
    q = deque()
    for var in csp.varDomains:
        for constraint in csp.binaryConstraints:
            if constraint.affects(var):
                otherVariable = constraint.otherVariable(var)
                q.append((var, otherVariable, constraint))
    while len(q) > 0:
        (xi, xj, constraint) = q.pop()
        r = revise(assignment, csp, xi, xj, constraint)
        if r is None:
            for i in inferences:
                assignment.varDomains[i[0]].add(i[1])
            return None
        if len(r):
            for constraint in csp.binaryConstraints:
                if constraint.affects(xj):
                    otherVariable = constraint.otherVariable(xj)
                    q.append((xj, otherVariable, constraint))
            for i in r:
                inferences.add(i)
    return assignment


def solve(csp, orderValuesMethod=leastConstrainingValuesHeuristic,
          selectVariableMethod=minimumRemainingValuesHeuristic,
          inferenceMethod=forwardChecking, useAC3=True):
    """
    Solves a binary constraint satisfaction problem.

    Args:
        csp (ConstraintSatisfactionProblem): a CSP to be solved
        orderValuesMethod (function): a function to decide the next value to try
        selectVariableMethod (function): a function to decide which variable to assign next
        inferenceMethod (function): a function to specify what type of inferences to use
        useAC3 (boolean): specifies whether to use the AC3 pre-processing step or not
    Returns:
        dictionary<string, value>
        A map from variables to their assigned values. None if no solution exists.
    """
    assignment = Assignment(csp)

    assignment = eliminateUnaryConstraints(assignment, csp)
    if assignment is None:
        return assignment

    if useAC3:
        assignment = AC3(assignment, csp)
        if assignment is None:
            return assignment

    assignment = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod)
    if assignment is None:
        return assignment

    return assignment.extractSolution()
