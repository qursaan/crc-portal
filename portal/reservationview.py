__author__ = 'qursaan'

import json
from dateutil import parser

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib import messages

from portal.actions import get_authority_by_user, get_authority_emails, \
    get_user_by_email, get_user_type, \
    schedule_auto_online, schedule_checking, schedule_checking_freq  # schedule_sim_online, \
from portal.models import SimReservation, Reservation, ReservationDetail, \
    SimulationImage, TestbedImage, ResourcesInfo, VirtualNode, PhysicalNode, SimulationVM, \
    FrequencyRanges, ReservationFrequency
from lab.models import Course, Experiments, LabsTemplate

from ui.topmenu import topmenu_items, the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page

# TODO: @qursaan
from crc.settings import SUPPORT_EMAIL, MAX_OMF_DURATION, MAX_SIM_DURATION, MAX_BUK_DURATION
from datetime import timedelta
from reservation_status import ReservationStatus


class ReservationView(LoginRequiredAutoLogoutView):
    def __init__(self):
        self.user_email = ''
        self.errors = []
        self.user_type = None

    def post(self, request, url):
        return self.get_or_post(request, 'POST', url)

    def get(self, request, url):
        return self.get_or_post(request, 'GET', url)

    def get_or_post(self, request, method, url):
        self.user_email = the_user(request)
        page = Page(request)
        reserve_type = None
        use_bulk = False

        if url == "reservation":
            reserve_type = "R"
        elif url == "bulk":
            reserve_type = "I"
            use_bulk = True

        user_hrn = the_user(request)
        user = get_user_by_email(user_hrn)
        user_type = get_user_type(user)

        if user_type != 2 and reserve_type == "I":  # (user_type != 1 and reserve_type == "R")
            messages.error(page.request, 'Error: You have not permission to access this page.')
            return HttpResponseRedirect("/")

        print "UT: ", reserve_type, "template: ", url

        # Load System Parameters
        sim_max_duration = MAX_SIM_DURATION
        omf_max_duration = MAX_OMF_DURATION
        # bulk_max_duration = MAX_BUK_DURATION

        template_name = None
        courses_list = None
        if reserve_type == "I":
            courses_list = Course.objects.filter(instructor_ref=user)
            labs_list = LabsTemplate.objects.all()
            template_name = "ins-experiments-add.html"
            omf_max_duration = sim_max_duration
        elif reserve_type == "R":
            template_name = "reservation-view.html"

        # Resources
        resources_list = VirtualNode.objects.all()
        resources_info = ResourcesInfo.objects.all()
        node_list = PhysicalNode.objects.all()
        sim_vm_list = SimulationVM.objects.all()
        freq_list = FrequencyRanges.objects.all()

        # Images
        sim_img_list = SimulationImage.objects.all()
        omf_img_list = TestbedImage.objects.all()

        s = None

        if method == 'POST':
            self.errors = []

            ex_title = None
            ex_course = None
            ex_due_date = None
            ex_detail = None
            # ex_reserve_type = None
            ex_max_duration = None
            ex_allow_shh = None
            ex_allow_crt = None
            ex_allow_img = None
            ex_file = None
            ex_use_labs = None
            ex_idx_lab = None
            ex_tmp_lab = None

            if reserve_type == "I":
                ex_title = request.POST.get('ex_title', '')
                ex_course = request.POST.get('ex_course', '')
                ex_due_date = request.POST.get('due_date', '')
                ex_detail = request.POST.get('ex_detail', '')
                # ex_reserve_type = request.POST.get('reserve_type', '')
                ex_max_duration = request.POST.get('max_duration', '')
                if len(request.FILES) > 0:
                    ex_file = request.FILES['ex_file']
                ex_allow_shh = request.POST.get('allow_ssh', False)
                ex_allow_crt = request.POST.get('allow_crt', False)
                ex_allow_img = request.POST.get('allow_img', False)
                ex_use_labs = request.POST.get('use_lab', False)
                ex_idx_lab = int(request.POST.get('pre_exp', '-1'))
                ex_tmp_lab = request.POST.getlist('t_lab', [])

                if ex_title is None or ex_title == '':
                    self.errors.append('Experiment Name is mandatory')
                if ex_due_date is None or ex_due_date == '':
                    self.errors.append('ex_due_date is mandatory')

            authority_hrn = get_authority_by_user(the_user(request))
            slice_name = request.POST.get('slice_name', None)
            server_type = request.POST.get('server_type', '')
            request_type = request.POST.get('request_type', '')

            request_date = timezone.now()  # request.POST.get('request_date', '')

            resource_group = request.POST.getlist('resource_group', [])
            freq_group = request.POST.getlist('freq_group', [])
            sim_img = request.POST.get('sim_img', '1')
            omf_img = request.POST.get('sim_img', '1')
            sim_vm = request.POST.get('sim_vm', '1')
            sim_no_proc = request.POST.get('sim_no_proc', '1')
            sim_ram_size = request.POST.get('sim_ram_size', '1024')

            purpose = request.POST.get('purpose', '')

            # date
            start_date = request.POST.get('req_time_date1', '')
            start_date = parser.parse(start_date)
            end_date = request.POST.get('req_time_date2', '')
            end_date = parser.parse(end_date)
            # time
            start_time = request.POST.get('req_time_time1', '')
            end_time = request.POST.get('req_time_time2', '')

            h1 = int(parser.parse(start_time).strftime('%H'))
            h2 = int(parser.parse(end_time).strftime('%H'))
            m1 = int(parser.parse(start_time).strftime('%M'))
            m2 = int(parser.parse(end_time).strftime('%M'))

            start_datetime = start_date + timedelta(hours=h1, minutes=m1)
            end_datetime = end_date + timedelta(hours=h2, minutes=m2)

            diff = end_datetime - start_datetime
            dur = diff.seconds / 60 / 60
            slice_duration = request.POST.get('slice_duration', dur)

            # in case of urgent reservation set duration with time range
            if request_type == 'lazy_t':
                slice_duration = dur

            email = self.user_email
            cc_myself = True
            # request_date    = parser.parse(request_date)

            if request_date is None or request_date == '':
                self.errors.append('Please, determine the request date and time')
            if slice_name is None or slice_name == '':
                self.errors.append('Slice Name is mandatory')
            if purpose is None or purpose == '':
                self.errors.append('Purpose is mandatory')

            if not self.errors:

                if server_type == "omf":
                    s = Reservation(
                        user_ref=user,
                        f_start_time=start_datetime,
                        f_end_time=end_datetime,
                        slice_name=slice_name,
                        slice_duration=slice_duration,  # approve_date
                        request_date=request_date,
                        authority_hrn=authority_hrn,
                        request_type=request_type,
                        base_image_ref=TestbedImage.objects.get(id=omf_img),  # ref
                        purpose=purpose,
                        status=ReservationStatus.get_pending(),
                    )
                    s.save()
                    for i in resource_group:
                        p = ReservationDetail(
                            reservation_ref=s,
                            node_ref=VirtualNode.objects.get(id=i),
                            image_ref=TestbedImage.objects.get(id=omf_img)
                        )
                        p.save()

                    for i in freq_group:
                        p = ReservationFrequency(
                            reservation_ref=s,
                            frequency_ref=FrequencyRanges.objects.get(id=i),
                        )
                        p.save()

                    # TODO: @qursaan
                    if not schedule_auto_online(s.id, "omf",use_bulk,reserve_type):
                        self.errors.append('Sorry, Time slot is not free')
                        s.delete()

                elif server_type == "sim":
                    s = SimReservation(
                        user_ref=user,
                        slice_name=slice_name,
                        slice_duration=slice_duration,  # approve_date
                        request_date=request_date,
                        f_start_time=start_datetime,
                        f_end_time=end_datetime,
                        authority_hrn=authority_hrn,
                        request_type=request_type,
                        image_ref=SimulationImage.objects.get(id=sim_img),  # ref
                        node_ref=SimulationVM.objects.get(id=sim_vm),  # ref
                        purpose=purpose,
                        status=ReservationStatus.get_pending(),
                        n_processor=sim_no_proc,
                        n_ram=sim_ram_size,
                    )
                    s.save()
                    # TODO: @qursaan
                    if not schedule_auto_online(s.id, "sim",use_bulk,reserve_type):
                        self.errors.append('Sorry, Time slot is not free')
                        s.delete()

            if not self.errors:
                # save experiment
                if reserve_type == "I":
                    se = Experiments(
                        title=ex_title,
                        course_ref=Course.objects.get(id=ex_course),
                        due_date=parser.parse(ex_due_date),
                        description=ex_detail,
                        reservation_type=0,
                        max_duration=ex_max_duration,
                        server_type=server_type,
                        instructor_ref=user,
                        allow_ssh=ex_allow_shh,
                        allow_img=ex_allow_img,
                        allow_crt=ex_allow_crt,
                    )
                    if server_type == "omf":
                        se.reservation_ref = s
                    elif server_type == "sim":
                        se.sim_reservation_ref = s
                    se.save()

                    # Save file and update
                    if ex_file:
                        fs = FileSystemStorage()
                        new_filename = user.username + "_" + request_date.strftime('%d_%m_%Y') + "_" + ex_file.name
                        filename = fs.save(new_filename, ex_file)
                        uploaded_file_url = fs.url(filename)
                        se.sup_files = uploaded_file_url
                        se.save()

                    if ex_use_labs and len(ex_tmp_lab) > ex_idx_lab >= 0:
                        lab_temp_id = int(ex_tmp_lab[ex_idx_lab])
                        lab_temp_obj = LabsTemplate.objects.get(id=lab_temp_id)
                        if lab_temp_obj:
                            se.lab_template_ref = lab_temp_obj
                            se.save()

                # The recipients are the PI of the authority
                # TODO: @qursaan
                recipients = get_authority_emails(authority_hrn)  # authority_get_pi_emails(request, authority_hrn)
                ctx = {
                    'email': email,
                    'slice_name': slice_name,
                    'authority_hrn': authority_hrn,
                    'server_type': server_type,
                    'request_type': request_type,
                    'slice_duration': slice_duration,
                    'purpose': purpose,
                    'request_date': request_date,
                }
                # if cc_myself:
                recipients.append(SUPPORT_EMAIL)
                msg = render_to_string('slice-request-email.txt', ctx)
                send_mail("CRC user %s requested a slice" % email, msg, email, recipients)

                template_env = {
                    'topmenu_items': topmenu_items('test_page', request),
                    'username': the_user(request),
                    'title': 'Request',
                }
                template_env.update(page.prelude_env())
                return render(request, 'slice-request-ack-view.html', template_env)  # Redirect after POST

        template_env = {
            'topmenu_items': topmenu_items('Request a slice', page.request),
            'username': the_user(request),
            'errors': self.errors,
            'slice_name': request.POST.get('slice_name', ''),
            'server_type': request.POST.get('server_type', ''),
            'request_type': request.POST.get('request_type', ''),

            'freq_list': freq_list,
            'freq_group': request.POST.getlist('freq_group', []),

            'node_list': node_list,

            'resource_list': resources_list,
            'resource_info': resources_info,
            'resource_group': request.POST.getlist('resource_group', []),

            'sim_vm_list': sim_vm_list,
            'sim_vm': request.POST.get('sim_vm', ''),

            'sim_no_proc': request.POST.get('sim_no_proc', '1'),
            'sim_ram_size': request.POST.get('sim_ram_size', '1024'),

            'sim_max_duration': sim_max_duration,
            'omf_max_duration': omf_max_duration,
            # 'buk_max_duration': bulk_max_duration,
            'sim_img_list': sim_img_list,
            'omf_img_list': omf_img_list,
            'sim_img': request.POST.get('sim_img', ''),

            'slice_duration': request.POST.get('slice_duration', ''),
            'number_of_nodes': request.POST.get('number_of_nodes', ''),
            'purpose': request.POST.get('purpose', ''),
            'email': self.user_email,
            'user_hrn': user_hrn,
            # 'login'         : user.username,
            # 'cc_myself'     : True,
            'time_now': timezone.now(),
            'title': "Reservation System",

            # General
            'reserve_type': reserve_type,
        }

        if reserve_type == "I":
            if not courses_list:
                messages.success(request, 'Success: Add a Course First!')
                return HttpResponseRedirect("/lab/courses/")

            template_env['ex_title'] = request.POST.get('ex_title', '')
            template_env['ex_course'] = request.POST.get('ex_course', '')
            template_env['due_date'] = request.POST.get('ex_due_date', '')
            template_env['ex_detail'] = request.POST.get('ex_detail', '')
            template_env['reserve_type'] = request.POST.get('ex_reserve_type', '')
            template_env['max_duration'] = request.POST.get('ex_max_duration', '')
            template_env['ex_courses_list'] = courses_list
            template_env['labs_list'] = labs_list
            template_env['title'] = "Add New Experiment"

        template_env.update(page.prelude_env())
        return render(request, template_name, template_env)


