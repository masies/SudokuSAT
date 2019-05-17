from flask import Flask, render_template, request, url_for

import random, json, os, sys, getopt, time, pycosat, itertools

sol = []
base_scale = [1,2,3,4,5,6,7,8,9]

app = Flask(__name__, static_folder = os.path.abspath(os.path.dirname(sys.argv[0])))

@app.route('/')
def init():
    return render_template('index.html')

@app.route('/problem_submission', methods = ['POST'])
def get_problem_instance():
	global sol
	jsdata = request.form["javascript_data"]
	data = json.loads(jsdata)
	sol = solve_problem(data)
	return jsdata

@app.route('/solution_request')
def send_problem_solution():
    json_helper = {}
    json_helper['solution'] = sol
    json_object = json.dumps(json_helper)
    return json_object


def solve_problem(problemset):
    solve(problemset) 
    return problemset 
    
def generate_clause(row, col, digit): 
    return 81 * (row - 1) + 9 * (col - 1) + digit



#Reduces Sudoku problem to a SAT clauses 
def get_sat_clauses(): 
    clauses = []
    # clauses to be satisfied for all the cells:
    for row in base_scale:
        for col in base_scale:
            # each cell denotes at leat one digit (or nothing) (#1)
            # each clause will have the form
            # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            clauses.append([generate_clause(row, col, digit) for digit in base_scale])
            # each cell denotes at most one digit (none ) (#36)  
            # each clause will have the form
            # [-1, -2]
            # [-1, -3]
            # [-1, -4]
            # [-1, -5]
            # [-1, -6]
            # [-1, -7]
            # [-1, -8]
            # [-1, -9]
            #  ....
            for pair in itertools.combinations(base_scale, 2):
                clauses.append([-generate_clause(row, col, pair[0]), -generate_clause(row, col, pair[1])])

    # we have 37 * 81 clauses here = 2997
    # print('lenght = ',len(clauses))


    # ensure rows and columns have distinct values
    # basically here it will first create a structure for each cell with : list(itertools.product([row],base_scale))
    #    (n, 1) (n, 2) ... (n, 9) 
    # then extract all the pairs from this list where pair_0 < pair_1 with : list(itertools.combinations(list(itertools.product([row],base_scale)), 2))
    #  ((n, 1), (n, 2)), ((n, 1), (n, 3)),..., ((n, 1), (n, n)), ((n, 2), (n, 3)), ((n, 2), (n, 4)), ...,  ((n, n-1), (n, n))
    # at this point we have all the pairs of cell on the same row so we can generate the clause to ensure these two cell does not contains the same digit
    for row in base_scale:
        for pairs in list(itertools.combinations(list(itertools.product([row],base_scale)), 2)):
            for digit in base_scale:
                clauses.append([-generate_clause(pairs[0][0], pairs[0][1], digit), -generate_clause(pairs[1][0], pairs[1][1], digit)])

    # we have 36 (all combination) * 9 (number of columns) * 9 (number of digits) + 2997 (previous clauses) clauses here = 5913
    # print('lenght = ',len(clauses))
         
    # this is actually for cols but can be just incorporated in the previos for loop just inverting the indexes in the pair
    # but i guess it is enough crazy just like that so have some separation
    for col in base_scale:
        for pairs in list(itertools.combinations(list(itertools.product(base_scale,[col])), 2)):
            for digit in base_scale:
                clauses.append([-generate_clause(pairs[0][0], pairs[0][1], digit), -generate_clause(pairs[1][0], pairs[1][1], digit)])

    # just like before, another 2916 clauses, raising the total to =  8829
    # print('lenght = ',len(clauses))

        
    # check for 3x3 subregion of the graph (does the same as before intuitively but with grid of 3x3)
    for cell1 in 1, 4, 7:
        for cell2 in 1, 4 ,7:
            for pairs in list(itertools.combinations([(cell1 + k % 3, cell2 + k // 3) for k in range(9)], 2)):
                for digit in base_scale:
                    clauses.append([-generate_clause(pairs[0][0], pairs[0][1], digit), -generate_clause(pairs[1][0], pairs[1][1], digit)])
    # we have 9 square * 9 (number of digits) * 36 (number of pairs) + 8829 (previous clauses) clauses here = 11745
    # print('lenght = ',len(clauses))
    
    # the number final of clauses should be = 11745
    # 81 cell * 37 condition (part 1)  + (9 rows + 9 cols + 9 grid)  * (9 digits * 36 combination)
    assert len(clauses) == 81 * (1 + 36) + 27 * 324
    return clauses

def solve(grid):
    # generate sat clauses
    clauses = get_sat_clauses()
    # we must add the digits we already have in the board
    for row in base_scale:
        for col in base_scale:
            if grid[row - 1][col - 1]:
                clauses.append([generate_clause(row, col, grid[row - 1][col - 1])])
    
    # run the sat solver
    sol = set(pycosat.solve(clauses))
    
    # TODO :: here we can call the minisat solver http://minisat.se/
    # basically his format is 
    # p cnf 5 3
    # 1 -5 4 0
    # -1 5 3 4 0
    # -3 -4 0
    # where in the first row "p cnf 5 3" means that this is SAT problem in CNF format with 5 variables and 3 clauses. and 0 at the end of each line means end of line

    # our format instead is just
    # [[1, -5, 4], [-1, 5, 3, 4], [-3, -4]]

    # you can invoke minsat with shell command "minisat [options] [INPUT-FILE [RESULT-OUTPUT-FILE]]"

    # basically we just need to generate a file writing all our clauses plus the first line and we are done


    # update the board
    for row in base_scale:
        for col in base_scale:
            for digit in base_scale:
                if generate_clause(row, col, digit) in sol:
                    grid[row - 1][col - 1] = digit
            
    


if __name__ == '__main__':
    app.run(debug=True)
