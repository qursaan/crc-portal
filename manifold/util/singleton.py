#-------------------------------------------------------------------------
# Class Singleton
#
# Classes that inherit from Singleton can be instanciated only once 
#-------------------------------------------------------------------------

class Singleton(type):
    def __init__(cls, name, bases, dic):
        super(Singleton,cls).__init__(name,bases,dic)
        cls.instance=None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance=super(Singleton,cls).__call__(*args,**kw)
        return cls.instance


# See also
# http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
