#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Query representation
#
# Copyright (C) UPMC Paris Universitas
# Authors:
#   Jordan Augé         <jordan.auge@lip6.fr>
#   Marc-Olivier Buob   <marc-olivier.buob@lip6.fr>
#   Thierry Parmentelat <thierry.parmentelat@inria.fr>

from types                      import StringTypes
from manifold.core.filter       import Filter, Predicate
from manifold.util.frozendict   import frozendict
from manifold.util.type         import returns, accepts
from manifold.util.clause       import Clause
import copy

import json
import uuid

def uniqid (): 
    return uuid.uuid4().hex

debug=False
#debug=True

class ParameterError(StandardError): pass

class Query(object):
    """
    Implements a TopHat query.

    We assume this is a correct DAG specification.

    1/ A field designates several tables = OR specification.
    2/ The set of fields specifies a AND between OR clauses.
    """

    #--------------------------------------------------------------------------- 
    # Constructor
    #--------------------------------------------------------------------------- 

    def __init__(self, *args, **kwargs):

        self.query_uuid = uniqid()

        # Initialize optional parameters
        self.clear()
    
        #l = len(kwargs.keys())
        len_args = len(args)

        if len(args) == 1:
            if isinstance(args[0], dict):
                kwargs = args[0]
                args = []

        # Initialization from a tuple

        if len_args in range(2, 7) and type(args) == tuple:
            # Note: range(x,y) <=> [x, y[

            # XXX UGLY
            if len_args == 3:
                self.action = 'get'
                self.params = {}
                self.timestamp     = 'now'
                self.object, self.filters, self.fields = args
            elif len_args == 4:
                self.object, self.filters, self.params, self.fields = args
                self.action = 'get'
                self.timestamp     = 'now'
            else:
                self.action, self.object, self.filters, self.params, self.fields, self.timestamp = args

        # Initialization from a dict
        elif "object" in kwargs:
            if "action" in kwargs:
                self.action = kwargs["action"]
                del kwargs["action"]
            else:
                print "W: defaulting to get action"
                self.action = "get"


            self.object = kwargs["object"]
            del kwargs["object"]

            if "filters" in kwargs:
                self.filters = kwargs["filters"]
                del kwargs["filters"]
            else:
                self.filters = Filter()

            if "fields" in kwargs:
                self.fields = set(kwargs["fields"])
                del kwargs["fields"]
            else:
                self.fields = set()

            # "update table set x = 3" => params == set
            if "params" in kwargs:
                self.params = kwargs["params"]
                del kwargs["params"]
            else:
                self.params = {}

            if "timestamp" in kwargs:
                self.timestamp = kwargs["timestamp"]
                del kwargs["timestamp"]
            else:
                self.timestamp = "now" 

            if kwargs:
                raise ParameterError, "Invalid parameter(s) : %r" % kwargs.keys()
        #else:
        #        raise ParameterError, "No valid constructor found for %s : args = %r" % (self.__class__.__name__, args)

        self.sanitize()

    def sanitize(self):
        if not self.filters:   self.filters   = Filter()
        if not self.params:    self.params    = {}
        if not self.fields:    self.fields    = set()
        if not self.timestamp: self.timestamp = "now" 

        if isinstance(self.filters, list):
            f = self.filters
            self.filters = Filter()
            for x in f:
                pred = Predicate(x)
                self.filters.add(pred)
        elif isinstance(self.filters, Clause):
            self.filters = Filter.from_clause(self.filters)

        if isinstance(self.fields, list):
            self.fields = set(self.fields)

        for field in self.fields:
            if not isinstance(field, StringTypes):
                raise TypeError("Invalid field name %s (string expected, got %s)" % (field, type(field)))

    #--------------------------------------------------------------------------- 
    # Helpers
    #--------------------------------------------------------------------------- 

    def copy(self):
        return copy.deepcopy(self)

    def clear(self):
        self.action = 'get'
        self.object = None
        self.filters = Filter()
        self.params  = {}
        self.fields  = set()
        self.timestamp  = 'now' # ignored for now

    def to_sql(self, platform='', multiline=False):
        get_params_str = lambda : ', '.join(['%s = %r' % (k, v) for k, v in self.get_params().items()])
        get_select_str = lambda : ', '.join(self.get_select()) 

        table  = self.get_from()
        select = 'SELECT %s' % (get_select_str()    if self.get_select()    else '*')
        where  = 'WHERE %s'  % self.get_where()     if self.get_where()     else ''
        at     = 'AT %s'     % self.get_timestamp() if self.get_timestamp() else ''
        params = 'SET %s'    % get_params_str()     if self.get_params()    else ''

        sep = ' ' if not multiline else '\n  '
        if platform: platform = "%s:" % platform
        strmap = {
            'get'   : '%(select)s%(sep)s%(at)s%(sep)sFROM %(platform)s%(table)s%(sep)s%(where)s%(sep)s',                                           
            'update': 'UPDATE %(platform)s%(table)s%(sep)s%(params)s%(sep)s%(where)s%(sep)s%(select)s',       
            'create': 'INSERT INTO %(platform)s%(table)s%(sep)s%(params)s%(sep)s%(select)s',
            'delete': 'DELETE FROM %(platform)s%(table)s%(sep)s%(where)s'
        }

        return strmap[self.action] % locals()

    @returns(StringTypes)
    def __str__(self):
        return self.to_sql(multiline=True)

    @returns(StringTypes)
    def __repr__(self):
        return self.to_sql()

    def __key(self):
        return (self.action, self.object, self.filters, frozendict(self.params), frozenset(self.fields))

    def __hash__(self):
        return hash(self.__key())

    #--------------------------------------------------------------------------- 
    # Conversion
    #--------------------------------------------------------------------------- 

    def to_dict(self):
        return {
            'action': self.action,
            'object': self.object,
            'timestamp': self.timestamp,
            'filters': self.filters.to_list(),
            'params': self.params,
            'fields': list(self.fields)
        }

    def to_json (self, analyzed_query=None):
        query_uuid=self.query_uuid
        a=self.action
        o=self.object
        t=self.timestamp
        f=json.dumps (self.filters.to_list())
        p=json.dumps (self.params)
        c=json.dumps (list(self.fields))
        # xxx unique can be removed, but for now we pad the js structure
        unique=0

        if not analyzed_query:
            aq = 'null'
        else:
            aq = analyzed_query.to_json()
        sq="{}"
        
        result= """ new ManifoldQuery('%(a)s', '%(o)s', '%(t)s', %(f)s, %(p)s, %(c)s, %(unique)s, '%(query_uuid)s', %(aq)s, %(sq)s)"""%locals()
        if debug: print 'ManifoldQuery.to_json:',result
        return result
    
    # this builds a ManifoldQuery object from a dict as received from javascript through its ajax request 
    # we use a json-encoded string - see manifold.js for the sender part 
    # e.g. here's what I captured from the server's output
    # manifoldproxy.proxy: request.POST <QueryDict: {u'json': [u'{"action":"get","object":"resource","timestamp":"latest","filters":[["slice_hrn","=","ple.inria.omftest"]],"params":[],"fields":["hrn","hostname"],"unique":0,"query_uuid":"436aae70a48141cc826f88e08fbd74b1","analyzed_query":null,"subqueries":{}}']}>
    def fill_from_POST (self, POST_dict):
        try:
            json_string=POST_dict['json']
            dict=json.loads(json_string)
            for (k,v) in dict.iteritems(): 
                setattr(self,k,v)
        except:
            print "Could not decode incoming ajax request as a Query, POST=",POST_dict
            if (debug):
                import traceback
                traceback.print_exc()
        self.sanitize()

    #--------------------------------------------------------------------------- 
    # Accessors
    #--------------------------------------------------------------------------- 

    @returns(StringTypes)
    def get_action(self):
        return self.action

    @returns(frozenset)
    def get_select(self):
        return frozenset(self.fields)

    @returns(StringTypes)
    def get_from(self):
        return self.object

    @returns(Filter)
    def get_where(self):
        return self.filters

    @returns(dict)
    def get_params(self):
        return self.params

    @returns(StringTypes)
    def get_timestamp(self):
        return self.timestamp

