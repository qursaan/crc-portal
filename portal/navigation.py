from random import randint
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from ui.topmenu import topmenu_items, the_user
from portal.models import UserImage, TestbedImage
from portal.actions import get_user_by_email
from portal.backend_actions import load_images, save_images, vm_restart, vm_shutdown, vm_start, exe_script,check_load_images,check_save_images


#  ********** Non Completed Page ************* #
def un_complete_page(request):
    return render(request, 'uncomplete.html', {
        'topmenu_items': topmenu_items('test_page', request),
        'title': 'TEST PAGE',
    })


# OK OK OK OK
def remote_node(request):
    post_data = ''
    r = 0
    try:
        if request.method == 'POST':
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
            post_data = "Success"
        else:
            post_data = "Fail, Try again!"
    finally:
        request.session['active_page'] = 4
    return HttpResponse(post_data, content_type="text/plain")


# OK OK OK OK
def load_image(request):
    try:
        # auto_save = request.POST.get('autosave','0')
        # node_group = request.POST.getlist('the_node',[])
        node_name = request.POST.get('the_node', '')
        os_id = request.POST.get('the_os', '')
        os_type = request.POST.get('the_type', '')
        if not node_name:
            return HttpResponse("Error: Please select at least one node", content_type="text/plain")

        slice_id = request.session.get('slice_id', '')
        if slice_id is None:
            messages.error(request, 'Error: Unexpected Load your session, Please go back and try again')
            return HttpResponseRedirect('/portal/lab/control/')

        slice_id = int(slice_id)
        os_location = ''
        if os_type == 'base_image':
            os_obj = TestbedImage.objects.get(id=os_id)
            os_location = os_obj.location
        elif os_type == 'user_image':
            os_obj = UserImage.objects.get(id=os_id)
            os_location = os_obj.location

        r = load_images(slice_id, os_location, ".", node_name)
        if r == 1:  # 0:
            return HttpResponse("Start Loading ...", content_type="text/plain")
        else:
            return HttpResponse("Error: Unable to Load image", content_type="text/plain")

    finally:
        request.session['active_page'] = 1
    return HttpResponseRedirect('/portal/lab/control/')


# OK OK OK OK
def save_image(request):
    try:
        user_image_name = request.POST.get('the_image', 'untitled').replace(" ","_")
        node_name = request.POST.get('the_node', '')
        if not node_name:
            messages.error(request, 'Error: Please select at least one node')

        user_name = the_user(request)
        user = get_user_by_email(user_name)

        slice_id = request.session.get('slice_id', '')
        if slice_id is None:
            messages.error(request, 'Error: Unexpected Load your session, Please go back and try again')
            return HttpResponseRedirect('/portal/lab/control/')

        r = save_images(slice_id, user_image_name, ".", node_name)

        if r == 1:
            image_name = user_image_name + "_" + node_name
            update_user_images(image_name, user)
            return HttpResponse("Start Saving ...", content_type="text/plain")
        else:
            return HttpResponse("Error: Unable to Save image", content_type="text/plain")

    finally:
        request.session['active_page'] = 2
    return HttpResponseRedirect('/portal/lab/control/')


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


def check_load(request):
    if "the_post" in request.POST:
        n_id = request.POST.get('the_post')
        ol = check_load_images(n_id)
        if ol != 0:
            return HttpResponse(ol, content_type="application/json")
        else:
            return HttpResponse('{"error": "Error"}', content_type="application/json")
    else:
        return HttpResponse('{"error": "Invalid Id"}', content_type="application/json")


def check_save(request):
    return 0


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
