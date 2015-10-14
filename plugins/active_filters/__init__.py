from unfold.plugin import Plugin
from manifold.util.predicate import eq, ne, lt, le, gt, ge, and_, or_, contains, included 

# NOTE: Python should pass templates to javascript for creating new filters
# - option variable
# - or, better, hidden div in the page
# In the meantime, templates are duplicated in the javascript code
# RECIPES FOR PLUGINS

# NOTE: having classes would help

class ActiveFilters(Plugin):

    def __init__ (self, query=None, **settings):
        Plugin.__init__ (self, **settings)

        self.query = query

    def template_file (self):
        return "active_filters.html"

    def template_env (self, request):

        def get_op_str(predicate):
            map = {
                eq      : 'eq',
                ne      : 'ne',
                lt      : 'lt',
                le      : 'le',
                gt      : 'gt',
                ge      : 'ge',
                and_    : 'and',
                or_     : 'or',
                contains: 'contains',
                included: 'included'
            }
            return map[predicate.get_op()]

        filters = [[f.get_key(), get_op_str(f), f.get_value()] for p in self.query.get_where()]
        env={}
        env.update(self.__dict__)
        env['filters'] = filters
        return env

    def requirements (self):
        reqs = {
            'js_files' : [
                'js/active_filters.js',
             ],
            'css_files': [ 
                'css/active_filters.css'
            ]
        }
        return reqs

    def json_settings_list (self):
        return ['plugin_uuid', 'domid', 'query_uuid']

    def export_json_settings (self):
        return True
