from plugins.lists.simplelist import SimpleList

# the SimpleList plugin requires 'key' and 'value' that are used 
# on the results of the query for rendering
class SliceList (SimpleList):
    
    def __init__ (self, **settings):
        SimpleList.__init__(self, key='slice.slice_hrn', classname='slicelist', **settings)

    # writing a js plugin for that would be overkill, just use SimpleList
    def plugin_classname (self):
        return 'SimpleList'

    def requirements (self):
        req = SimpleList.requirements(self)
        req['css_files'] += [ 'css/slicelist.css' ]
        return req
