from unfold.plugin import Plugin

class GoogleMap (Plugin):

    # expcted input are
    # query :           query about the slice 
    # query_all :       query about all resources
    # googlemap_key :   mandatory googlemap API v3 key
    # latitude,longitude, zoom : the starting point
    # apparently at some point there has been support for a boolean 'checkboxes' input arg but seems dropped
    def __init__ (self, query, query_all, googlemap_api_key=None, latitude=43., longitude=7., zoom=4, **settings):
        Plugin.__init__ (self, **settings)
        self.query=query
        self.query_all = query_all
        self.googlemap_api_key=googlemap_api_key
        self.query_all_uuid = query_all.query_uuid if query_all else None
        self.latitude=latitude
        self.longitude=longitude
        self.zoom=zoom

    def template_file (self):
        return "googlemap.html"

    def template_env (self, request):
        env={}
        return env

    def requirements (self):
        googlemap_api_url = "https://maps.googleapis.com/maps/api/js?"
        if self.googlemap_api_key: googlemap_api_url+="key=%s&"%self.googlemap_api_key
        googlemap_api_url += "sensor=false"
        reqs = {
            # let users configure their googlemap API key in production deployements
            'js_files' : [ googlemap_api_url,
                           "/js/googlemap.js",
                           "/js/markerclusterer.js",
                            "js/manifold.js", "js/manifold-query.js", 
                            "js/spin-presets.js", "js/spin.min.js", "js/jquery.spin.js", 
                            "js/unfold-helper.js",
                           ],
            'css_files' : [ "css/googlemap.css",
                            ],
            }
        return reqs

    # the list of things passed to the js plugin
    def json_settings_list (self): 
        return [ 'plugin_uuid', 'query_uuid', 'query_all_uuid',
                 'init_key',
                 'latitude', 'longitude', 'zoom', 
                 ]