#DEPRECATED#
#DEPRECATED#    def make_filters(self, filters):
#DEPRECATED#        return Filter(filters)
#DEPRECATED#
#DEPRECATED#    def make_fields(self, fields):
#DEPRECATED#        if isinstance(fields, (list, tuple)):
#DEPRECATED#            return set(fields)
#DEPRECATED#        else:
#DEPRECATED#            raise Exception, "Invalid field specification"

    #--------------------------------------------------------------------------- 
    # LINQ-like syntax
    #--------------------------------------------------------------------------- 

    @classmethod
    #@returns(Query)
    def action(self, action, object):
        """
        (Internal usage). Craft a Query according to an action name 
        See methods: get, update, delete, execute.
        Args:
            action: A String among {"get", "update", "delete", "execute"}
            object: The name of the queried object (String)
        Returns:
            The corresponding Query instance
        """
        query = Query()
        query.action = action
        query.object = object
        return query

    @classmethod
    #@returns(Query)
    def get(self, object):
        """
        Craft the Query which fetches the records related to a given object
        Args:
            object: The name of the queried object (String)
        Returns:
            The corresponding Query instance
        """
        return self.action("get", object)

    @classmethod
    #@returns(Query)
    def update(self, object):
        """
        Craft the Query which updates the records related to a given object
        Args:
            object: The name of the queried object (String)
        Returns:
            The corresponding Query instance
        """
        return self.action("update", object)
    
    @classmethod
    #@returns(Query)
    def create(self, object):
        """
        Craft the Query which create the records related to a given object
        Args:
            object: The name of the queried object (String)
        Returns:
            The corresponding Query instance
        """
        return self.action("create", object)
    
    @classmethod
    #@returns(Query)
    def delete(self, object):
        """
        Craft the Query which delete the records related to a given object
        Args:
            object: The name of the queried object (String)
        Returns:
            The corresponding Query instance
        """
        return self.action("delete", object)
    
    @classmethod
    #@returns(Query)
    def execute(self, object):
        """
        Craft the Query which execute a processing related to a given object
        Args:
            object: The name of the queried object (String)
        Returns:
            The corresponding Query instance
        """
        return self.action("execute", object)

    #@returns(Query)
    def at(self, timestamp):
        """
        Set the timestamp carried by the query
        Args:
            timestamp: The timestamp (it may be a python timestamp, a string
                respecting the "%Y-%m-%d %H:%M:%S" python format, or "now")
        Returns:
            The self Query instance
        """
        self.timestamp = timestamp
        return self

    def filter_by(self, *args):
        """
        Args:
            args: It may be:
                - the parts of a Predicate (key, op, value)
                - None
                - a Filter instance
                - a set/list/tuple of Predicate instances
        """
        if len(args) == 1:
            filters = args[0]
            if filters == None:
                self.filters = Filter()
                return self
            if not isinstance(filters, (set, list, tuple, Filter)):
                filters = [filters]
            for predicate in filters:
                self.filters.add(predicate)
        elif len(args) == 3: 
            predicate = Predicate(*args)
            self.filters.add(predicate)
        else:
            raise Exception, 'Invalid expression for filter'
        return self
            
    def select(self, *fields):

        # Accept passing iterables
        if len(fields) == 1:
            tmp, = fields
            if not tmp:
                fields = None
            elif isinstance(tmp, (list, tuple, set, frozenset)):
                fields = tuple(tmp)

        if not fields:
            # Delete all fields
            self.fields = set()
            return self

        for field in fields:
            self.fields.add(field)
        return self

    def set(self, params):
        self.params.update(params)
        return self

    def __or__(self, query):
        assert self.action == query.action
        assert self.object == query.object
        assert self.timestamp == query.timestamp # XXX
        filter = self.filters | query.filters
        # fast dict union
        # http://my.safaribooksonline.com/book/programming/python/0596007973/python-shortcuts/pythoncook2-chp-4-sect-17
        params = dict(self.params, **query.params)
        fields = self.fields | query.fields
        return Query.action(self.action, self.object).filter_by(filter).select(fields)

    def __and__(self, query):
        assert self.action == query.action
        assert self.object == query.object
        assert self.timestamp == query.timestamp # XXX
        filter = self.filters & query.filters
        # fast dict intersection
        # http://my.safaribooksonline.com/book/programming/python/0596007973/python-shortcuts/pythoncook2-chp-4-sect-17
        params =  dict.fromkeys([x for x in self.params if x in query.params])
        fields = self.fields & query.fields
        return Query.action(self.action, self.object).filter_by(filter).select(fields)

    def __le__(self, query):
        return ( self == self & query ) or ( query == self | query )

