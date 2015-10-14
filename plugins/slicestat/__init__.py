from unfold.plugin import Plugin

class SliceStat(Plugin):
    
    def __init__ (self, query, **settings):
        Plugin.__init__ (self, **settings)
        self.query=query
    
    def template_file (self):
        return "slicestat.html"

    def requirements (self):
        reqs = {
            'js_files' : [
                
                'js/slicestat.js',

            ],
            'css_files': [
                'css/slicestat.css',
            ]
        }
        return reqs

    def json_settings_list (self):
        return ['plugin_uuid', 'domid', 'query_uuid', 'slicename', 'o']

    def export_json_settings (self):
        return True
