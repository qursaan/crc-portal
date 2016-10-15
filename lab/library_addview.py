__author__ = 'qursaan'
import os
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from lab.models import CustomLibrary
from portal.actions import get_user_by_email, get_user_type
from ui.topmenu import topmenu_items, the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page


class AddLibraryView(LoginRequiredAutoLogoutView):
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

        user = get_user_by_email(the_user(request))
        user_type = get_user_type(user)
        if 0 <= user_type <= 3:
            messages.error(page.request, 'Error: You have not permission to access this page.')
            return HttpResponseRedirect("/")

        if method == 'POST':
            self.errors = []

            lib_name = request.POST.get('lib_name', None)
            lib_auth = request.POST.get('lib_auth', None)
            lib_type = request.POST.get('lib_type', None)
            lib_type_other = request.POST.get('lib_type_other', None)
            lib_tag = request.POST.get('lib_tag', None)
            lib_link = request.POST.get('lib_link', None)
            lib_desc = request.POST.get('lib_desc', None)
            lib_file = None
            request_date = timezone.now()
            if len(request.FILES) > 0:
                lib_file = request.FILES['lib_file']

            if lib_name is None or lib_name == '':
                self.errors.append('Library Name is mandatory')
            if lib_file is None or lib_file == '':
                self.errors.append('Code file is mandatory')
            if lib_type is None or lib_type == '':
                self.errors.append('Code type is mandatory')
            if lib_type == 'Other' and (lib_type_other is None or lib_type_other == ''):
                self.errors.append('Code type is mandatory')

            if not self.errors:
                if lib_type == 'Other':
                    lib_type = ''.join(e for e in lib_type_other if e.isalnum())
                c = CustomLibrary(
                    user_ref=user,
                    name=lib_name,
                    author=lib_auth,
                    type=lib_type,
                    tag=lib_tag,
                    external_link=lib_link,
                    description=lib_desc,
                )
                sv_library = c.save()

                # if sv_library:
                # Save file and update
                if lib_file:
                    fs = FileSystemStorage(location='media/' + lib_type + '/')
                    new_filename = user.username + "_" + request_date.strftime('%d_%m_%Y') + "_" + lib_file.name
                    # directory = os.path.join(fs.location, lib_type)
                    if not os.path.exists(fs.location):
                        os.makedirs(fs.location)
                    filename = fs.save(new_filename, lib_file)
                    uploaded_file_url = fs.url(lib_type + '/' + filename)
                    c.file = uploaded_file_url
                    sv_library = c.save()
                    # if not sv_library:
                    # c.delete()
                    # messages.error(page.request, 'Error: Cannot Upload file')

                    messages.success(page.request, 'Success: Add new course')
                    return HttpResponseRedirect("/lab/library")

                c.delete()
                messages.error(page.request, 'Error: Saving Library')

        template_env = {
            'topmenu_items': topmenu_items('Add new library', page.request),
            'username': the_user(request),
            'errors': self.errors,
            'title': "Add New Library"
        }
        template_env.update(page.prelude_env())
        return render(request, 'library-add.html', template_env)
