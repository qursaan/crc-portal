#from types import StringTypes
#try:
#    set
#except NameError:
#    from sets import Set
#    set = Set

import time
import datetime # Jordan
#from manifold.util.parameter import Parameter, Mixed, python_type
from manifold.util.predicate import Predicate, eq
#from itertools               import ifilter

class Filter(set):
    """
    A filter is a set of predicates
    """

    #def __init__(self, s=()):
    #    super(Filter, self).__init__(s)

    @staticmethod
    def from_list(l):
        f = Filter()
        try:
            for element in l:
                f.add(Predicate(*element))
        except Exception as e:
            print ("Error in setting Filter from list", e)
            return None
        return f

    @staticmethod
    def from_dict(d):
        f = Filter()
        for key, value in d.items():
            if key[0] in Predicate.operators.keys():
                f.add(Predicate(key[1:], key[0], value))
            else:
                f.add(Predicate(key, '=', value))
        return f

    def to_list(self):
        ret = []
        for predicate in self:
            ret.append(predicate.to_list())
        return ret


    @staticmethod
    def from_clause(clause):
        """
        NOTE: We can only handle simple clauses formed of AND fields.
        """
        raise Exception("Not implemented")

    def filter_by(self, predicate):
        self.add(predicate)
        return self

    def __str__(self):
        return ' AND '.join([str(pred) for pred in self])

    def __repr__(self):
        return '<Filter: %s>' % ' AND '.join([str(pred) for pred in self])

    def __key(self):
        return tuple([hash(pred) for pred in self])

    def __hash__(self):
        return hash(self.__key())

    def __additem__(self, value):
        if value.__class__ != Predicate:
            raise TypeError("Element of class Predicate expected, received %s" % value.__class__.__name__)
        set.__additem__(self, value)

    def keys(self):
        return set([x.key for x in self])

    # XXX THESE FUNCTIONS SHOULD ACCEPT MULTIPLE FIELD NAMES

    def has(self, key):
        for x in self:
            if x.key == key:
                return True
        return False

    def has_op(self, key, op):
        for x in self:
            if x.key == key and x.op == op:
                return True
        return False

    def has_eq(self, key):
        return self.has_op(key, eq)

    def get(self, key):
        ret = []
        for x in self:
            if x.key == key:
                ret.append(x)
        return ret

    def delete(self, key):
        to_del = []
        for x in self:
            if x.key == key:
                to_del.append(x)
        for x in to_del:
            self.remove(x)

        #self = filter(lambda x: x.key != key, self)

    def get_op(self, key, op):
        if isinstance(op, (list, tuple, set)):
            for x in self:
                if x.key == key and x.op in op:
                    return x.value
        else:
            for x in self:
                if x.key == key and x.op == op:
                    return x.value
        return None

    def get_eq(self, key):
        return self.get_op(key, eq)

    def set_op(self, key, op, value):
        for x in self:
            if x.key == key and x.op == op:
                x.value = value
                return
        raise KeyError(key)

    def set_eq(self, key, value):
        return self.set_op(key, eq, value)

    def get_predicates(self, key):
        # XXX Would deserve returning a filter (cf usage in SFA gateway)
        ret = []
        for x in self:
            if x.key == key:
                ret.append(x)
        return ret

#    def filter(self, dic):
#        # We go through every filter sequentially
#        for predicate in self:
#            print "predicate", predicate
#            dic = predicate.filter(dic)
#        return dic

    def match(self, dic, ignore_missing=True):
        for predicate in self:
            if not predicate.match(dic, ignore_missing):
                return False
        return True

    def filter(self, l):
        output = []
        for x in l:
            if self.match(x):
                output.append(x)
        return output

    def get_field_names(self):
        field_names = set()
        for predicate in self:
            field_names |= predicate.get_field_names()
        return field_names

