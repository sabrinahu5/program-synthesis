from dataclasses import dataclass

class Incomplete(Exception):
    pass

@dataclass
class Input:
    x: str

@dataclass
class Constant:
    s: str

@dataclass
class Hole:
    pass

@dataclass
class Concatenate:
    e1: object
    e2: object

@dataclass
class Left:
    e: object
    i: int

@dataclass
class Right:
    e: object
    i: int

@dataclass
class Mid:
    e: object
    i1: int
    i2: int

@dataclass
class Replace:
    e1: object
    e2: object
    i1: int
    i2: int

@dataclass
class Trim:
    e: object

@dataclass
class Repeat:
    i1: int
    i2: int

@dataclass
class Substitute:
    e1: object
    e2: object
    e3: object

@dataclass
class SubstituteI:
    e1: object
    e2: object
    e3: object
    i: int

@dataclass
class To_Text:
    i: int

@dataclass
class Lower:
    e: object

@dataclass
class Upper:
    e: object

@dataclass
class Proper:
    e: object

@dataclass
class If:
    e1: object
    e2: object
    e3: object

@dataclass
class Add:
    i1: int
    i2: int

@dataclass
class Minus:
    i1: int
    i2: int

@dataclass
class Divide:
    i1: int
    i2: int

@dataclass
class Find:
    e1: object
    e2: object

@dataclass
class FindI:
    e1: object
    e2: object
    i: int

@dataclass
class Len:
    e: object

@dataclass
class Exact:
    e1: object
    e2: object

@dataclass
class Equals:
    i1: int
    i2: int

@dataclass
class GT:
    i1: int
    i2: int

@dataclass
class GE:
    i1: int
    i2: int

@dataclass
class IsNumber:
    e: object

@dataclass
class Value:
    e: object

Expression = Concatenate | Left | Right | Repeat | Substitute | SubstituteI | To_Text | Lower | Upper | Proper | If | Add | Minus | Divide | Find | FindI | Len | Exact | Equals | GT | GE | IsNumber | Value

def execute(e, env):
    match e:
        case Input(x):
            return env[x]
        case Constant(s):
            return s
        case Hole():
            raise Incomplete()
        case Concatenate(e1, e2):
            return execute(e1, env) + execute(e, env)
        case Left(e, i):
            s = execute(e, env)
            return s[:i]
        case Right(e, i):
            s = execute(e, env)
            return s[len(s)-i:]
        case Mid(e, i1, i2):
            s = execute(e)
            return s[i1:i1+i2]
        case Replace(e1, e2, i1, i2):
            s = execute(e1, env)
            r = execute(e2, env)
            return s[:i1] + r + s[i1+i2:]
        case Trim(e):
            s = execute(e, env)
            return s.strip()
        case Repeat(i1, i2):
            return i1 * i2
        case Substitute(e1, e2, e3):
            s1 = execute(e1, env)
            s2 = execute(e2, env)
            s3 = execute(e3, env)
            if s2 in s1:
                return s1.replace(s2, s3)
            else:
                print(s2 + " not in " + s1)
                return s1
        case SubstituteI(e1, e2, e3, i):
            s1 = execute(e1, env)
            s2 = execute(e2, env)
            s3 = execute(e3, env)
            return s1.replace(s2, s3, i)
        case To_Text(i):
            return str(i)
        case Lower(e):
            s = execute(e, env)
            return s.lower()
        case Upper(e):
            s = execute(e, env)
            return s.upper()
        case Proper(e):
            s = execute(e, env)
            return s.title()
        case If(e1, e2, e3):
            return execute(e2, env) if execute(e1, env) else execute(e3, env)
        case Add(i1, i2):
            return i1 + i2
        case Minus(i1, i2):
            return i1 - i2
        case Divide(i1, i2):
            return i1 // i2
        case Find(e1, e2):
            s1 = execute(e1, env)
            s2 = execute(e2, env)
            return s2.find(s1)
        case FindI(e1, e2, i):
            s1 = execute(e1, env)
            s2 = execute(e2, env)
            return s2.find(s1, i)
        case Len(e):
            s = execute(e, env)
            return len(s)
        case Exact(e1, e2):
            s1 = execute(e1, env)
            s2 = execute(e2, env)
            return s1 == s2
        case Equals(i1, i2):
            return i1 == i2
        case GT(i1, i2):
            return i1 > i2
        case GE(i1, i2):
            return i1 >= i2
        case IsNumber(e):
            s = execute(e, env)
            return s.isnumeric()
        case Value(e):
            s = execute(e, env)
            return int(s)


def types():
    return {
        'Constant': (Constant, ('str', ('str'))),
        'Concatenate': (Concatenate, ('str', ('exp', 'exp'))),
        'Left': (Left, ('str', ('exp', 'int'))),
        'Right': (Right, ('str', ('exp', 'int'))),
    }

# Change representation of hole

"""
env = {'x': 'baby'}
env2 = {'x': 'bell'}
e = Substitute(Constant("bello"), Constant("b"), Constant("c"))
e1 = Substitute(Input('x'), Constant("b"), Constant("c"))
print(execute(e1, env))
print(execute(e1, env2))
print(execute(e, env))

io_examples = [('bello', 'cello'), ('cab', 'cac'), ('boba', 'coca')]
for (x, r) in io_examples:
    env = {'x': x}
    o = execute(e1, env)
    print(o)
    assert o == r

# execute(Hole(), env)
e2 = If(Input('x'), Constant('yes'), Hole())
io_examples = [('bello', 'yes'), ('', '')]
for (x, r) in io_examples:
    env = {'x': x}
    o = execute(e2, env)
    print(o)
    assert o == r
print(execute(e2, env))
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

e2 = If(Input('x'), Constant('yes'), Hole())
io_examples = [('bello', 'yes'), ('', ''), ('bello', 'no')]
print("Test 1: " + str(score_program(e2, io_examples)))

io_examples = [('bello', 'yes'), ('bello', 'no')]
print("Test 2: " + str(score_program(e2, io_examples)))

io_examples = [('bello', 'yes'), ('', '')]
print("Test 3: " + str(score_program(e2, io_examples)))

io_examples = [('bello', 'yes'), ('', ''), ('', 'no')]
print("Test 4: " + str(score_program(e2, io_examples)))

io_examples = [('bello', 'yes'), ('', ''), ('', 'no'), ('bello', 'no'), ('bello', 'no2')]
print("Test 5: " + str(score_program(e2, io_examples)))