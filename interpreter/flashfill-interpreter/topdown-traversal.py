from dataclasses import dataclass
import heapq

class Incomplete(Exception):
    pass

@dataclass
class Input:
    x: str

@dataclass
class Hole:
    e: object = None

@dataclass
class First:
    e: object

@dataclass
class Rest:
    e: object

Expression = Input | Hole | First | Rest

def execute(e, env):
    match e:
        case Input(x):
            return env[x]
        case Hole(e):
            raise Incomplete()
        case First(e):
            s = execute(e, env)
            if s == '':
                return s
            return s[0]
        case Rest(e):
            s = execute(e, env)
            if s == '':
                return s
            return s[1:]
        
def types():
    return {
        'First': (First, ('str', ('exp'))),
        'Rest': (Rest, ('str', ('exp'))),
    }

# Basic tests

env = {'x': 'baby'}
env2 = {'x': 'bell'}
e = First(Rest(Input('x')))
e1 = First(Input('x'))
"""
print(execute(e, env))
print(execute(e1, env))
"""

# Input: program, io examples, Output: score
# -1: not incomplete but not passing
# 0: incomplete (when catch exception)
# 1: passing
# score: sum/total (if sum is only of 1, -1 => -1)

def score_program(program, io_examples):
    total_score = 0
    for example in io_examples:
        input_data, expected_output = example
        env = {'x': input_data}
        try:
            output = execute(program, env)
            if output == expected_output:
                total_score += 1       
            else:
                return -1    
        except Incomplete:
            total_score += 0    
    if io_examples:
        return total_score / len(io_examples)
    else:
        return 0
    

# Testing scoring function 
e2 = First(Hole(Input('x')))
e3 = Rest(Input('x'))

io_examples_e2 = [
    ('hello', 'h'),  
    ('world', 'w'),  
    ('test', 'e'),   
]

io_examples_e3 = [
    ('hello', 'ello'), 
    ('world', 'orld'), 
    ('test', 'est'),  
]

"""
print("Score for e2: " + str(score_program(e2, io_examples_e2)))  
print("Score for e3: " + str(score_program(e3, io_examples_e3)))  
"""


def top_down_traversal(program, io_examples):
    pq = []  # Priority queue to hold (score, program) tuples
    counter = 0 # For same score 
    heapq.heappush(pq, (0, counter, program))  # Initialize with the original program and a default high score

    while pq:
        current_score, _, current_program = heapq.heappop(pq)
        if current_score == 1:
            return current_program  # Return immediately if a perfect score is found
        
        filled_programs = fill_hole(current_program)
        for filled_program in filled_programs:
            score = score_program(filled_program, io_examples)
            print(filled_program)
            print("SCORE: " + str(score))
            counter += 1
            if score == 1:
                return filled_program  # Return immediately if a perfect score is found
            heapq.heappush(pq, (score, counter, filled_program))  # Use score directly because we want the highest score at the top

# Checks if program contains any holes (not used)
def has_hole(program):
    if isinstance(program, Hole):
        return True
    elif isinstance(program, Input):
        return False
    elif isinstance(program, First) or isinstance(program, Rest):
        return has_hole(program.e)
    return False

# Input: program with holes 
# Ouput: list of programs with holes filled 
def fill_hole(program):
    if isinstance(program, Hole):
        return [First(program.e), Rest(program.e)]
    elif hasattr(program, 'e'):
        filled_subprograms = fill_hole(program.e)
        filled_programs = []
        for subprogram in filled_subprograms:
            if isinstance(program, First):
                filled_programs.append(First(subprogram))
            elif isinstance(program, Rest):
                filled_programs.append(Rest(subprogram))
        return filled_programs
    return []

"""
e3 = Hole(Rest(Hole(Input('x'))))
print(has_hole(e3))
print(fill_hole(e3))

e4 = Rest(Input('x'))
print(has_hole(e4))
"""

io_examples = [
    ('hello', 'l'),
    ('baby', 'b'),
    ('yesterday', 's'),
]

e5 = First(Hole(Hole(Input('x'))))
print(top_down_traversal(e5, io_examples))