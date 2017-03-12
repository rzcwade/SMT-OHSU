#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 09:57:27 2017

@author: Tristan
"""

from hw4standard import *
import random

# use freshvariables, unify, substitute

kb1 = [
        ['ostrich','sam'],
        ['canary','tweety'],
        [ ['bird','X'],['not',['ostrich','X']] ],
        [ ['bird','X'],['not',['canary','X']] ],
        [ ['fly','X'],['not',['bird','X']],['not',['normal','X']] ],
        [ ['not',['normal','X']],['not',['ostrich','X']] ],
        [ ['normal','X'],['not',['canary','X']] ],
        
     ]

kb2 = [ [['boy',['goo','X','Y']],['boy',['foo','X','Y']]] ]

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

def prove(query,kb):
    #negate literal
    queryNeg = negate(query)
    print("Negation of query %s" % prettyexpr(queryNeg))
    kb = kb + [[queryNeg]]
    
    while True:
        print("Looping through data")
        new = []
        for i in range(len(kb)):
            unitClause = kb[i]
            if len(unitClause) > 1:
                continue
            unitClause = freshvariables(unitClause)
            print(" Unit clause %s" % prettyCNF(unitClause))
            unitClauseNeg = negate(unitClause[0])
            for j in range(len(kb)):
                if i == j:
                    continue
                otherClause = kb[j]
                print(" Trying with %s" % prettyCNF(otherClause))
                for k in range(len(otherClause)):
                    otherClauseK = otherClause[k]
                    subs = {}
                    result = unify(unitClauseNeg,otherClauseK,subs)
                    if result == False:
                        continue
                    resolvent = otherClause[:k]+otherClause[k+1:]
                    resolvent = substitute(resolvent,subs)
                    different = 1
                    for a in kb + new:
                        if sameclause(a,resolvent):
                            different = 0
                            break
                    if different:
                        new.append(resolvent)
                        str = "  Adding %s via subs" % prettyCNF(resolvent)
                        for s in subs:
                            str += " %s/%s" % (s,prettyexpr(subs[s]))
                        print(str)
                    if len(resolvent) == 0:
                        print("Found false!")
                        return True
        if new == []:
            print("Unable to add any new resolvents.")
            return False
        kb = kb + new
        
prove(['fly','tweety'],kb1)