from random import randint
#
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.utils import timezone
#
from crc.settings import BASE_IMAGE_DIR
from ui.topmenu import topmenu_items, the_user
from portal.models import UserImage, TestbedImage, Reservation, SimReservation, SimulationImage
from portal.actions import get_user_by_email, get_task_id, update_task_testbed, check_next_task_duration, \
    get_username_by_email
from portal.backend_actions import load_images, save_images, vm_restart, vm_shutdown, vm_start, exe_script, exe_check, \
    check_load_images, check_save_images, exe_abort, commlab_exe, commlab_check, commlab_result
from reservation_status import ReservationStatus


#  ********** Non Completed Page ************* #
def un_complete_page(request):
    return render(request, 'uncomplete.html', {
        'topmenu_items': topmenu_items('test_page', request),
        'title': 'TEST PAGE',
    })


# OK OK OK OK
def remote_node(request):
    stype = request.POST.get('stype', None);
    if stype is None:
        return HttpResponse("error: Please go back and try again", content_type="text/plain")

    if not slice_on_time(request, stype):
        return HttpResponse('eof', content_type="text/plain")
    else:
        node_name = request.POST.get('the_node', '')
        action_name = request.POST.get('the_action', '')
        if not node_name:
            return HttpResponse(request, 'error: Please select at least one node', content_type="text/plain")

        if action_name == "Restart":
            r = vm_restart(node_name)
        elif action_name == "Shutdown":  # in request.POST:
            r = vm_shutdown(node_name)
        elif action_name == "Start":  # in request.POST:
            r = vm_start(node_name)

        if r == 1:
            return HttpResponse("success", content_type="text/plain")
    return HttpResponse("Fail, Try again!", content_type="text/plain")


# OK OK OK OK
def action_load_save_image(request, action):
    stype = request.POST.get('stype', None)
    if stype is None:
        return HttpResponse("error: Please go back and try again", content_type="text/plain")

    if not slice_on_time(request, stype):
        return HttpResponse('eof', content_type="text/plain")
    # for any action  ############# TODO: @qursaan

    node_name = None
    if action == 'load':
        node_name = request.POST.getlist('the_node[]', None)
    else:  # Save
        node_name = request.POST.get('the_node', None)

    if not node_name:
        return HttpResponse("error: Please select at least one node", content_type="text/plain")

    slice_id = request.session.get('slice_id', None)
    if slice_id is None:
        return HttpResponse("error: Please go back and try again")

    slice_id = int(slice_id)
    task_id = None
    task_id_list = None
    if action == 'load':
        task_id_list = []
        for n in node_name:
            task_id = str(get_task_id(slice_id, n, stype))
            task_id_list.append(task_id)
    else:  # Save
        task_id = get_task_id(slice_id, node_name, stype)

    if task_id:
        if not check_next_task_duration(task_id, stype):
            return HttpResponse('warning: wait 5 min before next try', content_type="text/plain")

        # end for any action ###########
        r = 0
        # if stype == 'omf':
        # for load action ###########
        if action == 'load':
            os_id = request.POST.get('the_os', '')
            os_type = request.POST.get('the_type', '')
            os_location = ''
            os_obj = None

            if os_type == 'base_image':
                if stype == 'omf':
                    os_obj = TestbedImage.objects.get(id=os_id)
                elif stype == 'sim':
                    os_obj = SimulationImage.objects.get(id=os_id)

            elif os_type == 'user_image':
                os_obj = UserImage.objects.get(id=os_id)

            if os_obj:
                os_location = os_obj.location

            r = load_images(task_id_list, os_location, ".", node_name)
            if r == 1:
                for t in task_id_list:
                    update_task_testbed(t, action, stype)
        # for save action ###########
        elif action == 'save':
            user_image_name = request.POST.get('the_image', 'untitled').replace(" ", "_")
            if user_image_name == '':
                user_image_name = "untitled"
            user_name = the_user(request)
            user = get_user_by_email(user_name)
            r = save_images(task_id, user_image_name, ".", node_name)
            if r == 1:
                image_name = user_image_name + "_" + node_name
                update_user_images(image_name, user)
                update_task_testbed(task_id, action, stype)

        # for any action  ##########
        if r == 1:
            return HttpResponse('success: start ' + action + ' ...', content_type="text/plain")
    return HttpResponse('error: Unable to ' + action + ' image', content_type="text/plain")


