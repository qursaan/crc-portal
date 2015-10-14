from django.template.loader import render_to_string

from unfold.composite import Composite

class Stack (Composite) :
    
    def template_file (self):        return "stack.html"
    def template_env (self, request):
        env = Composite.template_env (self, request)
        env['domid'] = self.domid
        return env
