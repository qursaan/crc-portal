# howdy/views.py
# from django.core.context_processors import csrf
# from django.contrib.auth import logout

# from manifold.manifoldresult import ManifoldResult
# from django.contrib.auth import logout
#from django.contrib.auth import authenticate, login
#from django.core.files.storage import FileSystemStorage
# from django.core.context_processors import csrf
# from django.http import HttpResponseRedirect
# from django.shortcuts import render
# from django.shortcuts import render_to_response
# from django.template import RequestContext
# from django.views.generic import TemplateView

# from crc.configengine import ConfigEngine
# from portal.models import PhysicalNode
# from manifold.manifoldresult import ManifoldResult
# from ui.topmenu import the_user, topmenu_items  # , topmenu_items_live
# from unfold.loginrequired import FreeAccessView
# from .forms import NameForm
# from manifold.manifoldresult import ManifoldResult
# from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage
# from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView

from crc.configengine import ConfigEngine
from portal.models import PhysicalNode
# from manifold.manifoldresult import ManifoldResult
from ui.topmenu import the_user, topmenu_items  # , topmenu_items_live
from unfold.loginrequired import FreeAccessView
from .forms import NameForm


# from django.views.generic      import View
# from django.http               import Http404, HttpResponse
# from django.template.loader    import get_template
# from django.template           import Context
# from portal.models             import PendingUser
##########################################################################
# Add this view
class AboutPageView(TemplateView):
    template_name = 'about.html'


# class UploadPageView(TemplateView):
#    template_name = 'upload.html'
def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'upload.html', {'form': form})


def simple_upload(request):
   # os.system(
    #    "/usr/share/arduino/hardware/tools/avrdude -C/usr/share/arduino/hardware/tools/avrdude.conf -v -v -v -v -patmega2560 -cwiring -P/dev/ttyACM0 -b115200 -D -V -Uflash:w:/root/crc-portal/crc-portal/media/sketch.hex:i")

    if request.user.is_authenticated:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            #time.sleep(10)
           # os.system("/usr/share/arduino/hardware/tools/avrdude -C/usr/share/arduino/hardware/tools/avrdude.conf -v -v -v -v -patmega2560 -cwiring -P/dev/ttyACM1 -b115200 -D -V -Uflash:w:/root/crc-portal/crc-portal" + uploaded_file_url + ":i")
          #  os.system("/usr/share/arduino/hardware/tools/avrdude -C/usr/share/arduino/hardware/tools/avrdude.conf -v -v -v -v -patmega2560 -cwiring -P/dev/ttyACM0 -b115200 -D -V -Uflash:w:/root/crc-portal/crc-portal" + uploaded_file_url + ":i")

            #/usr/share/arduino/hardware/tools/avrdude -C/usr/share/arduino/hardware/tools/avrdude.conf -v -v -v -v -patmega2560 -cwiring -P/dev/ttyACM1 -b115200 -D -V -Uflash:w:/tmp/build732328322582550757.tmp/Blink.cpp.hex:i
            return render(request, 'upload.html', {'uploaded_file_url': uploaded_file_url})
        return render(request, 'upload.html')
    else:
        render(request, 'index.html')

    # class simple_viewdevices(TemplateView):


def simple_viewdevices(request):
    node_list = PhysicalNode.objects.all()
    if request.method == 'POST':
        if request.POST.get("detail"):
            return render(request, 'devicedetails.html', {'node_list': node_list})
        elif request.POST.get("viewvars"):
            return render(request, 'viewvarstemp.html',)

        return render(request, 'viewdevices.html',
                      {'node_list': node_list})  # return render(request, 'viewdevices.html')
    return render(request, 'viewdevices.html', {'node_list': node_list})  # return render(request, 'viewdevices.html')