# OK OK OK OK
def slice_on_time(request, stype):
    slice_id = request.session.get('slice_id', None)
    if not slice_id:
        return False
    slice_id = int(slice_id)
    current_slice = None
    if stype == "omf":
        current_slice = Reservation.objects.get(id=slice_id)
    elif stype == "sim":
        current_slice = SimReservation.objects.get(id=slice_id)

    if current_slice is None or current_slice.status != ReservationStatus.get_active():
        messages.success(request, 'Error: You have not permission to access this page.')
        del request.session['slice_id']
        return False
    if current_slice.end_time < timezone.now():
        del request.session['slice_id']
        current_slice.status = ReservationStatus.get_expired()
        current_slice.save()
        messages.success(request, 'Error: Slice time has been expired. ')
        return False
    return True


# OK OK OK OK
def update_user_images(image_name, user):
    try:
        new_image = UserImage(
            user_ref=user,
            image_name=image_name,
            location=BASE_IMAGE_DIR + image_name + ".ndz",
        )
        new_image.save()
    except:
        return False
    return True


# action[Load,save]
def check_task_progress(request, action):
    stype = request.POST.get('stype', None);
    node_name = request.POST.get('the_node', None)
    slice_id = request.session.get('slice_id', None)
    if stype and slice_id and node_name:
        tid = get_task_id(slice_id, node_name, stype)
        ol = None
        if action == "load":
            ol = check_load_images(tid)
        elif action == "save":
            ol = check_save_images(tid)
        if ol != 0:
            return HttpResponse(ol, content_type="application/json")
    return HttpResponse('{"error": "Error, Invalid Id"}', content_type="application/json")


def check_exe_progress(request):
    exe_id = request.POST.get('the_eid', None)
    if exe_id:
        ol = exe_check(exe_id)
        if ol != 0:
            return HttpResponse(ol, content_type="application/json")
    return HttpResponse('{"error": "Error, Invalid File"}', content_type="application/json")


def abort_exe_progress(request):
    if not slice_on_time(request, "omf"):
        return HttpResponse('eof', content_type="text/plain")
    else:
        exe_id = request.POST.get('the_eid', None)
        if exe_id:
            ol = exe_abort(exe_id)
            if ol != 0:
                return HttpResponse("success: Execution Aborted", content_type="text/plain")
        return HttpResponse("error, Failed to cancel experiment", content_type="text/plain")


def omf_exe(request):
    if not slice_on_time(request, "omf"):
        return HttpResponse('eof', content_type="text/plain")
    else:
        script = request.POST.get('script_text', '')
        if not script:
            return HttpResponse(request, 'Script Empty', content_type="text/plain")

        username = get_username_by_email(the_user(request))
        t = exe_script("%s" % script, username)
        if t != 0:
            return HttpResponse(t, content_type="application/json")
        return HttpResponse({"error": "Error, Invalid Script"}, content_type="text/plain")


def lab_run(request):
    if not slice_on_time(request, "omf"):
        return HttpResponse('eof', content_type="text/plain")
    else:

        t = commlab_exe(request.POST)
        if t != 0:
            return HttpResponse(t, content_type="application/json")
        return HttpResponse({"error": "Error, Invalid Script"}, content_type="text/plain")


def lab_check(request):
    exe_id = request.POST.get('the_eid', None)
    if exe_id:
        ol = commlab_check(exe_id)
        if ol != 0:
            return HttpResponse(ol, content_type="application/json")
    return HttpResponse('{"error": "Error, Invalid File"}', content_type="application/json")


def lab_result(request):
    exe_id = request.POST.get('the_eid', None)
    if exe_id:
        ol = commlab_result(exe_id)
        if ol != 0:
            return HttpResponse(ol, content_type="text/plain")
    return HttpResponse('{"error": "Error, Invalid File"}', content_type="application/json")