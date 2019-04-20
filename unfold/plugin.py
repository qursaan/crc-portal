# this is the abstract interface for Plugin instances
# so it should be specialized in real plugin classes
# like e.g. plugins.simplelist.SimpleList

import json

from django.template.loader import render_to_string

from unfold.page import Page
from unfold.prelude import Prelude

#################### 
# set DEBUG to
# . False : silent
# . [ 'SliceList', 'TabbedView' ] : to debug these classes
# . True : to debug all plugin

DEBUG= False
#DEBUG= [ 'SimpleList' ]
#DEBUG=True

# decorator to deflect calls on Plugin to its Prelude through self.page.prelude
def to_prelude (method):
    def actual (self, *args, **kwds):
        if not self.page: # jordan
            return None
        prelude_method=Prelude.__dict__[method.__name__]
        return prelude_method(self.page.prelude,*args, **kwds)
    return actual

class Plugin:

    # using a simple incremental scheme to generate domids for now
    # we just need this to be unique in a page
    domid=0

    # when a domid is not set by the caller, we name plugins after their respective class as well, 
    # so as to limit name clashes between different views
    # this has to see with the UI storing the last-seen status of plugins based on their id
    # put it more bluntly it is recommended that a domid should be set 
    # and maybe xxx we should just enforce that...
    def newdomid(self):
        Plugin.domid += 1
        return "plugin-%s-%d"%(self.__class__.__name__.lower(),Plugin.domid)

    ########## 
    # Constructor
    #### mandatory
    # . page: the context of the request being served
    # . title: is used visually for displaying the widget
    #### optional
    # . visible: if not set the plugin does not show up at all
    #            (not quite sure what this was for)
    # . togglable: whether it can be turned on and off by clicking on the title (like PleKitToggle)
    # . toggled:   whether the plugin should startup open/shown or closed/hidden
    #              possible values are
    #   .. True         : start up open/hidden
    #   .. False        : start up closed/shown
    #   .. 'persistent' : start up as it was the last time that browser showed it (based on 'domid')
    #                NOTE that it is required for you to set a domid if you want to use persistent mode
    #                     since domid is the key for storing that data in the browser storage space
    #   .. None         : if not passed to __init__ at all, then the default_toggled() method is called
    #   ..              : anything else, defaults to True
    # . outline_complete: whether the overall plugin (body + toggle buttons/title) needs to receive
    #                     a border and extra space
    # . outline_body    : same but for the plugin body only
    #      for these 2 outline_ flags, possible values mimick the above behaviour, i.e.:
    #   .. True:        : outline is on
    #   .. False:       : outline is off
    #   .. None:        : calls default_outline_complete() on the plugin object
    #
    #### internal data
    # . domid: created internally, but can be set at creation time if needed
    #          useful for hand-made css, or for selecting an active plugin in a composite
    # . rank: this is for plugins sons of a composite plugin
    #### custom
    # any other setting can also be set when creating the object, like
    # p=Plugin(foo='bar')
    # which will result in 'foo' being accessible to the template engine
    # 
    def __init__(self, page, title=None, domid=None,
                  visible=True, togglable=None, toggled=None,
                  outline_complete=None, outline_body=None,
                  **settings):
        self.page = page
        # callers can provide their domid for css'ing 
        if not domid: domid=self.newdomid()
        self.domid=domid
        # title is shown when togglable
        #if not title: title="Plugin title for %s"%domid
        self.title=title
        self.classname=self._py_classname()
        self.plugin_classname=self._js_classname()
        self.visible=visible
        if togglable is None:           self.togglable=self.default_togglable()
        else:                           self.togglable=togglable
        if toggled is None:             self.toggled=self.default_toggled()
        else:                           self.toggled=toggled
        if outline_complete is None:    self.outline_complete=self.default_outline_complete()
        else:                           self.outline_complete=outline_complete
        if outline_body is None:        self.outline_body=self.default_outline_body()
        else:                           self.outline_body=outline_body
        # what comes from subclasses
        for (k,v) in settings.iteritems():
            setattr(self,k,v)
            if self.need_debug(): print ("%s init - subclass setting %s"%(self.classname,k))
        # minimal debugging
        if self.need_debug():
            print ("%s init dbg .... BEG"%self.classname)
            for (k,v) in self.__dict__.items(): print ("dbg %s:%s"%(k,v))
            print ("%s init dbg .... END"%self.classname)
        # do this only once the structure is fine
        if self.page: # I assume we can have a None page (Jordan)
            self.page.record_plugin(self)

    def __repr__(self):
        return "[%s]:%s"%(self.classname,self.domid)

    def _py_classname(self):
        try:    return self.__class__.__name__
        except: return 'Plugin'

    def _js_classname(self):
        try:    return self.plugin_classname ()
        except: return self._py_classname()

    ##########
    def need_debug(self):
        if not DEBUG:           return False
        if DEBUG is True:       return True
        else:                   return self.classname in DEBUG

    def setting_json(self, setting):
        # TMP: js world expects plugin_uuid
        if setting=='plugin_uuid':
            value=self.domid
        elif setting=='query_uuid':
            try: value=self.query.query_uuid
            except: return '%s:"undefined"'%setting
        else:
            value=getattr(self,setting,None)
            if value is None: value = "unknown-setting-%s"%setting
        # first try to use to_json method (json.dumps not working on class instances)
        try:    value_json=value.to_json()
        except: value_json=json.dumps(value,separators=(',',':'))
        return "%s:%s"%(setting,value_json)

    # expose in json format to js the list of fields as described in json_settings_list()
    # and add plugin_uuid: domid in the mix
    # NOTE this plugin_uuid thing might occur in js files from joomla/js, ** do not rename **
    def settings_json(self):
        exposed_settings=self.json_settings_list()
        if 'query' in exposed_settings:
            print ("WARNING, cannot expose 'query' directly in json_settings_list, query_uuid is enough")
        result = "{"
        result += ",".join([ self.setting_json(setting) for setting in self.json_settings_list() ])
        result += "}"
        return result

    # as a first approximation, only plugins that are associated with a query
    # need to be prepared for js - meaning their json settings get exposed to js
    # others just get displayed and that's it
    def export_json_settings(self):
        return 'query_uuid' in self.json_settings_list()
    
    # returns the html code for that plugin
    # in essence, wraps the results of self.render_content ()
    def render(self, request):
        # call render_content
        plugin_content = self.render_content (request)
        # shove this into plugin.html
        env = {}
        env ['plugin_content']= plugin_content
        env.update(self.__dict__)
        # translate high-level 'toggled' into 4 different booleans
        self.need_toggle = False
        if self.toggled=='persistent':
            # start with everything turned off and let the js callback do its job
            env.update({'persistent_toggle':True,'display_hide_button':False,
                        'display_show_button':False,'display_body':False})
        elif self.toggled==False:
            env.update({'persistent_toggle':False,'display_hide_button':False,
                        'display_show_button':True,'display_body':False})
        else:
            env.update({'persistent_toggle':False,'display_hide_button':True,
                        'display_show_button':False,'display_body':True})
        if self.need_debug(): 
            print ("rendering plugin.html with env keys %s"%env.keys())
            for (k,v) in env.items(): 
                if "display" in k or "persistent" in k: print (k,'->',v)
        result = render_to_string ('plugin.html',env)

        # export this only for relevant plugins
        if self.export_json_settings():
            env ['settings_json' ] = self.settings_json()
            # compute plugin-specific initialization
            js_init = render_to_string ( 'plugin-init.js', env )
            # make sure this happens first in js
            self.add_js_init_chunks (js_init)
        
        # interpret the result of requirements ()
        self.handle_requirements (request)

        return result
        
    # you may redefine this completely, but if you don't we'll just use methods 
    # . template_file() to find out which template to use, and 
    # . template_env() to compute a dictionary to pass along to the templating system
    def render_content (self, request):
        """Should return an HTML fragment"""
        template = self.template_file()
        # start with a fresh one
        env={}
        # add our own settings as defaults
        env.update(self.__dict__)
        # then the things explicitly defined in template_env()
        env.update(self.template_env(request))
        if not isinstance (env,dict):
            raise Exception("%s.template_env returns wrong type"%self.classname)
        result=render_to_string (template, env)
        if self.need_debug():
            print ("%s.render_content: BEG --------------------"%self.classname)
            print ("template=%s"%template)
            print ("env.keys=%s"%env.keys())
            #print "env=%s"%env
            #print result
            print ("%s.render_content: END --------------------"%self.classname)
        return result

    # or from the result of self.requirements()
    def handle_requirements (self, request):
        try:
            d=self.requirements()
            for (k,v) in d.iteritems():
                if self.need_debug():
                    print ("%s: handling requirement %s"%(self.classname,v))
                # e.g. js_files -> add_js_files
                method_name='add_'+k
                method=Page.__dict__[method_name]
                method(self.page,v)
        except AttributeError: 
            # most likely the object does not have that method defined, which is fine
            pass
        except:
            import traceback
            traceback.print_exc()
            pass

    #################### requirements/prelude management
    # just forward to our prelude instance - see decorator above
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

    ######################################## abstract interface
    # your plugin is expected to implement either 
    # (*) def render_content(self, request) -> html fragment
    # -- or --
    # (*) def template_file (self) -> filename
    #   relative to STATIC 
    # (*) def template_env (self, request) -> dict
    #   this is the variable->value association used to render the template
    # in which case the html template will be used

    # if you see this string somewhere your template_file() code is not kicking in
    def template_file(self):           return "undefined_template"

    def template_env(self, request):   return {}

    def default_togglable(self):       return False

    def default_toggled(self):         return 'persistent'

    def default_outline_complete(self):return False

    def default_outline_body(self):    return False

#    # tell the framework about requirements (for the document <header>)
#    # the notion of 'Media' in django provides for medium-dependant
#    # selection of css files
#    # as a first attempt however we keep a flat model for now
#    # can use one string instead of a list or tuple if needed, 
#    # see requirements.py for details
#    def requirements (self): 
#        return { 'js_files' : [],       # a list of relative paths for js input files
#                 'css_files': [],       # ditto for css, could have been a dict keyed on
#                                        # media instead
#                 'js_chunk' : [],       # (lines of) verbatim javascript code 
#                 'css_chunk': [],       # likewise for css scripts
#                 }
    
#    # for better performance
#    # you can specify a list of keys that won't be exposed as json attributes
#    def exclude_from_json (self): return []

    # mandatory : define the fields that need to be exposed to json as part of 
    # plugin initialization
    # mention 'domid' if you need plugin_uuid
    # also 'query_uuid' gets replaced with query.query_uuid
    def json_settings_list (self): return ['json_settings_list-must-be-redefined']

    # might also define these ones:
    #
    # see e.g. slicelist.py that piggybacks simplelist js code
    # def plugin_classname (self)
    #
    # whether we export the json settings to js
    # def export_json_settings (self)
