from unfold.plugin import Plugin

class MyPlugin(Plugin):
    
    def __init__ (self, query=None, **settings):
        Plugin.__init__ (self, **settings)
        self.query=query

    def template_file (self):
        return "myplugin.html"

    def requirements (self):
        reqs = {
            'js_files' : [
                'js/myplugin.js'
            ],
            'css_files': [
                'css/myplugin.css',
            ]
        }
        return reqs

    def json_settings_list (self):
        # query_uuid will pass self.query results to the javascript
        # and will be available as "record" in :
        # on_new_record: function(record)
        return ['plugin_uuid', 'domid', 'query_uuid']

    def export_json_settings (self):
        return True
