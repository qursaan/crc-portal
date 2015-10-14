#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Implements a clause
# - a "tree" (more precisely a predecessor map, typically computed thanks to a DFS) 
# - a set of needed fields (those queried by the user)
#
# Copyright (C) UPMC Paris Universitas
# Authors:
#   Jordan Augé       <jordan.auge@lip6.fr> 
#   Marc-Olivier Buob <marc-olivier.buob@lip6.fr>

import pyparsing as pp
import operator, re

from manifold.util.predicate import Predicate
from types                 import StringTypes

# XXX When to use Keyword vs. Regex vs. CaselessLiteral
# XXX capitalization ?

# Instead of CaselessLiteral, try using CaselessKeyword. Keywords are better
# choice for grammar keywords, since they inherently avoid mistaking the leading
# 'in' of 'inside' as the keyword 'in' in your grammar.


class Clause(object):

    def __new__(cls, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], StringTypes):
            return ClauseStringParser().parse(args[0])
        return super(Clause, cls).__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        if len(args) == 2:
            # unary
            self.operator = Predicate.operators[args[0]]
            self.operands = [args[1]]
        elif len(args) == 3:
            self.operator = Predicate.operators[args[1]]
            self.operands = [args[0], args[2]]
        else:
            raise Exception, "Clause can only be unary or binary"
                
    def opstr(self, operator):
        ops = [string for string, op in Predicate.operators.items() if op == operator]
        return ops[0] if ops else ''

    def __repr__(self):
        if len(self.operands) == 1:
            return "%s(%s)" % (self.operator, self.operands[0])
        else:
            return "(%s %s %s)" % (self.operands[0], self.opstr(self.operator), self.operands[1])

class ClauseStringParser(object):

    def __init__(self):
        """
        BNF HERE
        """

        #integer = pp.Word(nums)
        #floatNumber = pp.Regex(r'\d+(\.\d*)?([eE]\d+)?')
        point = pp.Literal( "." )
        e     = pp.CaselessLiteral( "E" )

        # Regex string representing the set of possible operators
        # Example : ">=|<=|!=|>|<|="
        OPERATOR_RX = '|'.join([re.sub('\|', '\|', o) for o in Predicate.operators.keys()])

        # predicate
        field = pp.Word(pp.alphanums + '_')
        operator = pp.Regex(OPERATOR_RX).setName("operator")
        value = pp.QuotedString('"') #| pp.Combine( pp.Word( "+-"+ pp.nums, pp.nums) + pp.Optional( point + pp.Optional( pp.Word( pp.nums ) ) ) + pp.Optional( e + pp.Word( "+-"+pp.nums, pp.nums ) ) )

        predicate = (field + operator + value).setParseAction(self.handlePredicate)

        # clause of predicates
        and_op = pp.CaselessLiteral("and") | pp.Keyword("&&")
        or_op  = pp.CaselessLiteral("or")  | pp.Keyword("||")
        not_op = pp.Keyword("!")

        predicate_precedence_list = [
            (not_op, 1, pp.opAssoc.RIGHT, lambda x: self.handleClause(*x)),
            (and_op, 2, pp.opAssoc.LEFT,  lambda x: self.handleClause(*x)),
            (or_op,  2, pp.opAssoc.LEFT,  lambda x: self.handleClause(*x))
        ]
        clause = pp.operatorPrecedence(predicate, predicate_precedence_list)

        self.bnf = clause

    def handlePredicate(self, args):
        return Predicate(*args)

    def handleClause(self, args):
        return Clause(*args)

    def parse(self, string):
        return self.bnf.parseString(string,parseAll=True)

if __name__ == "__main__":
    print ClauseStringParser().parse('country == "Europe" || ts > "01-01-2007" && country == "France"')
    print Clause('country == "Europe" || ts > "01-01-2007" && country == "France"')
