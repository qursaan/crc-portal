from unfold.page          import Page
from unfold.loginrequired import LoginRequiredAutoLogoutView #,FreeAccessView
from ui.topmenu           import topmenu_items, the_user

from portal.models  import Authority
from portal.actions import get_requests, get_user_by_email
#from portal.modules import get_user_by_email

#import json
#from django.http                import HttpResponseRedirect, HttpResponse
#from django.shortcuts           import render
#from django.template.loader     import render_to_string

#from portal.event               import Event
# presview is put in observation for now
#from plugins.pres_view          import PresView
#from plugins.raw                import Raw

# these seem totally unused for now
#from portal.util                import RegistrationView, ActivationView
#from manifold.manifoldapi       import execute_query
#from manifold.core.query        import Query


class ValidatePendingView(LoginRequiredAutoLogoutView): # FreeAccessView):
    template_name = "validate_pending.html"

    def get_context_data(self, **kwargs):
        #messages.info(self.request, 'You have logged in')
        page = Page(self.request)
        ctx_my_authorities = {}
        #ctx_delegation_authorities = {}
        #ctx_sub_authorities = {}

        # The user need to be logged in
        if the_user(self.request):
            # Who can a PI validate:
            # His own authorities + those he has credentials for.
            # In MySlice we need to look at credentials also.
            

            # XXX This will have to be asynchroneous. Need to implement barriers,
            # for now it will be sufficient to have it working statically

            # get user_id to later on query accounts
            # XXX Having real query plan on local tables would simplify all this
            # XXX $user_email is still not available for local tables
            #user_query = Query().get('local:user').filter_by('email', '==', '$user_email').select('user_id')
            # @qursaan
            # user_query = Query().get('local:user').filter_by('email', '==', the_user(self.request)).select('user_id')
#           user, = execute_query(self.request, user_query)
            user = get_user_by_email(u_email=the_user(page.request))

#            user_id = user.id  # ['user_id']


            # Query manifold to learn about available SFA platforms for more information
            # In general we will at least have the portal
            # For now we are considering all registries
#            all_authorities = []
#            platform_ids = []
#            sfa_platforms_query = Query().get('local:platform').filter_by('gateway_type', '==', 'sfa').select('platform_id', 'platform', 'auth_type')
#            sfa_platforms = execute_query(self.request, sfa_platforms_query)
#            for sfa_platform in sfa_platforms:
#                print "SFA PLATFORM > ", sfa_platform['platform']
#                if not 'auth_type' in sfa_platform:
#                    continue
#                auth = sfa_platform['auth_type']
#                if not auth in all_authorities:
#                    all_authorities.append(auth)
#                platform_ids.append(sfa_platform['platform_id'])

#            print "W: Hardcoding platform myslice"
            # There has been a tweak on how new platforms are referencing a
            # so-called 'myslice' platform for storing authentication tokens.
            # XXX This has to be removed in final versions.
#            myslice_platforms_query = Query().get('local:platform').filter_by('platform', '==', 'myslice').select('platform_id')
#            myslice_platforms = execute_query(self.request, myslice_platforms_query)
#            if myslice_platforms:
#                myslice_platform, = myslice_platforms
#                platform_ids.append(myslice_platform['platform_id'])

            # We can check on which the user has authoritity credentials = PI rights
#            credential_authorities = set()
#            credential_authorities_expired = set()

            # User account on these registries
#            user_accounts_query = Query.get('local:account').filter_by('user_id', '==', user_id).filter_by('platform_id', 'included', platform_ids).select('auth_type', 'config')
#            user_accounts = execute_query(self.request, user_accounts_query)
            #print "=" * 80
            #print user_accounts
            #print "=" * 80
#            for user_account in user_accounts:

#                print "USER ACCOUNT", user_account
#                if user_account['auth_type'] == 'reference':
#                    continue # we hardcoded the myslice platform...

#                config = json.loads(user_account['config'])
#                creds = []
#                print "CONFIG KEYS", config.keys()
#                if 'authority_credentials' in config:
#                    print "***", config['authority_credentials'].keys()
#                    for authority_hrn, credential in config['authority_credentials'].items():
                        #if credential is not expired:
#                        credential_authorities.add(authority_hrn)
                        #else
                        #    credential_authorities_expired.add(authority_hrn)
#                if 'delegated_authority_credentials' in config:
#                    print "***", config['delegated_authority_credentials'].keys()
#                    for authority_hrn, credential in config['delegated_authority_credentials'].items():
                        #if credential is not expired:
#                        credential_authorities.add(authority_hrn)
                        #else
                        #    credential_authorities_expired.add(authority_hrn)

#            print 'credential_authorities =', credential_authorities
#            print 'credential_authorities_expired =', credential_authorities_expired

#            # Using cache manifold-tables to get the list of authorities faster
#            all_authorities_query = Query.get('authority').select('name', 'authority_hrn')
#            all_authorities = execute_query(self.request, all_authorities_query)
            # @qursaan:
#            all_authorities = Authority.objects.all()

            # ** Where am I a PI **
            # For this we need to ask SFA (of all authorities) = PI function
