from manifold.util.singleton import Singleton

class ReactorWrapper(object):
    __metaclass__ = Singleton
    
    def __init__(self):
        # Be sure the import is done only at runtime, we keep a reference in the
        # class instance
        from twisted.internet import reactor
        self.reactor = reactor


    def callInReactor(self, callable, *args, **kw):
        print "ReactorWrapper::callInReactor"
        if self._reactorRunning:
            self.reactor.callFromThread(callable, *args, **kw)
        else:
            callable(*args, **kw)                 
            
    def isReactorRunning(self):
        return self._reactorRunning
       
    def start_reactor(self):
        self.reactor.run()

    def stop_reactor(self):
        self.reactor.stop()

    def addReactorEventTrigger(self, phase, eventType, callable):
        print "ReactorWrapper::addReactorEventTrigger"
        if self._reactorRunning:
            self.reactor.callFromThread(self.reactor.addSystemEventTrigger, phase, eventType, callable)
        else:
            self.reactor.addSystemEventTrigger(phase, eventType, callable)

    def __reactorShuttingDown(self):
        pass

    def __reactorShutDown(self):
        """This method called when the reactor is stopped"""
        print "REACTOR SHUTDOWN"
        self._reactorRunning = False

    def __getattr__(self, name):
        # We transfer missing methods to the reactor
        def _missing(*args, **kwargs):
            getattr(self.reactor, name)(*args, **kwargs)
        return _missing
