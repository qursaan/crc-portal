__author__ = 'pirate'

# from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render

from lab.models import StudentCourses, Course, Experiments, StudentsExperiment
# from portal.actions import get_user_by_email, get_user_type
from portal.user_access_profile import UserAccessProfile
from ui.topmenu import topmenu_items  # , the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page


class StudentExperimentsView(LoginRequiredAutoLogoutView):
    def post(self, request):
        return self.get_or_post(request, 'POST')

    def get(self, request):
        return self.get_or_post(request, 'GET')

    def get_or_post(self, request, method):
        page = Page(self.request)
        usera = UserAccessProfile(request)
        c_user = usera.user_obj #get_user_by_email(the_user(self.request))
        user_type = usera.user_type #get_user_type(c_user)
        if user_type != 3:
            # messages.error(page.request, 'Error: You have not permission to access this page.')
            return HttpResponseRedirect("/")

        template_name = "std-experiments-view.html"
        s_courses_list = StudentCourses.objects.filter(students_ref=c_user)

        c_ids = []

        for c in s_courses_list:
            c_ids.append(c.course_ref.id)

        courses_list = Course.objects.filter(id__in=c_ids)
        exp_list = Experiments.objects.filter(course_ref__in=courses_list, status=0)

        res_exp_list = Experiments.objects.filter(course_ref__in=courses_list)
        std_exp_list = StudentsExperiment.objects.filter(students_ref=c_user, experiment_ref__in=res_exp_list)

        res_std_list_id = []
        for s in std_exp_list:
            res_std_list_id.append(s.experiment_ref.id)

        exp_list = exp_list.exclude(id__in=res_std_list_id)

        template_env = {
            'topmenu_items': topmenu_items('My Courses', page.request),
            'username': usera.username,
            'exp_list': exp_list,
            'std_exp_list': std_exp_list,
            'title': 'My Courses',
        }
        template_env.update(page.prelude_env())
        return render(request, template_name, template_env)
