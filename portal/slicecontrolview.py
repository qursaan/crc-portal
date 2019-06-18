__author__ = 'pirate'
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from crc.settings import BACKENDIP
from lab.actions import get_control_options
#
from portal.models import Reservation, ReservationDetail, SimReservation, \
    TestbedImage, UserImage, SimulationImage, ReservationFrequency
from portal.navigation import action_load_save_image, omf_exe, remote_node, \
    check_task_progress, check_exe_progress, slice_on_time, abort_exe_progress, \
    lab_run, lab_check, lab_result, access_token_gen, action_prepare_nodes, check_emu
# from portal.actions import get_user_by_email, get_user_type
#
from portal.user_access_profile import UserAccessProfile
from ui.topmenu import topmenu_items  # , the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page


class SliceControlView(LoginRequiredAutoLogoutView):
    def post(self, request):
        return self.get_or_post(request, 'POST')

    def get(self, request):
        return self.get_or_post(request, 'GET')

    def get_or_post(self, request, method):
        template_name = "slice-control-view.html"
        page = Page(self.request)

        page.add_js_files(["js/jquery-1.11.1.js", "js/my_account.register.js", "js/my_account.edit_profile.js"])
        page.add_css_files(["css/plugin.css"])  # "css/onelab.css"

        image_list = None
        current_slice = None
        user_image_list = []
        node_list = []
        freq_list = []
        allow_ssh = True
        allow_crt = True
        allow_img = True
        supp_file = None
        show_lab = False
        show_enm = False
        lab_ref = None
        lab_param_list = []
        # vnc_link_access = None
        # vnc = False
        usera = UserAccessProfile(self.request)
        user = usera.user_obj  # get_user_by_email(the_user(self.request))
        if usera.access_all is False:
            user_image_list = UserImage.objects.filter(user_ref=user, username=usera.session_username).all()
        elif user:
            user_image_list = UserImage.objects.filter(user_ref=user).all()

        user_type = usera.user_type  # get_user_type(user)

        slice_id = page.request.session.get('slice_id', None)
        stype = page.request.session.get('stype', None)
        t = ''

        if not slice_id or not slice_on_time(page.request, stype):
            # messages.error(page.request, 'Error: You have not permission to access this page.')
            return HttpResponseRedirect("/portal/lab/current/")

        if slice_id:
            if stype == "omf":
                current_slice = Reservation.objects.get(id=slice_id)
                node_list = ReservationDetail.objects.filter(reservation_ref=current_slice)
                freq_list = ReservationFrequency.objects.filter(reservation_ref=current_slice)
                image_list = TestbedImage.objects.all()
                show_enm = current_slice.emulation_res
                t = 'Testbeds Remote Control Panel'
            elif stype == "sim":
                current_slice = SimReservation.objects.get(id=slice_id)
                node_list = SimReservation.objects.filter(id=slice_id)  # current_slice.vm_ref
                image_list = SimulationImage.objects.all()
                t = 'Simulation Remote Control Panel'
        # active_page = page.request.session.get('active_page','0')

        if not current_slice:
            return HttpResponseRedirect("/portal/lab/current/")

        if user_type == 3:
            allow_crt, allow_img, allow_ssh, supp_file, lab_ref, lab_param_list = get_control_options(stype,
                                                                                                      current_slice)
            if lab_ref:
                show_lab = True

        output_script = ''

        template_env = {
            'topmenu_items': topmenu_items('Control Panel', page.request),
            # 'errors': errors,
            'image_list': image_list,
            'slice_id': slice_id,
            'deadline': current_slice.end_time,
            'user_image_list': user_image_list,
            'node_list': node_list,
            'freq_list': freq_list,
            'output': output_script,
            'username': usera.username,  # the_user(self.request),
            'user_id': user.id,
            'title': t,
            'stype': stype,
            'allow_ssh': allow_ssh,
            'allow_crt': allow_crt,
            'allow_img': allow_img,
            'supp_file': supp_file,
            'show_lab': show_lab,
            'show_emu': show_enm,
            'lab_ref': lab_ref,
            'lab_param_list': lab_param_list,
            'vnc_link_access': "http://" + BACKENDIP + ":6080/vnc.html",
            'terminal_ip': "https://" + BACKENDIP + ":4200/"
            # 'vnc' :vnc,
        }
        template_env.update(page.prelude_env())
        return render(request, template_name, template_env)



@login_required
def control_access_token(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")
    return access_token_gen(request)


@login_required
def control_remote_node(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")
    return remote_node(request)


@login_required
def control_load_image(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")
    return action_load_save_image(request, "load")


@login_required
def control_save_image(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")
    return action_load_save_image(request, "save")


@login_required
def control_check_load(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")
    return check_task_progress(request, "load")


@login_required
def control_check_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")
    return check_task_progress(request, "save")


@login_required
def control_exe_script(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")
    return omf_exe(request)


@login_required
def control_exe_abort(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")
    return abort_exe_progress(request)


@login_required
def control_check_exe(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")
    return check_exe_progress(request)


@login_required
def control_load_sample(request):
    if request.method == 'POST':
        s_type = request.POST.get('the_post')
        response_data = {}

        t = None
        if s_type == "sample-1":
            t = render_to_string('sample-ping.rb')
        elif s_type == "sample-2":
            t = render_to_string('sample-urc.rb')

        response_data['result'] = t

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"error": "this isn't happening"}), content_type="application/json")


@login_required
def control_lab_run(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")
    return lab_run(request)


@login_required
def control_lab_check(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")
    return lab_check(request)


@login_required
def control_lab_result(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")
    return lab_result(request)


@login_required
def control_prepare_node(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")
    return action_prepare_nodes(request)


@login_required
def control_check_emu(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")
    return check_emu(request)
