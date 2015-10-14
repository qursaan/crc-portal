from unfold.composite import Composite
from unfold.plugin    import Plugin

class Wizard(Composite):
   
    def __init__(self, *args, **kwargs):
        Composite.__init__(self, *args, **kwargs)
        self.validate_step_js = []
        
    def export_json_settings(self):
        # We need initialization, even though we are not associated with a query
        return True
    
    def requirements (self):
        #return { 'js_files'     : ['js/wizard.js', 'js/jquery.smartWizard-2.0.min.js', ],
        return { 'js_files'     : ['js/wizard.js', 'js/jquery.smartWizard-2.0.js', ],
                 'css_files'    : ['css/wizard.css', 'css/smart_wizard.css', ] 
                 }

    def template_file (self):
        return "wizard.html"

    # the list of things passed to the js plugin
    def json_settings_list (self): return ['plugin_uuid', 'start_step']
