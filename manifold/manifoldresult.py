def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

ManifoldCode = enum (
    UNKNOWN_ERROR=-1,
    SUCCESS=0,
    SESSION_EXPIRED=1,
    NOT_IMPLEMENTED=2,
    SERVER_UNREACHABLE=3,
)

_messages_ = { -1 : "Unknown", 0: "OK", 1: "Session Expired", 2: "Not Implemented", 3: "Backend server unreachable"}

# being a dict this can be used with json.dumps
class ManifoldResult (dict):
    def __init__ (self, code=ManifoldCode.SUCCESS, value=None, output=""):
        self['code']=code
        self['value']=value
        self['output']=output
        self['description'] = '' # Jordan: needed by javascript code

    def from_json (self, json_string):
        d=json.dumps(json_string)
        for k in ['code','value','output']:
            self[k]=d[k]

    # raw accessors
    def code (self): return self['code']
    def output (self): return self['output']

    # this returns None if there's a problem, the value otherwise
    def ok_value (self):
        if self['code']==ManifoldCode.SUCCESS:
            return self['value']

    # both data in a single string
    def error (self):
        return "code=%s -- %s"%(self['code'],self['output'])


    def __repr__ (self):
        code=self['code']
        result="[MFresult %s (code=%s)"%(_messages_.get(code,"???"),code)
        if code==0:
            value=self['value']
            if isinstance(value,list): result += " [value=list with %d elts]"%len(value)
            elif isinstance(value,dict): result += " [value=dict with keys %s]"%value.keys()
            else: result += " [value=%s: %s]"%(type(value).__name__,value)
        else:
            result += " [output=%s]"%self['output']
        result += "]"
        return result

# probably simpler to use a single class and transport the whole result there
# instead of a clumsy set of derived classes
class ManifoldException (Exception):
    def __init__ (self, manifold_result):
        self.manifold_result=manifold_result
    def __repr__ (self):
        return "Manifold Exception %s"%(self.manifold_result.error())
