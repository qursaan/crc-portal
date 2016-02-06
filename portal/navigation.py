from random import randint
#
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.utils import timezone
#
from ui.topmenu import topmenu_items, the_user
from portal.models import UserImage, TestbedImage,Reservation, SimReservation
from portal.actions import get_user_by_email, get_task_id, update_task_testbed, check_next_task_duration
from portal.backend_actions import load_images, save_images, vm_restart, vm_shutdown, vm_start, exe_script,check_load_images,check_save_images


#  ********** Non Completed Page ************* #
def un_complete_page(request):
    return render(request, 'uncomplete.html', {
        'topmenu_items': topmenu_items('test_page', request),
        'title': 'TEST PAGE',
    })


# OK OK OK OK
def remote_node(request):
    if not slice_on_time(request):
        return HttpResponse('eof', content_type="text/plain")
    else:
        node_name = request.POST.get('the_node', '')
        action_name = request.POST.get('the_action', '')
        if not node_name:
            messages.error(request, 'Error: Please select at least one node')

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
    if not slice_on_time(request):
        return HttpResponse('eof', content_type="text/plain")
    # for any action  ##########
    node_name = request.POST.get('the_node', None)
    if not node_name:
        return HttpResponse("error: Please select at least one node", content_type="text/plain")

    slice_id = request.session.get('slice_id', None)
    if slice_id is None:
        messages.error(request, 'error: Unexpected Load your session, Please go back and try again')
        return HttpResponseRedirect('/portal/lab/control/')

    slice_id = int(slice_id)
    task_id = get_task_id(slice_id, node_name)
    if task_id:
        if not check_next_task_duration(task_id):
            return HttpResponse('warning: wait 5 min before next try', content_type="text/plain")

    # end for any action ###########
        r = 0
        # for load action ###########
        if action == 'load':
            os_id = request.POST.get('the_os', '')
            os_type = request.POST.get('the_type', '')
            os_location = ''
            if os_type == 'base_image':
                os_obj = TestbedImage.objects.get(id=os_id)
                os_location = os_obj.location
            elif os_type == 'user_image':
                os_obj = UserImage.objects.get(id=os_id)
                os_location = os_obj.location
            r = load_images(task_id, os_location, ".", node_name)
            if r == 1:
                update_task_testbed(task_id, action)

        # for save action ###########
        elif action == 'save':
            user_image_name = request.POST.get('the_image', 'untitled').replace(" ", "_")
            user_name = the_user(request)
            user = get_user_by_email(user_name)
            r = save_images(slice_id, user_image_name, ".", node_name)
            if r == 1:
                image_name = user_image_name + "_" + node_name
                update_user_images(image_name, user)
                update_task_testbed(task_id, action)

        # for any action  ##########
        if r == 1:
            return HttpResponse('success: '+action+' ...', content_type="text/plain")
    return HttpResponse('error: Unable to '+action+' image', content_type="text/plain")


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

    if current_slice is None or current_slice.status != 3:
        messages.success(request, 'Error: You have not permission to access this page.')
        del request.session['slice_id']
        return False
    if current_slice.end_time < timezone.now():
        del request.session['slice_id']
        current_slice.status = 4
        current_slice.save()
        messages.success(request, 'Error: Slice time has been expired. ')
        return False
    return True


# OK OK OK OK
"""def save_image(request):
    user_image_name = request.POST.get('the_image', 'untitled').replace(" ", "_")

    node_name = request.POST.get('the_node', None)
    if not node_name:
        return HttpResponse("error: Please select at least one node", content_type="text/plain")

    slice_id = request.session.get('slice_id', None)
    if slice_id is None:
        messages.error(request, 'error: Unexpected Load your session, Please go back and try again')
        return HttpResponseRedirect('/portal/lab/control/')

    user_name = the_user(request)
    user = get_user_by_email(user_name)

    r = save_images(slice_id, user_image_name, ".", node_name)

    if r == 1:
        image_name = user_image_name + "_" + node_name
        update_user_images(image_name, user)
        return HttpResponse("Start Saving ...", content_type="text/plain")
    else:
        return HttpResponse("Error: Unable to Save image", content_type="text/plain")"""


# OK OK OK OK
def update_user_images(image_name, user):
    try:
        new_image = UserImage(
            user_ref=user,
            image_name=image_name,
            location=image_name + ".ndz",
        )
        new_image.save()
    except:
        return False
    return True


# action[Load,save]
def check_task_progress(request, action):
    node_name = request.POST.get('the_node', None)
    slice_id = request.session.get('slice_id', None)
    if slice_id and node_name:
        tid = get_task_id(slice_id, node_name)
        ol = None
        if action == "load":
            ol = check_load_images(tid)
        elif action == "save":
            ol = check_save_images(tid)
        if ol != 0:
            return HttpResponse(ol, content_type="application/json")
    return HttpResponse('{"error": "Error, Invalid Id"}', content_type="application/json")



def omf_exe(request):
    script = request.POST.get('script_text', '')
    # ctx = {'script': script}
    # file = render_to_string('omf_script.rb', ctx)
    # savefile
    file_name = str(randint(1, 1000000)) + ".rb"
    text_file = open(file_name, "w")
    text_file.write("%s" % script)
    text_file.close()
    t = exe_script(file_name)
    messages.success(request, 'Success: Send Script')
    request.session['active_page'] = 3
    request.session['output'] = t
    return HttpResponseRedirect('/portal/lab/control/')


