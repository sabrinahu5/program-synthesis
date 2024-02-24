from dataclasses import dataclass
@dataclass
class Constant:
    s: str

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

def execute(e):
    match e:
        case Constant(s):
            return s
        case Concatenate(e1, e2):
            return execute(e1) + execute(e2)
        case Left(e, i):
            s = execute(e)
            return s[:i]
        case Right(e, i):
            s = execute(e)
            return s[len(s)-i:]
        case Mid(e, i1, i2):
            s = execute(e)
            return s[i1:i1+i2]
        case Replace(e1, e2, i1, i2):
            s = execute(e1)
            r = execute(e2)
            return s[:i1] + r + s[i1+i2:]
        case Trim(e):
            s = execute(e)
            return s.strip()
        case Repeat(i1, i2):
            return i1 * i2
        case Substitute(e1, e2, e3):
            s1 = execute(e1)
            s2 = execute(e2)
            s3 = execute(e3)
            if s2 in s1:
                return s1.replace(s2, s3)
            else:
                print(s2 + " not in " + s1)
                return s1
        case SubstituteI(e1, e2, e3, i):
            s1 = execute(e1)
            s2 = execute(e2)
            s3 = execute(e3)
            return execute(s1).replace(s2, s3, i)
        case To_Text(i):
            return str(i)
        case Lower(e):
            s = execute(e)
            return s.lower()
        case Upper(e):
            s = execute(e)
            return s.upper()
        case Proper(e):
            s = execute(e)
            return s.title()
        case If(e1, e2, e3):
            return execute(e2) if execute(e1) else execute(e3)
        case Add(i1, i2):
            return i1 + i2
        case Minus(e1, e2):
            return i1 - i2
        case Divide(e1, e2):
            return i1 // i2
        case Find(e1, e2):
            s1 = execute(e1)
            s2 = execute(e2)
            return s2.find(s1)
        case FindI(e1, e2, i):
            s1 = execute(e1)
            s2 = execute(e2)
            return s2.find(s1, i)
        case Len(e):
            s = execute(e)
            return len(s)
        case Exact(e1, e2):
            s1 = execute(e1)
            s2 = execute(e2)
            return s1 == s2
        case Equals(i1, i2):
            return i1 == i2
        case GT(i1, i2):
            return i1 > i2
        case GE(i1, i2):
            return i1 >= i2
        case IsNumber(e):
            s = execute(e)
            return s.isnumeric()
        case Value(e):
            s = execute(e)
            return int(s)


e = Substitute(Constant("bello"), Constant("b"), Constant("c"))
print(execute(e))
