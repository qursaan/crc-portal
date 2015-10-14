from unfold.plugin import Plugin

class MadDash (Plugin):

    # set checkboxes if a final column with checkboxes is desired
    # pass columns as the initial set of columns
    #   if None then this is taken from the query's fields
    # latitude,longitude, zoom : the starting point
    def __init__ (self, query = None, query_all = None, **settings):
        Plugin.__init__ (self, **settings)
        self.query=query
        self.query_all = query_all
        self.query_all_uuid = query_all.query_uuid if query_all else None

    def template_file (self):
        return "maddash.html"

    def template_env (self, request):
        env={}
        return env

    def requirements (self):
        reqs = {
            'js_files' : [ 
                'http://d3js.org/d3.v3.min.js',
                'js/jquery.tipsy.js',
                'js/buffer.js', 'js/maddash.js',
                'js/manifold.js', 'js/manifold-query.js',
                'js/spin-presets.js', 'js/spin.min.js', 'js/jquery.spin.js', 
                'js/unfold-helper.js',
            ],
            'css_files' : [ 
                'css/maddash.css',
                'css/tipsy.css',
            ],
        }
        return reqs

    # the list of things passed to the js plugin
    def json_settings_list (self): return ['plugin_uuid','query_uuid', 'query_all_uuid']
