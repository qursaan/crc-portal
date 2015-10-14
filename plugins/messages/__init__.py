from unfold.plugin import Plugin

# lists levels and sets them to enabled or not at startup
default_levels = {'fatal': True, 'error': True, 'warning' : True, 'info' : True, 'debug' : False}
#default_levels = {'fatal': False, 'error': False, 'warning' : False, 'info' : False, 'debug' : False}

# there are two implementations available here
# one shows up in the main page like a regular part of the page,
# while the other one relies on transient popups
# by default we use the latter, but you can specify 
# transient=False if you want to use the former
# xxx
# also the pieces that go with this transient mode are
# under views/templates, it would make sense to move them over here
# however it turns out that views/templates/base.html unconditionnally
# includes messages-transient-header.html 
class Messages (Plugin):

    def __init__ (self, transient=True, levels=None, **settings):
        Plugin.__init__ (self, **settings)
        if levels is None: levels=default_levels
        # shortcut: 'ALL' turn everything on
        elif levels=='ALL': levels=dict( [ (k,True) for k in default_levels ] )
        elif levels=='NONE': levels=dict( [ (k,False) for k in default_levels ] )
        self.transient=transient
        self.levels=levels

    def template_file (self):
        return "messages.html" if not self.transient else "messages-transient.html"

    def requirements (self):
        return {
            'js_files' :  [ "js/messages.js", "js/manifold.js", ],
            'css_files' : "css/messages.css",
            }

    # although this has no query, we need a plugin instance to be created in the js output
    def export_json_settings (self):
        return True
    # the js plugin expects a domid
    def json_settings_list (self):
        return [ 'plugin_uuid', 'levels' ]

