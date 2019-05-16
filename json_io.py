from flask import Flask, render_template, request, url_for

import random, json, os, sys, getopt, time, pycosat

sol = []

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
    
def v(i, j, d): 
    return 81 * (i - 1) + 9 * (j - 1) + d

#Reduces Sudoku problem to a SAT clauses 
def sudoku_clauses(): 
    res = []
    # for all cells, ensure that the each cell:
    for i in range(1, 10):
        for j in range(1, 10):
            # denotes (at least) one of the 9 digits (1 clause)
            res.append([v(i, j, d) for d in range(1, 10)])
            # does not denote two different digits at once (36 clauses)
            for d in range(1, 10):
                for dp in range(d + 1, 10):
                    res.append([-v(i, j, d), -v(i, j, dp)])

    def valid(cells): 
        for i, xi in enumerate(cells):
            for j, xj in enumerate(cells):
                if i < j:
                    for d in range(1, 10):
                        res.append([-v(xi[0], xi[1], d), -v(xj[0], xj[1], d)])

    # ensure rows and columns have distinct values
    for i in range(1, 10):
        valid([(i, j) for j in range(1, 10)])
        valid([(j, i) for j in range(1, 10)])
        
    # ensure 3x3 sub-grids "regions" have distinct values
    for i in 1, 4, 7:
        for j in 1, 4 ,7:
            valid([(i + k % 3, j + k // 3) for k in range(9)])
      
    assert len(res) == 81 * (1 + 36) + 27 * 324
    return res

def solve(grid):
    #solve a Sudoku problem
    clauses = sudoku_clauses()
    for i in range(1, 10):
        for j in range(1, 10):
            d = grid[i - 1][j - 1]
            # For each digit already known, a clause (with one literal). 
            if d:
                clauses.append([v(i, j, d)])
    
    # Print number SAT clause  
    numclause = len(clauses)
    print ("P CNF " + str(numclause) +"(number of clauses)")
    
    # solve the SAT problem
    start = time.time()
    sol = set(pycosat.solve(clauses))
    end = time.time()
    print("Time: "+str(end - start))
    
    def read_cell(i, j):
        # return the digit of cell i, j according to the solution
        for d in range(1, 10):
            if v(i, j, d) in sol:
                return d

    for i in range(1, 10):
        for j in range(1, 10):
            grid[i - 1][j - 1] = read_cell(i, j)


if __name__ == '__main__':
    app.run(debug=True)
