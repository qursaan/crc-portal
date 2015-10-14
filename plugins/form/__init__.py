from unfold.composite import Composite
from unfold.plugin    import Plugin

class CreateForm (Plugin):

    def __init__ (self, **settings):
        Plugin.__init__(self, **settings)
        print "SETTINGS", settings
        assert 'page'   in settings, "You should specify page"
        assert 'object' in settings, "You should specify object"

        if 'object' in settings:
            self.object = settings['object']

        if 'fields' in settings:
            self.fields = []
            for field in settings['fields']:
                c = {
                    'name'          : field.get('name', ''),
                    'field'         : field.get('field', ''),
                    'type'          : field.get('type', 'input'),
                    'description'   : field.get('description', ''),
                    'validate_rx'   : field.get('validate_rx', ''),
                    'validate_err'  : field.get('validate_err', ''),
                    'old_value'     : 'POST',
                }
                self.fields.append(c)
        else:
            # Attempt to retrieve object fields from metadata
            metadata = settings['page'].get_metadata()
            md_o = metadata.details_by_object(settings['object'])
            self.fields = md_o['column']
    
    def requirements (self):
        # Some should be included by default by manifold
        return { 'js_files'     : ['js/manifold.js', 'js/spin-presets.js', 'js/spin.min.js', 'js/jquery.spin.js',
                                   'js/form.js', 'js/jquery.validate.js', ],
                 'css_files'    : ['css/form.css'] 
                 }
    def export_json_settings(self):
        # We need initialization, even though we are not associated with a query
        return True

    def template_env (self, request):
        env={}
        env.update(self.__dict__)
        return env

    def template_file (self):
        return "form.html"

    def json_settings_list (self): return ['plugin_uuid', 'object', 'fields']
