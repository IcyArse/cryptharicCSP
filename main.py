import re

class CSP:
    def __init__(self, variables, domains, constraints, puzzle):
        self.variables = variables  
        self.domains = domains  
        self.constraints = constraints  
        self.puzzle = puzzle 
        self.solution = None

    def solve(self):
        return self.backtrack({})


    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            if self.is_valid_solution(assignment):
                return assignment
            return None

        var = self.select_unassigned_variable(assignment)

        for value in self.domains[var]:
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]  # if no solution is found
        return None

    def select_unassigned_variable(self, assignment):
        unassigned_vars = [var for var in self.variables if var not in assignment]

        return unassigned_vars[0]

    def is_consistent(self, var, value, assignment):
        return all(assignment.get(neighbor) != value for neighbor in self.constraints[var])

    def is_valid_solution(self, assignment):
        puzzle = self.puzzle

        for var in assignment:
            puzzle = puzzle.replace(var, str(assignment[var]))

        left_side, right_side = puzzle.split('=')

        try:
            return eval(left_side) == eval(right_side)
        except:
            return False


# the puzzle:
puzzle = "SEND + MORE = MONEY"
variables = list(set(re.findall(r'[A-Z]', puzzle)))  # Extract unique letters from the puzzle

domains = {var: list(range(10)) for var in variables}

# Prevents first letter from having 0 assigned to them
l = puzzle.split(' ')
for i in l:
        if i.isalpha():
                if 0 in domains[i[0]]:
                    domains[i[0]].remove(0)

# each variable taking a unique number
constraints = {var: [v for v in variables if v != var] for var in variables}
cryptarithmetic_csp = CSP(variables, domains, constraints, puzzle)

solution = cryptarithmetic_csp.solve()

if solution:
    print(f"Solution found: {solution}")
else:
    print("No valid solution found!")
