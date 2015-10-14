from unfold.plugin import Plugin

class Composite (Plugin):

    """a simple base class for plugins that contain/arrange a set of other plugins
sons is expected to be a list of the contained plugins, and 
active_domid is the domid for the one son that should be displayed as active
some subclasses of Composite, like e.g. Tabs, will not behave as expected 
if a valid active_domid is not provided
"""

    def __init__ (self, sons=None, active_domid=None, *args, **kwds):
        Plugin.__init__ (self, *args, **kwds)
        self.sons= sons if sons else []
        self.active_domid=active_domid
        # make sure this is valid, unset otherwise, so we always have exactly one active
        self.check_active_domid()
        
    def check_active_domid(self):
        matches= [ son for son in self.sons if son.domid==self.active_domid ]
        if len(matches)!=1: 
            print "WARNING: %s has %d valid son(s) for being active - expecting 1, resetting"%\
                (self,len(matches))
            self.active_domid=None
        
    def insert (self, plugin):
        self.sons.append(plugin)

    def template_env (self, request):
        # this is designed so as to support a template like
        # {% for son in sons %} {{ son.rendered }} ...
        def is_active (son,rank):
            # if active_domid is not specified, make the first one active
            if not self.active_domid: return rank==0
            return son.domid==self.active_domid
        ranks=range(len(self.sons))
        env = { 'sons':
                 [ { 'rendered': son.render(request),
                     'rank': rank,
                     'is_active': is_active(son,rank),
                     'title': son.title,
                     'domid': son.domid,
                     'classname': son.classname,
                     }
                   for (son,rank) in zip(self.sons,ranks) ]}
        return env

