from unfold.plugin import Plugin

class TopmenuValidation (Plugin):

    """This plugin is designed to work together with topmenu.
    
It will check to see if user has PI rights at least on one authority, 
and if so will enable corresponding validation button in topmenu.

A realistic example would have incoming query as

Query.get('ple:user').filter_by('user_hrn', '==', '$user_hrn').select('pi_authorities')

"""

    def __init__ (self, query=None, button_domid=None, **settings):
        Plugin.__init__ (self, **settings)
        # set defaults
        # @qursaan
        #if query is None:
            #query = Query.get('ple:user').filter_by('user_hrn', '==', '$user_hrn').select('pi_authorities')
        if button_domid is None: button_domid="topmenu-validate"
        self.query=query
        self.button_domid=button_domid

    # this does not have any materialization
    def render_content (self, request):
        return ""
    
    def requirements (self):
        return { 'js_files': [ 'js/topmenuvalidation.js', 'js/manifold-query.js', 
                               "js/spin-presets.js", "js/spin.min.js", "js/jquery.spin.js", 
                               ], }

    def json_settings_list (self):
        return [ 'query_uuid', 'button_domid', ]

#################### here is an extract previously in topmenu.py
#import json
#from pprint import pprint
#from manifold.manifoldapi       import execute_query
#from manifold.core.query        import Query
###        # ** Where am I a PI **
###        # For this we need to ask SFA (of all authorities) = PI function
###        user_query  = Query().get('local:user').select('config','email')
###        user_details = execute_query(request, user_query)
###
###        # Required: the user must have an authority in its user.config
###        # XXX Temporary solution
###        # not always found in user_details...
###        config={}
#### Deactivated until fixed 
####        if user_details is not None:
####            for user_detail in user_details:
####                #email = user_detail['email']
####                if user_detail['config']:
####                    config = json.loads(user_detail['config'])
####            user_detail['authority'] = config.get('authority',"Unknown Authority")
####            print "topmenu: %s", (user_detail['authority'])
####            if user_detail['authority'] is not None:
####                sub_authority = user_detail['authority'].split('.')
####                root_authority = sub_authority[0]
####                pi_authorities_query = Query.get(root_authority+':user').filter_by('user_hrn', '==', '$user_hrn').select('pi_authorities')
####        else:
####            pi_authorities_query = Query.get('user').filter_by('user_hrn', '==', '$user_hrn').select('pi_authorities')
####        try:
####            pi_authorities_tmp = execute_query(request, pi_authorities_query)
####        except:
####            pi_authorities_tmp = set()
####        pi_authorities = set()
####        for pa in pi_authorities_tmp:
####            if 'pi_authorities' in pa:
####                pi_authorities |= set(pa['pi_authorities'])
####        print "pi_authorities =", pi_authorities
####        if len(pi_authorities) > 0:
####            result.append({'label':'Validation', 'href': '/portal/validate/'})
###        result.append({'label':'Validation', 'href': '/portal/validate/'})
