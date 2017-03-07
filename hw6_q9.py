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
        #determines if two clauses are the same (-variable renameing)
        #used to make sure you do not add a clause that already have
        #that just happens to use different variables.
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
        #take a literal and negate it
        #use this to convert initial query and as part of resolution rule
        if type(literal) is list:
                if literal[0] == "not":
                        return literal[1]
        return ['not',literal]

def prettyCNF(cnf):
        #prints a clause that is a disjunction
        connector = ""
        str = ""
        if cnf == []:
                return "False"
        for x in cnf:
                str += connector
                str += prettyexpr(x)
                connector = " v "
        return str

def prove(query, kb):
        #take a query(a positive and negative literal) and a KB,
        #determine if KB |= query
        
        #Let the consequent set be the initial KB
        
        #add negation to the KB and see if it's derived false
        
        #foreach zip{clauseA : clauseB}:
        #       if clause_ is unit clause & resolved:
        #               if result not in consequence set:
        #                       add result
        #                       check if no more added and consequence set is {}
        #return True if proved and print
        return False
        