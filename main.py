# Ethan Philpott
# Project 2
# AI
# Dec 2021

import copy

# Reads lines from filename
def read_file(file_name):
    lines = []
    with open(file_name) as f:
        for line in f.readlines():
            # Remove newline character and then split line based on spaces
            line = line.strip()
            line = line.split(' ')
            # If blank line then we skip
            if line == ['']:
                continue
            # Add in line
            lines.append(line)
    return lines

# Stores data in a dictionary based on 2d list inputted
def store_data(lines):
    # Converts strings to ints in constraints 2d array
    for i in range(3, len(lines)):
        for j in range(0, len(lines[i])):
            lines[i][j] = int(lines[i][j])
    
    # Stores data in dictionary and returns it
    return {
        'assignments': [copy.deepcopy(lines[2]) for i in range(0, int(lines[0][0]))],
        'constraints': lines[3:]
    }

def mrv(assignments):
    # Holds the max MRV value found
    max = len(assignments[0])
    # Holds the index of the max MRV values found
    max_items = [0]
    # Search for max items
    for i in range(1, len(assignments)):
        item = assignments[i]
        if len(item) > max:
            max = len(item)
            max_items = [i]
        elif len(item) == max:
            max_items.append(i)
    return max_items

def degree(assignments, constraints, variables):
    # Holds the max degree and list of the indexes of the max degree items
    max = 0
    max_items = []
    # Go through variables
    for var in variables:
        degree = 0
        # Go through constraints
        row = constraints[var]
        for i in range(0, len(row)):
            # If we have a 1 and the item it relates to isn't assigned then we increment degree
            if row[i] == 1 and len(assignments[i]) != 1:
                degree += 1
        # Update max if necessary and append
        if degree > max:
            max = degree
            max_items = [var]
        elif degree == max:
            max_items.append(var)

    return max_items

# Checks if we can assign a given color
def checkNeighbors(assignments, constraints, var, domain):
    # Go through constraints
    row = constraints[var]
    for i in range(0, len(row)):
        if row[i] == 1 and len(assignments[i]) == 1:
            if assignments[i][0] == domain:
                return False
    return True

def inference(assignments, constraints, var, domain):
    # Go through constraints
    row = constraints[var]
    for i in range(0, len(row)):
        if row[i] == 1 and domain in assignments[i]:
            assignments[i].remove(domain)
            if len(assignments[i]) == 0:
                return None
    return assignments

def backtrack(constraints, assignments):
    # Check if we are done
    done = True
    for elem in assignments:
        if len(elem) > 1:
            done = False
        elif len(elem) == 0:
            # We have an empty assignment so we return failure
            return None
    if done:
        return assignments
    
    # Get variables
    variables = mrv(assignments)
    variables = degree(assignments, constraints, variables)
    
    # If we have no variables then we failed
    if variables == []:
        return None

    # Select variable
    variable = variables[0]

    # TODO Check how to do deepcopy to prevent issues here
    for domain in assignments[variable]:
        # Check if we can assign the domain to the variable
        if checkNeighbors(assignments, constraints, variable, domain):
            # Keep a copy of old domain in case we fail
            old_assignments = copy.deepcopy(assignments)
            # Assign domain to variable
            assignments[variable] = [domain]
            inferences = inference(assignments, constraints, variable, domain)
            if inferences != None:
                # Recurse
                assignments = inferences
                assignments = backtrack(constraints, assignments)
                if assignments != None:
                    return assignments
        # If we failed then we unassign everything
        assignments = old_assignments
    # Return failure
    return None

def test(val, assign):
    if val:
        old = copy.deepcopy(assign)
        assign[0] = ['R', 'G', 'B']
        test(False, assign)
        print(assign)
        assign = old
        return assign
    else:
        old = copy.deepcopy(assign)
        assign[0] = ['A', 'B', 'C']
        print(assign)
        assign = old
        return None

def main():
    # Get filename
    file_name = str(input('Enter the filename: ')).strip()

    # Get data
    lines = read_file(file_name)
    data = store_data(lines)

    result = backtrack(data['constraints'], data['assignments'])
    print(result)

    test(True, [['T', 'F', 'F']])

if __name__ == "__main__":
    main()