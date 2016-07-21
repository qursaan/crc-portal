__author__ = 'qursaan'

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from lab.models import Course
from portal.actions import get_user_by_email , get_user_type
from ui.topmenu import topmenu_items, the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page


# TODO: @qursaan


class AddCourseView(LoginRequiredAutoLogoutView):
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

        if method == 'POST':
            self.errors = []

            user = get_user_by_email(the_user(self.request))
            user_type = get_user_type(user)
            if user_type != 2:
                messages.error(page.request, 'Error: You have not permission to access this page.')
                return HttpResponseRedirect("/")

            course_title = request.POST.get('course_title', '')
            course_key = request.POST.get('course_key', '')
            course_detail = request.POST.get('course_detail', '')
            course_max = request.POST.get('course_max', '')
            course_code = request.POST.get('course_code', '')

            if course_title is None or course_title == '':
                self.errors.append('Course title is mandatory')
            if course_key is None or course_key == '':
                self.errors.append('Course key is mandatory')

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
                #template_env = {
                #    'topmenu_items': topmenu_items('Add a course', page.request),
                #    'username': the_user(request),
                #    'title': "Add New Course",
                #}
                #template_env.update(page.prelude_env())
                #return render(request, 'courses-add.html', template_env)  # Redirect after POST

        template_env = {
            'topmenu_items': topmenu_items('Add a course', page.request),
            'username': the_user(request),
            'errors': self.errors,
            'course_title': request.POST.get('course_title', ''),
            'course_key': request.POST.get('course_key', ''),
            'course_code': request.POST.get('course_code', ''),
            'course_detail': request.POST.get('course_detail', ''),
            'course_max': request.POST.get('course_max', ''),
            'title': "Add New Course"
        }
        template_env.update(page.prelude_env())
        return render(request, 'ins-courses-add.html', template_env)
