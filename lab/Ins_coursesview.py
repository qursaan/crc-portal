__author__ = 'pirate'

from django.shortcuts import render
from django.contrib import messages
from ui.topmenu import topmenu_items, the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page

#
from django.utils import timezone
from django.http import HttpResponseRedirect
from portal.actions import get_user_by_email, get_user_type
from lab.models import Course


class CoursesView(LoginRequiredAutoLogoutView):
    def post(self, request):
        return self.get_or_post(request, 'POST')

    def get(self, request):
        return self.get_or_post(request, 'GET')

    def get_or_post(self, request, method):
        page = Page(self.request)

        c_user = get_user_by_email(the_user(self.request))
        user_type = get_user_type(c_user)
        if user_type != 2:
            messages.error(page.request, 'Error: You have not permission to access this page.')
            return HttpResponseRedirect("/")

        template_name = "ins-courses-view.html"
        courses_list = Course.objects.filter(instructor_ref=c_user)
        template_env = {
            'topmenu_items': topmenu_items('Courses List', page.request),
            # 'errors': errors,
            'username': the_user(self.request),
            'courses_list': courses_list,
            'time_now': timezone.now,
            'title': 'Current Active Courses',
        }
        template_env.update(page.prelude_env())
        return render(request, template_name, template_env)
