from unfold.composite import Composite

# although the persistent_active feature originally targetted any kind of 
# composite widget, the current implementation clearly 
# works only with Tabs, as the javascript function for enabling a given tab
# cannot just set the 'active' class on some DOM element, but is required
# by bootstrap to call the tab() javascript method

class Tabs (Composite):
    
    """A composite plugin for arranging sons as selectable tabs
    
persistent_active: if set to True, enables preserving 
the domid for the active tab, so that a given page
will re-open with the same active tab
"""

    def __init__ (self, persistent_active=False, *args, **kwds):
        Composite.__init__ (self, *args, **kwds)
        self.persistent_active=persistent_active
        
    def requirements (self):
        return { 'js_files'     : ['js/tabs.js', 'js/bootstrap.js'],
                 'css_files'    : ['css/bootstrap.css', 'css/tabs.css', ] 
                 }

    def template_file (self):
        return "tabs.html"

    def template_env (self, request):
        inherited=Composite.template_env(self,request)
        inherited.update({'persistent_active':self.persistent_active})
        return inherited

    # see Composite.py for the details of template_env, that exposes global
    # 'sons' as a list of sons with each a set of a few attributes
    def json_settings_list (self):
        return []