# @qursaan
#            pi_authorities_query = Query.get('user').filter_by('user_hrn', '==', '$user_hrn').select('pi_authorities')
#            pi_authorities_tmp = execute_query(self.request, pi_authorities_query)
            pi_authorities_tmp = Authority.objects.filter(authority_hrn=user.authority_hrn).all()
            pi_authorities = set()
            for pa in pi_authorities_tmp:
            #    pi_authorities |= set(pa.authority_hrn) #['pi_authorities'])
                pi_authorities=pi_authorities.union([user.authority_hrn])

#            # include all sub-authorities of the PI
#            # if PI on ple, include all sub-auths ple.upmc, ple.inria and so on...
#            pi_subauthorities = set()
#            for authority in all_authorities:
#                authority_hrn = authority.authority_hrn #['authority_hrn']
#                for my_authority in pi_authorities:
#                    if authority_hrn.startswith(my_authority) and authority_hrn not in pi_subauthorities:
#                        pi_subauthorities.add(authority_hrn)

            #print "pi_authorities =", pi_authorities
            #print "pi_subauthorities =", pi_subauthorities
            
            # My authorities + I have a credential
# @qursaan
#            pi_credential_authorities = pi_authorities & credential_authorities
#            pi_no_credential_authorities = pi_authorities - credential_authorities - credential_authorities_expired
#            pi_expired_credential_authorities = pi_authorities & credential_authorities_expired
            # Authorities I've been delegated PI rights
#            pi_delegation_credential_authorities = credential_authorities - pi_authorities
#            pi_delegation_expired_authorities = credential_authorities_expired - pi_authorities

            #print "pi_credential_authorities =", pi_credential_authorities
            #print "pi_no_credential_authorities =", pi_no_credential_authorities
            #print "pi_expired_credential_authorities =", pi_expired_credential_authorities
            #print "pi_delegation_credential_authorities = ", pi_delegation_credential_authorities
            #print "pi_delegation_expired_authorities = ", pi_delegation_expired_authorities

            # Summary intermediary
            pi_my_authorities = pi_authorities # pi_credential_authorities | pi_no_credential_authorities | pi_expired_credential_authorities
            #pi_delegation_authorities = [] # pi_delegation_credential_authorities | pi_delegation_expired_authorities

            #print "--"
            #print "pi_my_authorities = ", pi_my_authorities
            #print "pi_delegation_authorities = ", pi_delegation_authorities
            #print "pi_subauthorities = ", pi_subauthorities

            # Summary all
# @qursaan
#            queried_pending_authorities = pi_my_authorities | pi_delegation_authorities #| pi_subauthorities
            #print "----"
            #print "queried_pending_authorities = ", queried_pending_authorities

# iterate on the requests and check if the authority matches a prefix startswith an authority on which the user is PI
            requests = get_requests()
            #dest = {}
            # requests = get_requests(queried_pending_authorities)
            for request in requests:
                auth_hrn = request['authority_hrn']
                if user.is_admin==1:
                    for my_auth in pi_my_authorities:
                        if auth_hrn.startswith(my_auth):
                            #dest = ctx_my_authorities
                            request['allowed'] = 'allowed'
                # @qursaan
                # for my_auth in pi_delegation_authorities:
                #    if auth_hrn.startswith(my_auth):
                #        dest = ctx_delegation_authorities
                #        request['allowed'] = 'allowed'
                # if auth_hrn in pi_expired_credential_authorities:
                #      request['allowed'] = 'expired'
                if 'allowed' not in request:
                    request['allowed'] = 'denied'
               #print "authority for this request", auth_hrn

                if auth_hrn in pi_my_authorities:
                    #dest = ctx_my_authorities
                    if not auth_hrn in ctx_my_authorities:
                        ctx_my_authorities[auth_hrn] = []
                    ctx_my_authorities[auth_hrn].append(request)
#                    # define the css class
#                    if auth_hrn in pi_credential_authorities:
#                        request['allowed'] = 'allowed'
#                    elif auth_hrn in pi_expired_credential_authorities:
#                        request['allowed'] = 'expired'
#                    else: # pi_no_credential_authorities
#                        request['allowed'] = 'denied'
#
#                elif auth_hrn in pi_delegation_authorities:
#                    dest = ctx_delegation_authorities
#
#                    if auth_hrn in pi_delegation_credential_authorities:
#                        request['allowed'] = 'allowed'
#                    else: # pi_delegation_expired_authorities
#                        request['allowed'] = 'expired'
#
#                elif auth_hrn in pi_subauthorities:
#                    dest = ctx_sub_authorities
#
#                    if auth_hrn in pi_subauthorities:
#                        request['allowed'] = 'allowed'
#                    else: # pi_delegation_expired_authorities
#                        request['allowed'] = 'denied'
#
#                else:
#                    continue
# @qursaan
#                if not auth_hrn in dest:
#                    dest[auth_hrn] = []
#                dest[auth_hrn].append(request)
        
        context = super(ValidatePendingView, self).get_context_data(**kwargs)
        context['my_authorities'] = ctx_my_authorities
        #context['sub_authorities']   = ctx_sub_authorities
        #context['delegation_authorities'] = ctx_delegation_authorities
        context['is_admin'] = user.is_admin
        # XXX This is repeated in all pages
        # more general variables expected in the template
        context['title'] = 'Validate Requests'
        # the menu items on the top
        context['topmenu_items'] = topmenu_items('Validation', page.request)
        # so we can sho who is logged
        context['username'] = the_user(self.request) 

        # XXX We need to prepare the page for queries
        context.update(page.prelude_env())

        return context
