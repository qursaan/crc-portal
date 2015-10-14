from unfold.plugin import Plugin

class QuickFilter (Plugin) :

    def __init__ (self, criterias, **settings):
        Plugin.__init__(self, **settings)
        self.criterias=criterias
        self.page.expose_js_metadata()

    def template_file(self): return "quickfilter.html"

    def requirements(self):
        return { 
            'js_files': ["js/quickfilter.js", "js/metadata.js", ],
            'css_files': "css/quickfilter.css",
            }

    def json_settings_list (self):
        return ['criterias','plugin_uuid']

    def template_env (self,request):
        return {'criterias':self.criterias}
