
#from datetime              import  datetime
#from manifold.core.query   import Query
#from manifold.manifoldapi  import execute_admin_query, execute_query
#from portal.actions        import authority_get_pi_emails
#from portal.forms          import SliceRequestForm
#from portal.modules import schedule_slice
#import json

from django.template.loader import render_to_string
from django.shortcuts       import render
from django.core.mail       import send_mail
from django.utils           import timezone
from dateutil               import parser
from unfold.page            import Page
from portal.models          import PendingSlice, ResourcesInfo, VirtualNode, PhysicalNode, SimulationImage
from unfold.loginrequired   import LoginRequiredAutoLogoutView
from ui.topmenu             import topmenu_items, the_user
from portal.actions         import get_authority_by_user, get_authority_emails
from crc.settings           import SUPPORT_EMAIL


class SliceRequestView (LoginRequiredAutoLogoutView):
    def __init__(self):
        self.user_email = ''
        self.errors = []

    # because we inherit LoginRequiredAutoLogoutView that is implemented by redefining 'dispatch'
    # we cannot redefine dispatch here, or we'd lose LoginRequired and AutoLogout behaviours
    def post(self, request):
        return self.get_or_post(request, 'POST')

    def get(self, request):
        return self.get_or_post(request, 'GET')

    def get_or_post(self, request, method):
        # Using cache manifold-tables to get the list of authorities faster
        # @qursaan: comment and change
        # authorities_query = Query.get('authority').select('name', 'authority_hrn')
        #authorities = Authority.objects.all() #execute_admin_query(request, authorities_query)
        #if authorities is not None:
        #    authorities = sorted(authorities)

        #user_query = User.objects.get()
#        user_query  = Query().get('local:user').select('email')
#        user_email = execute_query(self.request, user_query)
        self.user_email = the_user(request)  # user_email[0].get('email')


#        account_query  = Query().get('local:account').select('user_id','platform_id','auth_type','config')
#        account_details = execute_query(self.request, account_query)

#        platform_query  = Query().get('local:platform').select('platform_id','platform','gateway_type','disabled')
#        platform_details = execute_query(self.request, platform_query)

        # getting user_hrn from local:account