#class OldFilter(Parameter, dict):
#    """
#    A type of parameter that represents a filter on one or more
#    columns of a database table.
#    Special features provide support for negation, upper and lower bounds,
#    as well as sorting and clipping.
#
#
#    fields should be a dictionary of field names and types.
#    As of PLCAPI-4.3-26, we provide support for filtering on
#    sequence types as well, with the special '&' and '|' modifiers.
#    example : fields = {'node_id': Parameter(int, "Node identifier"),
#                        'hostname': Parameter(int, "Fully qualified hostname", max = 255),
#                        ...}
#
#
#    filter should be a dictionary of field names and values
#    representing  the criteria for filtering.
#    example : filter = { 'hostname' : '*.edu' , site_id : [34,54] }
#    Whether the filter represents an intersection (AND) or a union (OR)
#    of these criteria is determined by the join_with argument
#    provided to the sql method below
#
#    Special features:
#
#    * a field starting with '&' or '|' should refer to a sequence type
#      the semantic is then that the object value (expected to be a list)
#      should contain all (&) or any (|) value specified in the corresponding
#      filter value. See other examples below.
#    example : filter = { '|role_ids' : [ 20, 40 ] }
#    example : filter = { '|roles' : ['tech', 'pi'] }
#    example : filter = { '&roles' : ['admin', 'tech'] }
#    example : filter = { '&roles' : 'tech' }
#
#    * a field starting with the ~ character means negation.
#    example :  filter = { '~peer_id' : None }
#
#    * a field starting with < [  ] or > means lower than or greater than
#      < > uses strict comparison
#      [ ] is for using <= or >= instead
#    example :  filter = { ']event_id' : 2305 }
#    example :  filter = { '>time' : 1178531418 }
#      in this example the integer value denotes a unix timestamp
#
#    * if a value is a sequence type, then it should represent
#      a list of possible values for that field
#    example : filter = { 'node_id' : [12,34,56] }
#
#    * a (string) value containing either a * or a % character is
#      treated as a (sql) pattern; * are replaced with % that is the
#      SQL wildcard character.
#    example :  filter = { 'hostname' : '*.jp' }
#
#    * the filter's keys starting with '-' are special and relate to sorting and clipping
#    * '-SORT' : a field name, or an ordered list of field names that are used for sorting
#      these fields may start with + (default) or - for denoting increasing or decreasing order
#    example : filter = { '-SORT' : [ '+node_id', '-hostname' ] }
#    * '-OFFSET' : the number of first rows to be ommitted
#    * '-LIMIT' : the amount of rows to be returned
#    example : filter = { '-OFFSET' : 100, '-LIMIT':25}
#
#    Here are a few realistic examples
#
#    GetNodes ( { 'node_type' : 'regular' , 'hostname' : '*.edu' , '-SORT' : 'hostname' , '-OFFSET' : 30 , '-LIMIT' : 25 } )
#      would return regular (usual) nodes matching '*.edu' in alphabetical order from 31th to 55th
#
#    GetPersons ( { '|role_ids' : [ 20 , 40] } )
#      would return all persons that have either pi (20) or tech (40) roles
#
#    GetPersons ( { '&role_ids' : 10 } )
#    GetPersons ( { '&role_ids' : 10 } )
#    GetPersons ( { '|role_ids' : [ 10 ] } )
#    GetPersons ( { '|role_ids' : [ 10 ] } )
#      all 4 forms are equivalent and would return all admin users in the system
#    """
#
#    def __init__(self, fields = {}, filter = {}, doc = "Attribute filter"):
#        # Store the filter in our dict instance
#        dict.__init__(self, filter)
#
#        # Declare ourselves as a type of parameter that can take
#        # either a value or a list of values for each of the specified
#        # fields.
#        self.fields = dict ( [ ( field, Mixed (expected, [expected]))
#                                 for (field,expected) in fields.iteritems() ] )
#
#        # Null filter means no filter
#        Parameter.__init__(self, self.fields, doc = doc, nullok = True)
#
#    def sql(self, api, join_with = "AND"):
#        """
#        Returns a SQL conditional that represents this filter.
#        """
#
#        # So that we always return something
#        if join_with == "AND":
#            conditionals = ["True"]
#        elif join_with == "OR":
#            conditionals = ["False"]
#        else:
#            assert join_with in ("AND", "OR")
#
#        # init
#        sorts = []
#        clips = []
#
#        for field, value in self.iteritems():
#            # handle negation, numeric comparisons
#            # simple, 1-depth only mechanism
#
#            modifiers={'~' : False,
#                       '<' : False, '>' : False,
#                       '[' : False, ']' : False,
#                       '-' : False,
#                       '&' : False, '|' : False,
#                       '{': False ,
#                       }
#            def check_modifiers(field):
#                if field[0] in modifiers.keys():
#                    modifiers[field[0]] = True
#                    field = field[1:]
#                    return check_modifiers(field)
#                return field
#            field = check_modifiers(field)
#
#            # filter on fields
#            if not modifiers['-']:
#                if field not in self.fields:
#                    raise PLCInvalidArgument, "Invalid filter field '%s'" % field
#
#                # handling array fileds always as compound values
#                if modifiers['&'] or modifiers['|']:
#                    if not isinstance(value, (list, tuple, set)):
#                        value = [value,]
#
#                if isinstance(value, (list, tuple, set)):
#                    # handling filters like '~slice_id':[]
#                    # this should return true, as it's the opposite of 'slice_id':[] which is false
#                    # prior to this fix, 'slice_id':[] would have returned ``slice_id IN (NULL) '' which is unknown
#                    # so it worked by coincidence, but the negation '~slice_ids':[] would return false too
#                    if not value:
#                        if modifiers['&'] or modifiers['|']:
#                            operator = "="
#                            value = "'{}'"
#                        else:
#                            field=""
#                            operator=""
#                            value = "FALSE"
#                    else:
#                        value = map(str, map(api.db.quote, value))
#                        if modifiers['&']:
#                            operator = "@>"
#                            value = "ARRAY[%s]" % ", ".join(value)
#                        elif modifiers['|']:
#                            operator = "&&"
#                            value = "ARRAY[%s]" % ", ".join(value)
#                        else:
#                            operator = "IN"
#                            value = "(%s)" % ", ".join(value)
#                else:
#                    if value is None:
#                        operator = "IS"
#                        value = "NULL"
#                    elif isinstance(value, StringTypes) and \
#                            (value.find("*") > -1 or value.find("%") > -1):
#                        operator = "LIKE"
#                        # insert *** in pattern instead of either * or %
#                        # we dont use % as requests are likely to %-expansion later on
#                        # actual replacement to % done in PostgreSQL.py
#                        value = value.replace ('*','***')
#                        value = value.replace ('%','***')
#                        value = str(api.db.quote(value))
#                    else:
#                        operator = "="
#                        if modifiers['<']:
#                            operator='<'
#                        if modifiers['>']:
#                            operator='>'
#                        if modifiers['[']:
#                            operator='<='
#                        if modifiers[']']:
#                            operator='>='
#                        #else:
#                        #    value = str(api.db.quote(value))
#                        # jordan
#                        if isinstance(value, StringTypes) and value[-2:] != "()": # XXX
#                            value = str(api.db.quote(value))
#                        if isinstance(value, datetime.datetime):
#                            value = str(api.db.quote(str(value)))
#
#                #if prefix:
#                #    field = "%s.%s" % (prefix,field)
#                if field:
#                    clause = "\"%s\" %s %s" % (field, operator, value)
#                else:
#                    clause = "%s %s %s" % (field, operator, value)
#
#                if modifiers['~']:
#                    clause = " ( NOT %s ) " % (clause)
#
#                conditionals.append(clause)
#            # sorting and clipping
#            else:
#                if field not in ('SORT','OFFSET','LIMIT'):
#                    raise PLCInvalidArgument, "Invalid filter, unknown sort and clip field %r"%field
#                # sorting
#                if field == 'SORT':
#                    if not isinstance(value,(list,tuple,set)):
#                        value=[value]
#                    for field in value:
#                        order = 'ASC'
#                        if field[0] == '+':
#                            field = field[1:]
#                        elif field[0] == '-':
#                            field = field[1:]
#                            order = 'DESC'
#                        if field not in self.fields:
#                            raise PLCInvalidArgument, "Invalid field %r in SORT filter"%field
#                        sorts.append("%s %s"%(field,order))
#                # clipping
#                elif field == 'OFFSET':
#                    clips.append("OFFSET %d"%value)
#                # clipping continued
#                elif field == 'LIMIT' :
#                    clips.append("LIMIT %d"%value)
#
#        where_part = (" %s " % join_with).join(conditionals)
#        clip_part = ""
#        if sorts:
#            clip_part += " ORDER BY " + ",".join(sorts)
#        if clips:
#            clip_part += " " + " ".join(clips)
##       print 'where_part=',where_part,'clip_part',clip_part
#        return (where_part,clip_part)
#
