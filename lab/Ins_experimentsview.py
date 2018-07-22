__author__ = 'pirate'

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# from portal.actions import get_user_by_email, get_user_type
from lab.models import Experiments
from portal.user_access_profile import UserAccessProfile
from ui.topmenu import topmenu_items  # , the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page


class ExperimentsView(LoginRequiredAutoLogoutView):
    def post(self, request):
        return self.get_or_post(request, 'POST')

    def get(self, request):
        return self.get_or_post(request, 'GET')

    def get_or_post(self, request, method):
        page = Page(self.request)
        usera = UserAccessProfile(request)
        c_user = usera.user_obj #get_user_by_email(the_user(self.request))
        user_type = usera.user_type #get_user_type(c_user)
        if user_type != 2:
            messages.error(page.request, 'Error: You have not permission to access this page.')
            return HttpResponseRedirect("/")

        template_name = "ins-experiments-view.html"
        # courses_list = Course.objects.filter(instructor_ref=c_user)

        exp_list = Experiments.objects.filter(course_ref__instructor_ref=c_user)

        template_env = {
            'topmenu_items': topmenu_items('Experiments List', page.request),
            # 'errors': errors,
            'username': usera.username, #the_user(self.request),
            'exp_list': exp_list,
            'title': 'Current Experiments',
        }
        template_env.update(page.prelude_env())
        return render(request, template_name, template_env)


@login_required
def experiments_cancel(request, exp):
    exp_id = int(exp)
    usera = UserAccessProfile(request)
    #c_user = get_user_by_email(the_user(request))
    user_type = usera.get_user_type() # get_user_type(c_user)
    if user_type != 2:
        # messages.error(page.request, 'Error: You have not permission to access this page.')
        return HttpResponseRedirect("/")
    exp_obj = Experiments.objects.get(id=exp_id)
    exp_obj.status = 2
    exp_obj.save()
    messages.success(request, 'Success: Remove Experiments.')
    return HttpResponseRedirect("/lab/experiments/")
