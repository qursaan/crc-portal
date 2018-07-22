__author__ = 'pirate'

from django.shortcuts import render
from django.contrib import messages
from ui.topmenu import topmenu_items#, the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page
from django.contrib.auth.decorators import login_required
#
from django.utils import timezone
from django.http import HttpResponseRedirect
#from portal.actions import get_user_by_email, get_user_type
from portal.models import MyUser
from portal.user_access_profile import UserAccessProfile


class ManageStudentView(LoginRequiredAutoLogoutView):
    def post(self, request):
        return self.get_or_post(request, 'POST')

    def get(self, request):
        return self.get_or_post(request, 'GET')

    def get_or_post(self, request, method):
        page = Page(self.request)
        usera = UserAccessProfile(request)
        c_user = usera.user_obj
        user_type = usera.user_type
        if user_type != 2:
            messages.error(page.request, 'Error: You have not permission to access this page.')
            return HttpResponseRedirect("/")

        template_name = "ins_students_manage.html"
        student_list = MyUser.objects.filter(supervisor_id=c_user.id, user_type=3)
        template_env = {
            'topmenu_items': topmenu_items('Students List', page.request),
            # 'errors': errors,
            'username': usera.username, #the_user(self.request),
            'student_list': student_list,
            'time_now': timezone.now,
            'title': 'Current Students',
        }
        template_env.update(page.prelude_env())
        return render(request, template_name, template_env)


@login_required
def student_disable(request, sid):
    s_id = int(sid)
    usera = UserAccessProfile(request)
    #c_user = get_user_by_email(the_user(request))
    user_type = usera.user_type #get_user_type(c_user)
    if user_type != 2:
        messages.error(request, 'Error: You have not permission to access this page.')
        return HttpResponseRedirect("/")
    std_obj = MyUser.objects.get(id=s_id)
    std_obj.status = 0
    std_obj.save()
    messages.success(request, 'Success: Update User.')
    return HttpResponseRedirect("/lab/students/")


@login_required
def student_enable(request, sid):
    s_id = int(sid)
    usera = UserAccessProfile(request)
    #c_user = get_user_by_email(the_user(request))
    user_type = usera.user_type #get_user_type(c_user)
    if user_type != 2:
        messages.error(request, 'Error: You have not permission to access this page.')
        return HttpResponseRedirect("/")
    std_obj = MyUser.objects.get(id=s_id)
    std_obj.status = 2
    std_obj.save()
    messages.success(request, 'Success: Update User.')
    return HttpResponseRedirect("/lab/students/")
