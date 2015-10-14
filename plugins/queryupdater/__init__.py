from unfold.plugin import Plugin

class QueryUpdater(Plugin):

    def template_file (self):
        return "queryupdater.html"

    def requirements (self):
        reqs = {
            'js_files' : [ "js/dataTables.js", "js/queryupdater.js" ] ,
            'css_files': [ "css/dataTables.bootstrap.css", "css/queryupdater.css" ],
            }
        return reqs

    def json_settings_list (self):
        return ['plugin_uuid', 'domid', 'query_uuid']

