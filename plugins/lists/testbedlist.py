from plugins.lists.simplelist import SimpleList

class TestbedList (SimpleList):
    
    def __init__ (self, **settings):
        SimpleList.__init__(self, key='platform', classname='testbedlist', **settings)

    # writing a js plugin for that would be overkill, just use SimpleList
    def plugin_classname (self):
        return 'SimpleList'

    def requirements (self):
        req = SimpleList.requirements(self)
        req['css_files'] += [ 'css/testbedlist.css' ]
        return req
