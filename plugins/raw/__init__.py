from unfold.plugin import Plugin

# usage Raw (html="some html text")

class Raw (Plugin):

    def __init__ (self, html, **kwds):
        Plugin.__init__ (self, **kwds)
        self.html=html

    def render_content (self, request):
        return self.html
