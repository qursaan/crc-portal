__author__ = 'qursaan'

"""from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from lab.models import Course
from portal.actions import get_user_by_email, get_user_type
from ui.topmenu import topmenu_items, the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page


# TODO: @qursaan


class AddExperimentView(LoginRequiredAutoLogoutView):
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
        user = get_user_by_email(the_user(self.request))
        courses_list = Course.objects.filter(instructor_ref=user)

        if method == 'POST':
            self.errors = []

            user_type = get_user_type(user)
            if user_type != 2:
                messages.error(page.request, 'Error: You have not permission to access this page.')
                return HttpResponseRedirect("/")

            if not self.errors:
                s = Course(
                    instructor_ref=user,
                    title=course_title,
                    code=course_code,
                    key=course_key,
                    description=course_detail,
                    max_students=course_max,
                )
                s.save()
                messages.error(page.request, 'Success: Add new course')
                return HttpResponseRedirect("/lab/courses")

        template_env = {
            'topmenu_items': topmenu_items('Add an Experiment', page.request),
            'username': the_user(request),
            'errors': self.errors,
            'ex_title': request.POST.get('course_title', ''),
            'ex_courses_list': courses_list,
            'ex_detail': request.POST.get('ex_detail', ''),
            'title': "Add New Experiment"
        }
        template_env.update(page.prelude_env())
        return render(request, 'ins-experiments-add.html', template_env)
"""