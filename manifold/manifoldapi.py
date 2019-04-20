# Manifold API Python interface
import copy, xmlrpc

from crc.configengine import ConfigEngine

from django.contrib import messages
from .manifoldresult import ManifoldResult, ManifoldCode, ManifoldException
from manifold.core.result_value import ResultValue

debug=False
debug=True
debug_deep=False
#debug_deep=True

########## ugly stuff for hopefully nicer debug messages
def mytruncate (obj, l):
    # we will add '..'
    l1=l-2
    repr="%s"%obj
    return (repr[:l1]+'..') if len(repr)>l1 else repr

from time import time, gmtime, strftime
from math import trunc
def mytime (start=None):
    gm=gmtime()
    t=time()
    msg=strftime("%H:%M:%S-", gmtime())+"%03d"%((t-trunc(t))*1000)
    if start is not None: msg += " (%03fs)"%(t-start)
    return t,msg
##########

class ManifoldAPI:

    def __init__ (self, auth=None, cainfo=None):

        self.auth = auth
        self.cainfo = cainfo
        self.errors = []
        self.trace = []
        self.calls = {}
        self.multicall = False
        self.url = ConfigEngine().manifold_url()
        self.server = xmlrpc.Server(self.url, verbose=False, allow_none=True)

    def __repr__ (self): return "ManifoldAPI[%s]"%self.url

    def _print_value (self, value):
        print ("+++",'value',)
        if isinstance (value,list):     print ("[%d]"%len(value),)
        elif isinstance (value,dict):   print ("{%d}"%len(value),)
        print (mytruncate (value,80))

    # a one-liner to give a hint of what the return value looks like
    def _print_result (self, result):
        if not result:                        print ("[no/empty result]")
        elif isinstance (result,str):         print ("result is '%s'"%result)
        elif isinstance (result,list):        print ("result is a %d-elts list"%len(result))
        elif isinstance (result,dict):
            print ("result is a dict with %d keys : %s"%(len(result),result.keys()))
            for (k,v) in result.iteritems():
                if v is None: continue
                if k=='value':  self._print_value(v)
                else:           print ('+++',k,':',mytruncate (v,30))
        else:                                 print ("[dont know how to display result] %s"%result)

    # how to display a call
    def _repr_query (self,methodName, query):
        try:    action=query['action']
        except: action="???"
        try:    subject=query['object']
        except: subject="???"
        # most of the time, we run 'forward'
        if methodName=='forward':       return "forward(%s(%s))"%(action,subject)
        else:                           return "%s(%s)"%(action,subject)

    # xxx temporary code for scaffolding a ManifolResult on top of an API that does not expose error info
    # as of march 2013 we work with an API that essentially either returns the value, or raises
    # an xmlrpclib.Fault exception with always the same 8002 code
    # since most of the time we're getting this kind of issues for expired sessions
    # (looks like sessions are rather short-lived), for now the choice is to map these errors on
    # a SESSION_EXPIRED code
    def __getattr__(self, methodName):
        def func(*args, **kwds):
            # shorthand
            def repr(): return self._repr_query (methodName, args[0])
            try:
                if debug:
                    start,msg = mytime()
                    print ("====>",msg,"ManifoldAPI.%s"%repr(),"url",self.url)
                    # No password in the logs
                    logAuth = copy.copy(self.auth)
                    for obfuscate in ['Authring','session']:
                        if obfuscate in logAuth:  logAuth[obfuscate]="XXX"
                    if debug_deep: print ("=> auth",logAuth)
                    if debug_deep: print ("=> args",args,"kwds",kwds)
                annotations = {
                    'authentication': self.auth
                }
                args += (annotations,)
                result = getattr(self.server, methodName)(*args, **kwds)
                print ("%s%r" %(methodName, args))

                if debug:
                    print ('<= result=',)
                    self._print_result(result)
                    end,msg = mytime(start)
                    print ("<====",msg,"backend call %s returned"%(repr()))

                return ResultValue(**result)

            except Exception as error:
                print ("** MANIFOLD API ERROR **")
                if debug:
                    print ("===== xmlrpc catch-all exception:",error)
                    import traceback
                    traceback.print_exc(limit=3)
                if "Connection refused" in error:
                    raise ManifoldException ( ManifoldResult (code=ManifoldCode.SERVER_UNREACHABLE,
                                                              output="%s answered %s"%(self.url,error)))
                # otherwise
                print ("<==== ERROR On ManifoldAPI.%s"%repr())
                raise ManifoldException ( ManifoldResult (code=ManifoldCode.SERVER_UNREACHABLE, output="%s"%error) )

        return func

def _execute_query(request, query, manifold_api_session_auth):
    manifold_api = ManifoldAPI(auth=manifold_api_session_auth)
    print ("-"*80)
    print (query)
    print (query.to_dict())
    print ("-"*80)
    result = manifold_api.forward(query.to_dict())
    if result['code'] == 2:
        # this is gross; at the very least we need to logout()
        # but most importantly there is a need to refine that test, since
        # code==2 does not necessarily mean an expired session
        # XXX only if we know it is the issue
        if 'manifold' in request.session:
            del request.session['manifold']
        # Flush django session
        request.session.flush()
        #raise Exception, 'Error running query: %r' % result

    if result['code'] == 1:
        print ("WARNING")
        print (result['description'])

    # XXX Handle errors
    #Error running query: {'origin': [0, 'XMLRPCAPI'], 'code': 2, 'description': 'No such session: No row was found for one()', 'traceback': 'Traceback (most recent call last):\n  File "/usr/local/lib/python2.7/dist-packages/manifold/core/xmlrpc_api.py", line 68, in xmlrpc_forward\n    user = Auth(auth).check()\n  File "/usr/local/lib/python2.7/dist-packages/manifold/auth/__init__.py", line 245, in check\n    return self.auth_method.check()\n  File "/usr/local/lib/python2.7/dist-packages/manifold/auth/__init__.py", line 95, in check\n    raise AuthenticationFailure, "No such session: %s" % e\nAuthenticationFailure: No such session: No row was found for one()\n', 'type': 2, 'ts': None, 'value': None}

    return result['value']

def execute_query(request, query):
    if not 'manifold' in request.session or not 'auth' in request.session['manifold']:
        request.session.flush()
        raise Exception( "User not authenticated")
    manifold_api_session_auth = request.session['manifold']['auth']
    return _execute_query(request, query, manifold_api_session_auth)

def execute_admin_query(request, query):
    admin_user, admin_password = ConfigEngine().manifold_admin_user_password()
    admin_auth = {'AuthMethod': 'password', 'Username': admin_user, 'AuthString': admin_password}
    return _execute_query(request, query, admin_auth)
