from unfold.plugin import Plugin

class StaticList (Plugin) :

    """ StaticList allows you to display an html list 
    that you provide the contents for in the 'list' input argument
    It is static in the sense that no query is going to be used to
    manage this contents
    """

    # only deal with our own stuff here and let Plugin handle the rest
    def __init__ (self, list=[], with_datatables=False, **settings):
        Plugin.__init__ (self, **settings)
        self.list=list
        self.with_datatables = with_datatables

    # SimpleList is useless per se anyways
    def template_file (self): 
        return "staticlist.html"
    
    def template_env (self, request):
        env={}
        # would need some cleaner means to set a header here
        header=getattr(self,'header',None)
        if header: env['header']=header
        env['list']=self.list
        env['with_datatables']= "yes" if self.with_datatables else ""
        return env

    def requirements (self):
        reqs = { 'js_files' : [ ] ,
                 'css_files': [ "css/staticlist.css" ],
                 }
        if self.with_datatables:
            reqs['js_files'].append ("js/dataTables.js")
            reqs['js_files'].append ("js/with-datatables.js")
        return reqs
