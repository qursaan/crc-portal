__author__ = 'pirate'

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from lab.models import CustomLibrary
# from portal.actions import get_user_by_email, get_user_type
from portal.user_access_profile import UserAccessProfile
from ui.topmenu import topmenu_items  # , the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page


class LibraryView(LoginRequiredAutoLogoutView):
    def post(self, request):
        return self.get_or_post(request, 'POST')

    def get(self, request):
        return self.get_or_post(request, 'GET')

    def get_or_post(self, request, method):
        page = Page(self.request)
        usera = UserAccessProfile(self.request)
        c_user = usera.user_obj # get_user_by_email(the_user(self.request))
        user_type = usera.user_type # get_user_type(c_user)
        if user_type > 3:
            messages.error(page.request, 'Error: You have not permission to access this page.')
            return HttpResponseRedirect("/")
        lib_list = None
        lib_name = request.POST.get('lib_name', '')
        lib_auth = request.POST.get('lib_auth', '')
        lib_type = request.POST.get('lib_type', '')
        lib_tag = request.POST.get('lib_tag', '')
        lib_desc = request.POST.get('lib_desc', '')

        if method == 'POST':
            lib_list = CustomLibrary.objects.filter(name__icontains=lib_name, author__icontains=lib_auth,
                                                    type__icontains=lib_type, tag__icontains=lib_tag,
                                                    description__icontains=lib_desc)

        else:
            lib_list = CustomLibrary.objects.all()

        template_name = "library-view.html"
        template_env = {
            'topmenu_items': topmenu_items('Library List', page.request),
            # 'errors': errors,
            'lib_list': lib_list,
            'lib_name': lib_name,
            'lib_auth': lib_auth,
            'lib_type': lib_type,
            'lib_tag': lib_tag,
            'lib_desc': lib_desc,
            'username': usera.username, # the_user(self.request),
            'title': 'Custom Libraries',
        }
        template_env.update(page.prelude_env())
        return render(request, template_name, template_env)


from django.http import HttpResponse
from crc import settings
import os
import mimetypes
from wsgiref.util import FileWrapper

def download(request, file_name):
    file_path = settings.HTTPROOT +'/'+ file_name
    file_wrapper = FileWrapper(open(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s/' % os.path.basename(file_path)
    return response