#No import statements.

MAX_CONSTANTS = 10
connectives = ["^", "v", ">"]
prop = ["p", "q", "r", "s"]
negated_prop = ["-p", "-q", "-r", "-s"]
var = ["x", "y", "z", "w"]
pred = ["P", "Q", "R", "S"]

def remove_character(fmla, index):
    if len(fmla) > index:
        fmla = fmla[0 : index : ] + fmla[index + 1 : : ]
    return fmla

def remove_negations(fmla):
    for index, char in enumerate(fmla):
        if char == '-':
            if fmla[index+1] in "-(pqrs":
                new_fmla = remove_character(fmla, index)
                return remove_negations(new_fmla)
            else:
                return 0
    return fmla

def remove_quant_and_pred(fmla):
    for index, char in enumerate(fmla):
        if char == 'E' or char == 'A':
            if fmla[index+1] in var:
                new_fmla = remove_character(remove_character(fmla,index), index)
                new_fmla = new_fmla[0:index] + "-" + new_fmla[index:]
                return remove_quant_and_pred(new_fmla)
            else:
                return 0
        if char in pred:
            if fmla[index+1] == '(' and fmla[index+2] in var and fmla[index+3] == ',' and fmla[index+4] in var and fmla[index+5] == ')':
                new_fmla = remove_character(remove_character(remove_character(remove_character(remove_character(remove_character(fmla,index),index),index),index),index),index)
                new_fmla = new_fmla[0:index] + "p" + new_fmla[index:]
                return remove_quant_and_pred(new_fmla)
    return fmla


#this method also checks for balanced brackets
def split_fmla(fmla):
    stack = []
    main_connective = None
    lhs = None
    rhs = None
    for index, char in enumerate(fmla):
        if char == '(':
            stack.append(char)
        elif char == ')':
            if(len(stack) > 0):    
                stack.pop()
        elif char in connectives and len(stack) == 1 and main_connective == None:
            main_connective = char
            lhs = fmla[1:index]
            rhs = fmla[index+1: len(fmla)-1]
        elif char in connectives and len(stack) == 1 and main_connective != None:
            return False
    if len(stack) == 0 and main_connective != None:
        return (lhs,rhs,main_connective)
    else:
        return False

def check_possible(fmla):
    if fmla in prop:
        return True
    elif fmla[0] == '-':
        return check_possible(fmla[1:])
    elif fmla[0] == '(':
        if split_fmla != False:
            return check_possible(split_fmla(fmla)[1] and split_fmla(fmla)[0])
        else:
            return False
    else:
        return False

def check_possible_fol(fmla):
    if fmla in prop:
        return True
    elif fmla[0] == '-':
        return check_possible_fol(fmla[1:])
    elif fmla[0] == '(':
        if split_fmla(fmla) != False:
            return check_possible_fol(split_fmla(fmla)[1] and split_fmla(fmla)[0])
        else:
            return False
    elif fmla[0] == 'E' or fmla[0] == 'A':
        if fmla[1] in var:
            return check_possible_fol(fmla[2:])
        else:
            return False
    elif fmla[0] in pred:
        if fmla[1] == '(' and fmla[2] in var and fmla[3] == ',' and fmla[4] in var and fmla[5] == ')' and len(fmla) == 6:
            return True
        else: 
            return False
    else:
        return False

def parse_prop(fmla):
    # type_of_formula = None # 0 not valid; 1 proposition; 2 binary connective formula; 3 negation of formula

    if fmla in prop:
        return 6 
    elif fmla[0] == '(':
        # now we determine the middle connective, rhs and lhs
        if split_fmla(fmla) == False:
            return 0
        else:            
            lhs = split_fmla(fmla)[0]
            rhs = split_fmla(fmla)[1]
        
        if check_possible(lhs) == True and check_possible(rhs) == True:
            return 8
        else:
            return 0
    elif fmla[0] == '-':
        if check_possible(fmla[1:]) == True:
            return 7
        else:
            return 0
    else:
        return 0

def parse_fol(fmla):
    if fmla[0] in pred:
        if fmla[1] == '(' and fmla[2] in var and fmla[3] == ',' and fmla[4] in var and fmla[5] == ')' and len(fmla) == 6:
            return 1
        else:
            return 0
    elif fmla[0] == '-':
        if check_possible_fol(fmla[1:]) == True:
            return 2
        else:
            return 0
    elif fmla[0] == 'E':
        if fmla[1] in var:
            if check_possible_fol(fmla[2:]) == True:
                return 4
            else:
                return 0
        else:
            return 0
    elif fmla[0] == 'A':
        if fmla[1] in var:
            if check_possible_fol(fmla[2:]) == True:
                return 3
            else:
                return 0
        else:
            return 0
    elif fmla[0] == '(':
        new_fmla = remove_quant_and_pred(fmla)
        if new_fmla != 0 and split_fmla(new_fmla) != False:
            right = rhs(new_fmla)
            left = lhs(new_fmla)
        else:
            return 0

        if check_possible_fol(left) == True and check_possible_fol(right) == True:
            return 5
        else:
            return 0