@login_required
def check_availability(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")
    the_type = request.POST.get('the_type', None)

    # date
    start_date = request.POST.get('date1', '')
    start_date = parser.parse(start_date)
    end_date = request.POST.get('date2', '')
    end_date = parser.parse(end_date)
    # time
    start_time = request.POST.get('time1', '')
    end_time = request.POST.get('time2', '')

    h1 = int((parser.parse(start_time).strftime('%H')))
    h2 = int((parser.parse(end_time).strftime('%H')))
    m1 = int((parser.parse(start_time).strftime('%M')))
    m2 = int((parser.parse(end_time).strftime('%M')))

    start_datetime = timezone.make_aware(start_date + timedelta(hours=h1, minutes=m1))
    end_datetime = timezone.make_aware(end_date + timedelta(hours=h2, minutes=m2))

    if the_type == "omf":
        the_nodes = request.POST.getlist('the_nodes[]', None)
        the_freq = request.POST.getlist('the_freq[]', None)
        # msg = checking_omf_time(the_nodes, start_datetime, end_datetime)
        msg = schedule_checking(the_nodes, start_datetime, end_datetime, "omf")
        if the_freq:
            msg += schedule_checking_freq(the_freq, start_datetime, end_datetime)

            # busy_list = schedule_checking_all(start_datetime, end_datetime, "omf")
    elif the_type == "sim":
        the_nodes = request.POST.get('the_nodes', None)
        # the_dur = request.POST.get('the_dur', None)
        msg = schedule_checking(the_nodes, start_datetime, end_datetime, "sim")
        # busy_list = schedule_checking_all(start_datetime, end_datetime, "sim")
        # msg = checking_sim_time(the_nodes, start_datetime, end_datetime, the_dur)

    free = "0"
    if not msg:
        msg = "Free"
        free = "1"

    output = {
        "free": free,
        "msg": msg,
        # "busy": busy_list
    }

    post_data = json.dumps(output)
    return HttpResponse(post_data, content_type="application/json")
