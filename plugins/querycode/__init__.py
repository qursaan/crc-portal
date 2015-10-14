from unfold.plugin import Plugin

class QueryCode (Plugin):

    def __init__ (self, query, **settings):
        Plugin.__init__ (self, **settings)
        self.query=query

    def template_file (self):
        return "querycode.html"

    def requirements (self):
        return { 
            'js_files' : [ 
                "js/querycode.js", 
                "js/manifold.js", "js/manifold-query.js",
                "js/spin-presets.js", "js/spin.min.js", "js/jquery.spin.js", 
                "js/shAutoloader.js","js/shCore.js","js/shBrushPython.js","js/shBrushRuby.js",
                ] ,
# thierry: see this file for details of why we turn this off for now            
            'css_files': [
                "css/querycode.css" ,
                "css/shCore.css","css/shCoreDefault.css","css/shThemeDefault.css",
                ],
            }

    def json_settings_list (self): return ['plugin_uuid','query_uuid']
