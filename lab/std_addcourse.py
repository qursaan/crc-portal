__author__ = 'qursaan'

from django.contrib import messages
from django.http import HttpResponseRedirect

from lab.models import StudentCourses, Course
from portal.user_access_profile import UserAccessProfile
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page


# TODO: @qursaan
class StudentAddCourseView(LoginRequiredAutoLogoutView):
    def __init__(self):
        self.user_email = ''
        self.errors = []

    def post(self, request):
        return self.get_or_post(request, 'POST')

    def get(self, request):
        return HttpResponseRedirect("/")

    def get_or_post(self, request, method):
        usera = UserAccessProfile(request)
        self.user_email = usera.username
        page = Page(request)

        if method == 'POST':
            self.errors = []

            user = usera.user_obj # get_user_by_email(the_user(self.request))
            user_type = usera.user_type # get_user_type(user)
            if user_type != 3:
                messages.error(page.request, 'Error: You have not permission to access this page.')
                return HttpResponseRedirect("/")

            course_key = request.POST.get('course_key', '')

            course = Course.objects.filter(key__iexact=course_key)
            if course and not self.errors:
                s = StudentCourses(
                    students_ref=user,
                    course_ref=course[0],
                )
                s.save()
                messages.error(page.request, 'Success: Enroll into a new course')
            else:
                messages.error(page.request, 'Error: Course not exist')

        return HttpResponseRedirect("/lab/my_courses")

