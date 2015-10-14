from manifold.operators      import LAST_RECORD
import threading

#------------------------------------------------------------------
# Class callback
#------------------------------------------------------------------

class Callback:
    def __init__(self, deferred=None, router=None, cache_id=None):
    #def __init__(self, deferred=None, event=None, router=None, cache_id=None):
        self.results = []
        self._deferred = deferred

        #if not self.event:
        self.event = threading.Event()
        #else:
        #    self.event = event

        # Used for caching...
        self.router = router
        self.cache_id = cache_id

    def __call__(self, value):
        # End of the list of records sent by Gateway
        if value == LAST_RECORD:
            if self.cache_id:
                # Add query results to cache (expires in 30min)
                #print "Result added to cached under id", self.cache_id
                self.router.cache[self.cache_id] = (self.results, time.time() + CACHE_LIFETIME)

            if self._deferred:
                # Send results back using deferred object
                self._deferred.callback(self.results)
            else:
                # Not using deferred, trigger the event to return results
                self.event.set()
            return self.event

        # Not LAST_RECORD add the value to the results
        self.results.append(value)

    def wait(self):
        self.event.wait()
        self.event.clear()

    def get_results(self):
        self.wait()
        return self.results
        
