__author__ = 'qursaan'

from django.template.loader import render_to_string
from django.shortcuts       import render
from django.contrib         import messages
from django.core.mail       import send_mail
from django.utils           import timezone
from dateutil               import parser
from unfold.page            import Page
from portal.models          import SimReservation,Reservation, ReservationDetail,\
                                    SimulationImage, TestbedImage, \
                                    ResourcesInfo, VirtualNode, PhysicalNode, SimulationVM
from unfold.loginrequired   import LoginRequiredAutoLogoutView
from ui.topmenu             import topmenu_items, the_user
from portal.actions         import get_authority_by_user, get_authority_emails, \
                                    get_user_by_email, schedule_online
from crc.settings           import SUPPORT_EMAIL


class ReservationView (LoginRequiredAutoLogoutView):
    def __init__(self):
        self.user_email = ''
        self.errors = []

    def post(self, request):
        return self.get_or_post(request, 'POST')

    def get(self, request):
        return self.get_or_post(request, 'GET')

    def get_or_post(self, request, method):
        self.user_email = the_user(request)
        page = Page(request)

        user_hrn = the_user(request)
        user = get_user_by_email(user_hrn)

        #System Parameters
        max_duration = 24

        #Resources
        resources_list = VirtualNode.objects.all()
        resources_info = ResourcesInfo.objects.all()
        node_list = PhysicalNode.objects.all()
        sim_vm_list = SimulationVM.objects.all()

        #Images
        sim_img_list = SimulationImage.objects.all()
        omf_img_list = TestbedImage.objects.all()

        if method == 'POST':
            self.errors = []
            authority_hrn  = get_authority_by_user(the_user(request))
            slice_name     = request.POST.get('slice_name', '')
            server_type    = request.POST.get('server_type', '')
            request_type   = request.POST.get('request_type', '')

            request_date   = timezone.now() #request.POST.get('request_date', '')

            resource_group = request.POST.getlist('resource_group', [])
            sim_img        = request.POST.get('sim_img', '1')
            omf_img        = request.POST.get('sim_img', '1')
            sim_vm         = request.POST.get('sim_vm', '1')

            purpose         = request.POST.get('purpose', '')
            slice_duration  = request.POST.get('slice_duration', '1')

            #time
            start_time = request.POST.get('req_time_time1', '')
            end_time   = request.POST.get('req_time_time2', '')

            email           = self.user_email
            cc_myself       = True
            #request_date    = parser.parse(request_date)

            if request_date is None or request_date == '':
                self.errors.append('Please, determine the request date and time')
            if slice_name is None or slice_name == '':
                self.errors.append('Slice Name is mandatory')
            if purpose is None or purpose == '':
                self.errors.append('Purpose is mandatory')

            if not self.errors:
                ctx = {
                    'email'         : email,
                    'slice_name'    : slice_name,
                    'authority_hrn' : authority_hrn,
                    'server_type'   : server_type,
                    'request_type'  : request_type,
                    'slice_duration': slice_duration,
                    'purpose'       : purpose,
                    'request_date'  : request_date,
                }
                if server_type == "omf":
                    s = Reservation(
                        user_ref        = user,
                        f_start_time  = parser.parse(start_time).strftime('%Y-%m-%d %H:%M:%S'),
                        f_end_time     = parser.parse(end_time).strftime('%Y-%m-%d %H:%M:%S'),
                        slice_name     = slice_name,
                        slice_duration = slice_duration,  #approve_date
                        request_date   = request_date,
                        authority_hrn  = authority_hrn,
                        request_type   = request_type,
                        base_image_ref = TestbedImage.objects.get(id=omf_img),  #ref
                        purpose        = purpose,
                        status         = 1,
                    )
                    s.save()
                    for i in resource_group:
                        p = ReservationDetail(
                            reservation_ref=s,
                            node_ref=VirtualNode.objects.get(id=i),
                            image_ref=TestbedImage.objects.get(id=omf_img)
                        )
                        p.save()

                if server_type == "sim":
                    s = SimReservation(
                        user_ref         = user,
                        slice_name      = slice_name,
                        slice_duration  = slice_duration,  #approve_date
                        request_date    = request_date,
                        authority_hrn   = authority_hrn,
                        request_type    = request_type,
                        base_image_ref  = SimulationImage.objects.get(id=sim_img),  #ref
                        vm_name         = SimulationVM.objects.get(id=sim_vm),  #ref
                        purpose         = purpose,
                        status          = 1,
                    )
                    s.save()

                # TODO: @qursaan
                schedule_online(s.id)

                # The recipients are the PI of the authority
                # TODO: @qursaan
                recipients = get_authority_emails(authority_hrn) #authority_get_pi_emails(request, authority_hrn)

                #if cc_myself:
                recipients.append(SUPPORT_EMAIL)
                msg = render_to_string('slice-request-email.txt', ctx)
                send_mail("CRC user %s requested a slice"%email, msg, email, recipients)

                template_env = {
                    'topmenu_items': topmenu_items('test_page', request),
                    'username': the_user(request),
                    'title': 'Request',
                }
                template_env.update(page.prelude_env())
                return render(request, 'slice-request-ack-view.html', template_env)  # Redirect after POST

        template_env = {
            'topmenu_items' : topmenu_items('Request a slice', page.request),
            'username'      : the_user(request),
            'errors'        : self.errors,
            'slice_name'    : request.POST.get('slice_name', ''),
            'server_type'   : request.POST.get('server_type', ''),
            'request_type'  : request.POST.get('request_type', ''),

            'node_list'     : node_list,
            'resource_list' : resources_list,
            'resource_info' : resources_info,
            'resource_group': request.POST.getlist('resource_group',[]),
            'sim_vm_list'   : sim_vm_list,
            'sim_vm'       : request.POST.get('sim_vm',''),

            'max_duration'  :max_duration,
            'sim_img_list'  : sim_img_list,
            'omf_img_list'  : omf_img_list,
            'sim_img'       : request.POST.get('sim_img', ''),

            'slice_duration'  : request.POST.get('slice_duration', ''),
            'number_of_nodes': request.POST.get('number_of_nodes', ''),
            'purpose'       : request.POST.get('purpose', ''),
            'email'         : self.user_email,
            'user_hrn'      : user_hrn,
            #'login'         : user.username,
            #'cc_myself'     : True,
            'time_now'      :timezone.now(),
            'title': "Reservation System"
        }
        template_env.update(page.prelude_env())
        return render(request, 'reservation-view.html', template_env)

