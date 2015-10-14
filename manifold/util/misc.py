import os, glob, inspect
from types import StringTypes

def find_local_modules(filepath):
    modules = []
    for f in glob.glob(os.path.dirname(filepath)+"/*.py"):
        name = os.path.basename(f)[:-3]
        if name != '__init__':
            modules.append(name)
    return modules 

def make_list(elt):
    if not elt or isinstance(elt, list):
        return elt
    if isinstance(elt, StringTypes):
        return [elt]
    if isinstance(elt, (tuple, set, frozenset)):
        return list(elt)


# FROM: https://gist.github.com/techtonik/2151727
# Public Domain, i.e. feel free to copy/paste
# Considered a hack in Python 2

import inspect
 
def caller_name(skip=2):
    """Get a name of a caller in the format module.class.method
    
       `skip` specifies how many levels of stack to skip while getting caller
       name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.
       
       An empty string is returned if skipped levels exceed stack height
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
      return ''
    parentframe = stack[start][0]    
    
    name = []
    module = inspect.getmodule(parentframe)
    # `modname` can be None when frame is executed directly in console
    # TODO(techtonik): consider using __main__
    if module:
        name.append(module.__name__)
    # detect classname
    if 'self' in parentframe.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parentframe.f_locals['self'].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != '<module>':  # top level usually
        name.append( codename ) # function or a method
    del parentframe
    return ".".join(name)

def is_sublist(x, y, shortcut=None):
    if not shortcut: shortcut = []
    if x == []: return (True, shortcut)
    if y == []: return (False, None)
    if x[0] == y[0]:
        return is_sublist(x[1:],y[1:], shortcut)
    else:
        return is_sublist(x, y[1:], shortcut + [y[0]])
