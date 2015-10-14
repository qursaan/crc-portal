from unfold.plugin import Plugin

class SensLabMap (Plugin):

    # set checkboxes if a final column with checkboxes is desired
    # pass columns as the initial set of columns
    #   if None then this is taken from the query's fields
    def __init__ (self, query, query_all, **settings):
        Plugin.__init__ (self, **settings)
        self.query = query
        self.query_all = query_all
        self.query_all_uuid = query_all.query_uuid

    def template_file (self):
        return "senslabmap.html"

    def template_env (self, request):
        env={}
        return env

    def requirements (self):
        reqs = {
            'js_files' : [ "js/senslabmap.js",
                           "js/spin-presets.js", "js/spin.min.js", "js/jquery.spin.js",
                           "js/three.min.js", "js/jquery-mousewheel.min.js", "js/map.js",
                           ],
            'css_files': [ "css/senslabmap.css",
                           ],
            }
        return reqs

    # the list of things passed to the js plugin
    def json_settings_list (self): return ['plugin_uuid', 'dom_id', 'query_uuid', 'query_all_uuid']
