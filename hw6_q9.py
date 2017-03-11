from hw4standard import *
import random

# use freshvariables, unify, substitute

kb = [
        ['ostrich','sam'],
        ['canary','tweety'],
        [ ['bird','X'],['not',['ostrich','X']] ],
        [ ['bird','X'],['not',['canary','X']] ],
        [ ['fly','X'],['not',['bird','X']],['not',['normal','X']] ],
        [ ['not',['normal','X']],['not',['ostrich','X']] ],
        [ ['normal','X'],['not',['canary','X']] ],
        [ [['boy',['goo','X','Y']],['boy',['foo','X','Y']]] ]
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
        neq_query = negate(query)
        #Let the consequent set be the initial KB
        #add negation to the KB and see if it's derived false
        kb.append(neq_query)
        #foreach zip{clauseA : clauseB}:
        #       if clause_ is unit clause & resolved:
        #               if result not in consequence set:
        #                       add result
        #                       check if no more added and consequence set is {}
        
        while kb != []:
            indx = list(range(len(kb)))
            random.shuffle(indx)
            for rule1 in kb[indx[0]]:
                for rule2 in kb[indx[1]]:
                    if (rule1[0] == 'not') and (rule2[0] != 'not') and (unify(rule1[1:],rule2,{})):
                        new_lit = [kb[indx[0]].remove(rule1)]+[kb[indx[1]].remove(rule2)]
                        print(new_lit)
                        for old_lit in kb:
                            if sameclause(new_lit,old_lit):
                                kb.append(new_lit)
                                print(kb)
                    if (rule1[0] != 'not') and (rule2[0] == 'not') and (unify(rule1,rule2[1:],{})):
                        new_lit = [kb[indx[0]].remove(rule1)]+[kb[indx[1]].remove(rule2)]
                        print(new_lit)
                        for old_lit in kb:
                            if sameclause(new_lit,old_lit):
                                kb.append(new_lit)
                                print(kb)
        
            return True
        #return True if proved and print
        print("proved")
       
#query = ['fly','sam']
query = ['fly','tweety']
#query2 = ['boy','X']
prove(['fly','sam'],kb)