def expanded(theory):
    for x in theory:
        if x in prop or x in negated_prop:
            continue
        else:
            return False
    return True

def contradictory(theory):
    for x in theory:
        if x in prop:
            if ("-" + x) in theory:
                return True
    return False 

def replace(theory, fmla):
   theory.remove(fmla)
   theory.add(negate(fmla))
   return theory

def negate(fmla):
    if fmla in prop:
        return "-" + fmla
    if fmla in negated_prop:
        return fmla[1]
    if parse(fmla) == 7:
        return negate(fmla[1:])
    if parse(fmla) == 8:
        right = rhs(fmla)
        left = lhs(fmla)
        connector = con(fmla)

        if connector == '^':
            return "(" + negate(left) + "v" + negate(right) + ")"
        if connector == 'v':
            return "(" + negate(left) + "^" + negate(right) + ")"
        if connector == '>':
            return "(" + left + '^' + negate(right) + ")"

# Parse a formula, consult parseOutputs for return values.
def parse(fmla):
    if parse_prop(fmla) == 0:
        return parse_fol(fmla)
    return parse_prop(fmla)

# Return the LHS of a binary connective formula
def lhs(fmla):
    return split_fmla(fmla)[0]

# Return the connective symbol of a binary connective formula
def con(fmla):
    return split_fmla(fmla)[2]

# Return the RHS symbol of a binary connective formula
def rhs(fmla):
    return split_fmla(fmla)[1]

# You may choose to represent a theory as a set or a list
def theory(fmla):#initialise a theory with a single formula in it
    tableau = [{fmla}] #singleton, treat this list as queue
    while len(tableau) != 0:
        theory = tableau.pop(0)
        if expanded(theory) and not contradictory(theory):
            return 1
        else:
            new_theory = theory.copy()
            for my_fmla in theory:
                if my_fmla not in prop and my_fmla not in negated_prop:
                    case = parse(my_fmla)
                    if case == 7:
                        new_theory = replace(new_theory, my_fmla)
            theorycopy = new_theory.copy()
            for my_fmla in theorycopy:
                if my_fmla not in prop and my_fmla not in negated_prop:
                    case = parse(my_fmla)
                    if case == 8:
                        right = rhs(my_fmla)
                        left = lhs(my_fmla)
                        connector = con(fmla)

                        if connector == '^':
                                new_theory.add(left)
                                new_theory.add(right)
                                if not contradictory(new_theory) and new_theory not in tableau:
                                    tableau.append(new_theory)
                        if connector == 'v':
                            theory1 = new_theory.add(left)
                            theory2 = new_theory.add(right)

                            if theory1 not in tableau and not contradictory(theory1):
                                tableau.append(theory1)
                            if theory2 not in tableau and not contradictory(theory2):
                                tableau.append(theory2)
            
    return 0

#check for satisfiability
def sat(tableau):
#output 0 if not satisfiable, output 1 if satisfiable, output 2 if number of constants exceeds MAX_CONSTANTS
    if tableau == [0]:
        return 0
    if tableau == [1]:
        return 1

#DO NOT MODIFY THE CODE BELOW
f = open('input.txt')

parseOutputs = ['not a formula',
                'an atom',
                'a negation of a first order logic formula',
                'a universally quantified formula',
                'an existentially quantified formula',
                'a binary connective first order formula',
                'a proposition',
                'a negation of a propositional formula',
                'a binary connective propositional formula']

satOutput = ['is not satisfiable', 'is satisfiable', 'may or may not be satisfiable']



firstline = f.readline()

PARSE = False
if 'PARSE' in firstline:
    PARSE = True

SAT = False
if 'SAT' in firstline:
    SAT = True

for line in f:
    if line[-1] == '\n':
        line = line[:-1]
    parsed = parse(line)

    if PARSE:
        output = "%s is %s." % (line, parseOutputs[parsed])
        if parsed in [5,8]:
            output += " Its left hand side is %s, its connective is %s, and its right hand side is %s." % (lhs(line), con(line) ,rhs(line))
        print(output)

    if SAT:
        if parsed:
            tableau = [theory(line)]
            print('%s %s.' % (line, satOutput[sat(tableau)]))
        else:
            print('%s is not a formula.' % line)
