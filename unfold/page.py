# the supervisor for Plugins
# keeps a handle on all present plugins for managing their queries in a consistent way
# it is expected to exist one such object for a given page

import json

from django.template.loader import render_to_string

from manifold.metadata import MetaData

from unfold.prelude import Prelude

from crc.configengine import ConfigEngine

# decorator to deflect calls on this Page to its prelude
def to_prelude (method):
    def actual (self, *args, **kwds):
        prelude_method=Prelude.__dict__[method.__name__]
        return prelude_method(self.prelude,*args, **kwds)
    return actual

debug = False
debug = True


class Page:

    def __init__(self, request):
        self.request=request
        # all plugins mentioned in this page
        self._plugins = {}
        # the set of all queries
        self._queries=set()
        # queue of queries with maybe a domid, see enqueue_query
        self._queue=[]
        # global prelude object
        # global requirements should go in base.html
        self.prelude=Prelude()

    # record known plugins hashed on their domid
    def record_plugin (self, plugin):
        self._plugins[plugin.domid]=plugin

    def get_plugin (self, domid):
        return self._plugins.get(domid,None)

    # not sure this is useful at all
#    def reset_queue (self):
#        self._queries = set()
#        self._queue = []

    # this method adds a query to the page
    # the query will be exposed to js when calling __expose_queries, which is done by prelude_env()
    # additionally if run_it is set to True, this query will be asynchroneously triggered on page load
    # in this case (exec=True) the js async callback (see manifold.asynchroneous_success)
    # offers the option to deliver the result to a specific DOM elt (in this case, set domid)
    # otherwise (i.e. if domid not provided), it goes through the pubsub system (so all plugins can receive it)
    #
    # NOTE:
    # analyzed_query is required because it contains query_uuid that the
    # plugins initialized in the python part will listen to. When a result is
    # received in javascript, subresults should be publish to the appropriate
    # query_uuid.
    #
    def enqueue_query (self, query, run_it=True, domid=None, analyzed_query=None):
        # _queries is the set of all known queries
        # XXX complex XXX self._queries = self._queries.union(set( [ query, ] ))
        self._queries.add((query, analyzed_query))
        # _queue is the list of queries that need to be triggered, with an optional domid
        # we only do this if run_it is set
        if run_it: self._queue.append ( (query.query_uuid,domid) )

    def generate_records(self, query, generators, number=10):
        self.add_js_files('js/record_generator.js');
        js_chunk = '$(document).ready(function() { new RecordGenerator(%s,%s,%s).run(); });'%(query.to_json(),json.dumps(generators),number);
        self.add_js_chunks(js_chunk)

    # return the javascript code for exposing queries
    # all queries are inserted in the global manifold object
    # in addition, the ones enqueued with 'run_it=True' are triggered
    def __expose_queries(self):
        # compute variables to expose to the template
        env = {}
        # expose the json definition of all queries
        env['queries_json'] = [ query.to_json(analyzed_query=aq) for (query, aq) in self._queries ]
        def query_publish_dom_tuple (a,b):
            result={'query_uuid':a}
            if b: result['domid']=b
            return result
        env['query_exec_tuples'] = [ query_publish_dom_tuple (a,b) for (a,b) in self._queue ]
        javascript = render_to_string ("page-queries.js",env)
        self.add_js_chunks (javascript)
#        self.reset_queue()
        # unconditionnally expose MANIFOLD_URL, this is small and manifold.js uses that for various messages
        self.expose_js_manifold_config()

    # needs to be called explicitly and only when metadata is actually required
    # in particular user needs to be logged
    def get_metadata(self):
        # look in session's cache - we don't want to retrieve this for every request
        session=self.request.session

        if 'manifold' not in session:
            session['manifold'] = {}
        manifold = session['manifold']

        # if cached, use it
        if 'metadata' in manifold and isinstance(manifold['metadata'],MetaData):
            if debug: print "Page.get_metadata: return cached value"
            return manifold['metadata']

        metadata_auth = {'AuthMethod':'anonymous'}

        metadata=MetaData (metadata_auth)
        metadata.fetch(self.request)
        # store it for next time
        manifold['metadata']=metadata
        if debug: print "Page.get_metadata: return new value"
        return metadata

    def expose_js_metadata(self):
        # expose global MANIFOLD_METADATA as a js variable
        # xxx this is fetched synchroneously..
        self.add_js_init_chunks("var MANIFOLD_METADATA =" + self.get_metadata().to_json() + ";\n")

    def expose_js_manifold_config (self):
        self.add_js_init_chunks(ConfigEngine().manifold_js_export())

    #################### requirements/prelude management
    # just forward to self.prelude - see decorator above
    @to_prelude
    def add_js_files (self):pass
    @to_prelude
    def add_css_files (self):pass
    @to_prelude
    def add_js_init_chunks (self):pass
    @to_prelude
    def add_js_chunks (self):pass
    @to_prelude
    def add_css_chunks (self):pass

    # prelude_env also does expose_queries
    def prelude_env (self):
        #self.__expose_queries()
        from_prelude=self.prelude.prelude_env()
        return from_prelude
