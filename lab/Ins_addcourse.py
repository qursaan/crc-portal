__author__ = 'qursaan'

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from lab.models import Course, StudentCourses
from lab.actions import add_course_by_email
from portal.actions import get_user_by_email, get_user_type
from ui.topmenu import topmenu_items, the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page


# TODO: @qursaan


class AddCourseView(LoginRequiredAutoLogoutView):
    def __init__(self):
        self.user_email = ''
        self.errors = []

    def post(self, request, cid=None):
        return self.get_or_post(request, 'POST', cid)

    def get(self, request, cid=None):
        return self.get_or_post(request, 'GET', cid)

    def get_or_post(self, request, method, course_id):
        self.user_email = the_user(request)
        page = Page(request)

        course_title = ''
        course_key = ''
        course_detail = ''
        course_max = ''
        course_code = ''
        course_emails = ''

        if method == 'GET' and course_id:
            c = Course.objects.get(id=course_id)
            if c:
                course_title = c.title
                course_key = c.key
                course_detail = c.description
                course_max = c.max_students
                course_code = c.code
                course_emails = c.email_list

        if method == 'POST':
            self.errors = []

            course_title = request.POST.get('course_title', '')
            course_key = request.POST.get('course_key', '')
            course_detail = request.POST.get('course_detail', '')
            course_max = request.POST.get('course_max', '')
            course_code = request.POST.get('course_code', '')
            course_emails = request.POST.get('course_emails', '')

            user = get_user_by_email(the_user(self.request))
            user_type = get_user_type(user)
            if user_type != 2:
                messages.error(page.request, 'Error: You have not permission to access this page.')
                return HttpResponseRedirect("/")

            if course_title is None or course_title == '':
                self.errors.append('Course title is mandatory')
            if course_key is None or course_key == '':
                self.errors.append('Course key is mandatory')

            if not self.errors:
                sv_course = False

                if not course_id:
                    c = Course(
                        instructor_ref=user,
                        title=course_title,
                        code=course_code,
                        key=course_key,
                        description=course_detail,
                        max_students=course_max,
                        email_list=course_emails,
                    )
                    sv_course = c.save()
                else:
                    c = Course.objects.get(id=course_id)
                    if c:
                        c.title = course_title
                        c.code = course_code
                        c.key = course_key
                        c.description = course_detail
                        c.max_students = course_max
                        c.email_list = course_emails
                        sv_course = c.save()
                #if sv_course:
                    # look for add student already register
                    s_email = [x.strip() for x in course_emails.split(',')]
                    for se in s_email:
                        add_course_by_email(c, se)

                messages.error(page.request, 'Success: Add new course')
                return HttpResponseRedirect("/lab/courses")
                # template_env = {
                #    'topmenu_items': topmenu_items('Add a course', page.request),
                #    'username': the_user(request),
                #    'title': "Add New Course",
                # }
                # template_env.update(page.prelude_env())
                # return render(request, 'courses-add.html', template_env)  # Redirect after POST

        template_env = {
            'topmenu_items': topmenu_items('Add a course', page.request),
            'username': the_user(request),
            'errors': self.errors,
            'course_title': course_title,
            'course_key': course_key,
            'course_code': course_code,
            'course_detail': course_detail,
            'course_max': course_max,
            'course_emails': course_emails,
            'title': "Add New Course"
        }
        template_env.update(page.prelude_env())
        return render(request, 'ins-courses-add.html', template_env)

