#from django.core.context_processors import csrf
#from django.contrib.auth            import authenticate, login, logout
#from django.template                import RequestContext
#from django.shortcuts               import render_to_response
#from django.template.loader     import get_template
#from django.template            import Context
#from subprocess                 import call
#from subprocess import Popen, PIPE, STDOUT

import subprocess
from random         import randint
from django.utils   import timezone
#
from django.http       import HttpResponseRedirect # Http404, HttpResponse
from django.shortcuts  import render
from django.contrib    import messages
from ui.topmenu        import topmenu_items, the_user
#
from portal.models import UserImage, PendingSlice  #, Node
from portal.actions import get_user_by_email
from portal.backend_actions import load_images,vm_restart,vm_shutdown,vm_start, exe_script

#  ********** Non Completed Page ************* #
def un_complete_page(request):
    return render(request, 'uncomplete.html', {
        'topmenu_items': topmenu_items('test_page', request),
        'title': 'TEST PAGE',
        })



"""def check_node(node_id):
    t = -1
    try:
        t = subprocess.check_output(["sshpass","-p","CRC123","ssh","-o","StrictHostKeyChecking=no","crc-am@10.0.0.200","echo CRC123 | sudo -S ./getNodeStatus.sh node"+str(node_id)])
        print t
    finally:
        return t
"""


def remote_node(request):
    try:
        if request.method == 'POST':
            node_name = request.POST.get('node_group','')
            if not node_name:
                messages.error(request, 'Error: Please select at least one node')
            r = 0
            if "b_restart" in request.POST:
                r = vm_restart(node_name)
            elif "b_shutdown" in request.POST:
                r = vm_shutdown(node_name)
            elif "b_start" in request.POST:
                r = vm_start(node_name)

            if r == 1:
                messages.success(request, 'Success: action')
            else:
                messages.error(request, 'Error: Unable to do action')
    finally:
        request.session['active_page'] = 1
    return HttpResponseRedirect('/portal/lab/control/')



def load_image(request):
    try:
        #auto_save = request.POST.get('autosave','0')
        node_group = request.POST.getlist('node_group',[])
        os_location = request.POST.get('osimage','')
        if not node_group:
            messages.error(request, 'Error: Please select at least one node')

        ##TODO: update
        slice_id = request.session.get('slice_id','')
        if slice_id is None:
            messages.error(request, 'Error: Unexpected Load your session, Please go back and try againg')
            return HttpResponseRedirect('/portal/lab/control/')

        slice_id = int(slice_id)
        #current_slice = PendingSlice.objects.get(id=slice_id)
        #time_diff = current_slice.end_time - timezone.now()
        #rem_time = time_diff.total_seconds()
        #username = request.user.email.replace("@", "_").replace(".","_")
        #password = request.user.email

        r = load_images(slice_id, os_location, ".", node_group)
        #r = load_images(','.join(repr(e) for e in node_group), os_location,str(rem_time),auto_save,username,password)
        if r == 1: #0:
            messages.success(request, 'Success: Loading of image(s)')
        else:
            messages.error(request, 'Error: Unable to Load image(s)')
    finally:
        request.session['active_page'] = 1
    return HttpResponseRedirect('/portal/lab/control/')

"""
def load_images(node_lst,image_name,rem_time,auto_save,username,password):
    t = -1
    #u = -1
    try:
        node_lst = node_lst.replace("'","").replace("u","")
        t = subprocess.call(["sshpass","-p","CRC123","ssh","-o","StrictHostKeyChecking=no","crc-am@10.0.0.200","echo CRC123 | sudo -S ./omf_load.sh", node_lst, image_name ])
        #u = subprocess.call(["sshpass","-p","CRC123","ssh","-o","StrictHostKeyChecking=no","crc-am@10.0.0.200","echo CRC123 | sudo -S ./waitForEnd.sh", rem_time, username, password ])
        print t#, u
    finally:
        return t#+u
"""

def save_image(request):
    user_image_name = request.POST.get('image_name','untitled')
    node_group = request.POST.getlist('node_group',[])
    if not node_group:
        messages.error(request, 'Error: Please select at least one node')

    user_name = the_user(request)
    user = get_user_by_email(user_name)
    try:
        result = save_images(' ,'.join(repr(e) for e in node_group), user_image_name)
        if result != 0:
            messages.error(request, 'Error: Unexpected error while save image')
            return HttpResponseRedirect('/portal/lab/control/')
        else:
            messages.success(request, 'Success: Save of image')

            for node_name in node_group:
                ## TODO:
                #image_time = timezone.now().strftime('[%X %d %M %Y]') #"_"+image_time+
                image_name = user_image_name+ "_" +node_name
                update_user_images(image_name,user )
    except:
        messages.error(request, 'Error: Unexpected error while save image')
    finally:
        request.session['active_page'] = 2
    return HttpResponseRedirect('/portal/lab/control/')



def save_images(node_lst,image_name):
    t = -1
    try:
        node_lst = node_lst.replace("'","").replace("u","")
        t = subprocess.call(["sshpass", "-p", "CRC123", "ssh", "-o", "StrictHostKeyChecking=no", "crc-am@10.0.0.200","echo CRC123 | sudo -S ./omf_save.sh",node_lst,image_name])
        print t
    except:
        return -1
    finally:
        return t


def update_user_images(image_name, user):
    try:
        new_image = UserImage(
            user_ref     = user,
            image_name   = image_name,
            location     = image_name+".ndz",
        )
        new_image.save()
    except:
        return False
    return True


def omf_exe(request):
    script = request.POST.get('script_text', '')
    #ctx = {'script': script}
    #file = render_to_string('omf_script.rb', ctx)
    #savefile
    file_name = str(randint(1, 1000000)) +".rb"
    text_file = open(file_name, "w")
    text_file.write("%s" % script)
    text_file.close()
    t = exe_script(file_name)
    messages.success(request, 'Success: Send Script')
    request.session['active_page'] = 3
    request.session['output'] = t
    return HttpResponseRedirect('/portal/lab/control/')

"""
def omf_execute(filename):
    t = -1
    try:
        subprocess.call(["sshpass", "-p", "CRC123", "scp", filename, "crc-am@10.0.0.200:~"])
        t = subprocess.check_output(["sshpass", "-p", "CRC123", "ssh", "-o", "StrictHostKeyChecking=no",
                                     "crc-am@10.0.0.200", "echo CRC123 | sudo -S omf_ec -u amqp://10.0.0.200 exec --oml_uri tcp:10.0.0.200:3003",filename])
        print t
    finally:
        return t


import sys
p = subprocess.Popen(["python printandwait.py"], shell=True, stdout=subprocess.PIPE)
while True:
    print "Looping"
    line = p.stdout.readline()
    if not line:
        break
    print line.strip()
    sys.stdout.flush()"""
