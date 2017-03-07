from hw4standard import *

# use freshvariables, unify, substitute

kb = [
        ['ostrich','sam'],
        ['canary','tweety'],
        [ ['bird','X'],['ostrich','X'] ],
        [ ['bird','X'],['canary','X'] ],
        [ ['fly','X'],['bird','X'],['normal','X'] ],
        [ ['not',['normal','X']],['ostrich','X'] ],
        [ ['normal','X'],['canary','X'] ],
     ]

def sameclause(a,b):
        avars = findvariables(a,[])
        bvars = findvariables(b,[])
        subs = {}
        for av, bv in zip(avars, bvars):
                subs[av] = bv
        newa = substitute(a, subs)
        if newa == b:
                return True
        return False

def negate(literal):
        if type(literal) is list:
                if literal[0] == "not":
                        return literal[1]
        return ['not',literal]

def prettyCNF(cnf):
        connector = ""
        str = ""
        if cnf == []:
                return "False"
        for x in cnf:
                str += connector
                str += prettyexpr(x)
                connector = " v "
        return str


        