#        for account_detail in account_details:
#            for platform_detail in platform_details:
#                if platform_detail['platform_id'] == account_detail['platform_id']:
#                    # taking user_hrn only from myslice account
#                    # NOTE: we should later handle accounts filter_by auth_type= managed OR user
#                    if 'myslice' in platform_detail['platform']:
#                        account_config = json.loads(account_detail['config'])
#                        user_hrn = account_config.get('user_hrn','N/A')
    
        #user_query  = Query().get('user').select('user_hrn').filter_by('user_hrn','==','$user_hrn')
        # @qursaan: must change
        user_hrn = the_user(request)   # execute_query(self.request, user_query)

        #self.user_hrn = user_hrn[0].get('user_hrn')
        total_nodes = PhysicalNode.objects.count()
        node_list = PhysicalNode.objects.all()
        #for i in range(int(total_nodes)):
        #    node_list.append(i+1)

        #total_resources = NodeResource.objects.count()
        resources_list = VirtualNode.objects.all() #[[range(total_resources)] for x in range(total_nodes)]
        resources_info = ResourcesInfo.objects.all()

        duration_list = []
        for i in range(1, 25, 1):
            duration_list.append(i)

        sim_os_list = SimulationImage.objects.all()

        page = Page(request)
        #page.add_css_files(["http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css"])

        if method == 'POST':
            self.errors = []
    
            # The form has been submitted
            slice_name  = request.POST.get('slice_name', '')
            authority_hrn = get_authority_by_user(the_user(request)) #request.POST.get('authority_hrn', '')
            request_date = request.POST.get('request_date', '')
            server_type = request.POST.get('server_type', '')
            request_type = request.POST.get('request_type', '')
            resource_group = request.POST.getlist('resource_group', [])
            #number_of_nodes = request.POST.get('number_of_nodes', '')
            purpose = request.POST.get('purpose', '')
            slice_duration = request.POST.get('sim_duration', '1')
            sim_os_image = request.POST.get('sim_os', '1')
            email = self.user_email
            #user_hrn = user_hrn
            cc_myself = True
            #print request_date
            #10/01/2015 12:00 PM
            request_date = parser.parse(request_date)
            print request_date

            #if (authority_hrn is None or authority_hrn == ''):
            #    self.errors.append('Please, select an authority')
            if (request_date is None or request_date == ''):
                self.errors.append('Please, determine the request date and time')
            # What kind of slice name is valid?
            if (slice_name is None or slice_name == ''):
                self.errors.append('Slice Name is mandatory')
            if (purpose is None or purpose == ''):
                self.errors.append('Purpose is mandatory')
    
            if not self.errors:
                ctx = {
                    'email'         : email,
                    'slice_name'    : slice_name,
                    'authority_hrn' : authority_hrn,
                    'server_type'   : server_type,
                    'request_type'  : request_type,
                    #'number_of_nodes': number_of_nodes,
                    'slice_duration': slice_duration,
                    'purpose'       : purpose,
                    'request_date'  : request_date,
                }            
                s = PendingSlice(
                    slice_name      = slice_name,
                    user_hrn        = user_hrn,
                    request_date    = request_date,
                    authority_hrn   = authority_hrn,
                    server_type     = server_type,
                    request_type    = request_type,
                    base_image      = sim_os_image,
                    slice_duration  = slice_duration,
                    #number_of_nodes = number_of_nodes,
                    purpose         = purpose,
                    status          = 1,
                )
                s.save()
                #for i in resource_group:
                 #   duration_list.append(i)
                  #  p = PendingReservationDetail(
                   #     slice_id=s,
                    #    node_resource_id=NodeResource.objects.get(id=i),
                   # )
                   # p.save()

                #schedule_slice(s.id)

                # The recipients are the PI of the authority
                recipients = get_authority_emails(authority_hrn) #authority_get_pi_emails(request, authority_hrn)
    
                #if cc_myself:
                recipients.append(SUPPORT_EMAIL)
                msg = render_to_string('slice-request-email.txt', ctx)
                #print "email, msg, email, recipients", email , msg, email, recipients 
                send_mail("CRC user %s requested a slice"%email, msg, email, recipients)

                template_env = {
                    'topmenu_items': topmenu_items('test_page', request),
                    'username': the_user(request),
                    'title': 'Request',
                }
                template_env.update(page.prelude_env())
                return render(request, 'slice-request-ack-view.html',template_env)  # Redirect after POST
     
        template_env = {
            'topmenu_items': topmenu_items('Request a slice', page.request),
            'username': the_user(request),
            'errors': self.errors,
            'slice_name': request.POST.get('slice_name', ''),
            #'authority_hrn': request.POST.get('authority_hrn', ''),
            'node_list': node_list,
            'resource_list': resources_list,
            'resource_info': resources_info,
            'duration_list': duration_list,
            'sim_os_list': sim_os_list,
            'sim_os': request.POST.get('sim_os',''),
            'resource_group' : request.POST.getlist('resource_group',[]),
            'server_type': request.POST.get('server_type', ''),
            'request_type': request.POST.get('request_type', ''),
            'sim_duration': request.POST.get('slice_duration', ''),
            'number_of_nodes': request.POST.get('number_of_nodes', ''),
            'purpose': request.POST.get('purpose', ''),
            'email': self.user_email,
            'user_hrn': user_hrn,
            'cc_myself': True,
            'time_now':timezone.now(),
            #'authorities': authorities,
            'title': "Request a Slice"
        }
        template_env.update(page.prelude_env())
        return render(request, 'slicerequest-view.html', template_env)
