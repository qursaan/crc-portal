__author__ = 'pirate'

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# from portal.actions import get_user_by_email, get_user_type
from lab.actions import add_all_courses_by_email, remove_course_by_emails
from lab.models import StudentCourses
from portal.user_access_profile import UserAccessProfile
from ui.topmenu import topmenu_items  # , the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page


class StudentCoursesView(LoginRequiredAutoLogoutView):
    def post(self, request):
        return self.get_or_post(request, 'POST')

    def get(self, request):
        return self.get_or_post(request, 'GET')

    def get_or_post(self, request, method):
        page = Page(self.request)
        usera = UserAccessProfile(request)
        c_user = usera.user_obj # get_user_by_email(the_user(self.request))
        user_type = usera.user_type # get_user_type(c_user)
        if user_type != 3:
            # messages.error(page.request, 'Error: You have not permission to access this page.')
            return HttpResponseRedirect("/")

        template_name = "std-courses-view.html"
        add_all_courses_by_email(usera.username)
        courses_list = StudentCourses.objects.filter(students_ref=c_user)
        template_env = {
            'topmenu_items': topmenu_items('My Courses', page.request),
            'username': usera.username, #the_user(self.request),
            'courses_list': courses_list,
            'title': 'My Courses',
        }
        template_env.update(page.prelude_env())
        return render(request, template_name, template_env)


@login_required
def student_course_cancel(request, cid):
    course_id = int(cid)
    usera = UserAccessProfile(request)
    #c_user = get_user_by_email(the_user(request))
    user_type = usera.user_type # get_user_type(c_user)
    if user_type != 3:
        # messages.error(page.request, 'Error: You have not permission to access this page.')
        return HttpResponseRedirect("/")

    course = StudentCourses.objects.get(id=course_id)
    remove_course_by_emails(usera.username, course.course_ref.id)
    course.delete()
    messages.success(request, 'Success: Unroll from Course.')
    return HttpResponseRedirect("/lab/my_courses/")