class AnalyzedQuery(Query):

    # XXX we might need to propagate special parameters sur as DEBUG, etc.

    def __init__(self, query=None, metadata=None):
        self.clear()
        self.metadata = metadata
        if query:
            self.query_uuid = query.query_uuid
            self.analyze(query)
        else:
            self.query_uuid = uniqid()

    @returns(StringTypes)
    def __str__(self):
        out = []
        fields = self.get_select()
        fields = ", ".join(fields) if fields else '*'
        out.append("SELECT %s FROM %s WHERE %s" % (
            fields,
            self.get_from(),
            self.get_where()
        ))
        cpt = 1
        for method, subquery in self.subqueries():
            out.append('  [SQ #%d : %s] %s' % (cpt, method, str(subquery)))
            cpt += 1

        return "\n".join(out)

    def clear(self):
        super(AnalyzedQuery, self).clear()
        self._subqueries = {}

    def subquery(self, method):
        # Allows for the construction of a subquery
        if not method in self._subqueries:
            analyzed_query = AnalyzedQuery(metadata=self.metadata)
            analyzed_query.action = self.action
            try:
                type = self.metadata.get_field_type(self.object, method)
            except ValueError ,e: # backwards 1..N
                type = method
            analyzed_query.object = type
            self._subqueries[method] = analyzed_query
        return self._subqueries[method]

    def get_subquery(self, method):
        return self._subqueries.get(method, None)

    def remove_subquery(self, method):
        del self._subqueries[method]

    def get_subquery_names(self):
        return set(self._subqueries.keys())

    def get_subqueries(self):
        return self._subqueries

    def subqueries(self):
        for method, subquery in self._subqueries.iteritems():
            yield (method, subquery)

    def filter_by(self, filters):
        if not isinstance(filters, (set, list, tuple, Filter)):
            filters = [filters]
        for predicate in filters:
            if predicate and '.' in predicate.key:
                method, subkey = predicate.key.split('.', 1)
                # Method contains the name of the subquery, we need the type
                # XXX type = self.metadata.get_field_type(self.object, method)
                sub_pred = Predicate(subkey, predicate.op, predicate.value)
                self.subquery(method).filter_by(sub_pred)
            else:
                super(AnalyzedQuery, self).filter_by(predicate)
        return self

    def select(self, *fields):

        # XXX passing None should reset fields in all subqueries

        # Accept passing iterables
        if len(fields) == 1:
            tmp, = fields
            if isinstance(tmp, (list, tuple, set, frozenset)):
                fields = tuple(tmp)

        for field in fields:
            if field and '.' in field:
                method, subfield = field.split('.', 1)
                # Method contains the name of the subquery, we need the type
                # XXX type = self.metadata.get_field_type(self.object, method)
                self.subquery(method).select(subfield)
            else:
                super(AnalyzedQuery, self).select(field)
        return self

    def set(self, params):
        for param, value in self.params.items():
            if '.' in param:
                method, subparam = param.split('.', 1)
                # Method contains the name of the subquery, we need the type
                # XXX type = self.metadata.get_field_type(self.object, method)
                self.subquery(method).set({subparam: value})
            else:
                super(AnalyzedQuery, self).set({param: value})
        return self
        
    def analyze(self, query):
        self.clear()
        self.action = query.action
        self.object = query.object
        self.filter_by(query.filters)
        self.set(query.params)
        self.select(query.fields)

    def to_json (self):
        query_uuid=self.query_uuid
        a=self.action
        o=self.object
        t=self.timestamp
        f=json.dumps (self.filters.to_list())
        p=json.dumps (self.params)
        c=json.dumps (list(self.fields))
        # xxx unique can be removed, but for now we pad the js structure
        unique=0

        aq = 'null'
        sq=", ".join ( [ "'%s':%s" % (object, subquery.to_json())
                  for (object, subquery) in self._subqueries.iteritems()])
        sq="{%s}"%sq
        
        result= """ new ManifoldQuery('%(a)s', '%(o)s', '%(t)s', %(f)s, %(p)s, %(c)s, %(unique)s, '%(query_uuid)s', %(aq)s, %(sq)s)"""%locals()
        if debug: print 'ManifoldQuery.to_json:',result
        return result
