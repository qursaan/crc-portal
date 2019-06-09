__author__ = 'qursaan'
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from portal.models import VirtualNode
from portal.user_access_profile import UserAccessProfile
# from portal.actions import  get_user_by_email, get_user_type
from ui.topmenu import topmenu_items  # , the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page


# TODO: @qursaan


class FedResourceView(LoginRequiredAutoLogoutView):
    def __init__(self):
        self.user_email = ''
        self.errors = []

    def post(self, request):
        return self.get_or_post(request, 'POST')

    def get(self, request):
        return self.get_or_post(request, 'GET')

    def get_or_post(self, request, method):
        usera = UserAccessProfile(request)
        self.user_email = usera.username  # the_user(request)
        page = Page(request)

        self.errors = []
        # user = get_user_by_email(the_user(self.request))
        user_type = usera.user_type  # get_user_type(user)
        if user_type != 0:
            messages.error(page.request, 'Error: You have not permission to access this page.')
            return HttpResponseRedirect("/")

        resourceslist = VirtualNode.objects.all()

        if method == 'POST':
            self.errors = []

        template_name = "fed-resources.html"
        template_env = {
            'topmenu_items': topmenu_items('Site Information', page.request),
            'username': usera.username,  # the_user(self.request),
            'resourceslist': resourceslist,
            'title': 'Resources Information',
        }
        template_env.update(page.prelude_env())
        return render(request, template_name, template_env)


@login_required
def resource_enable(request, resource_id):
    resource_id = int(resource_id)
    current_res = VirtualNode.objects.get(id=resource_id)
    current_res.shared = True
    current_res.save()
    messages.success(request, 'Success: Resources Enabled.')
    return HttpResponseRedirect("/federation/resources")


@login_required
def resource_disable(request, resource_id):
    resource_id = int(resource_id)
    current_res = VirtualNode.objects.get(id=resource_id)
    current_res.shared = False
    current_res.save()
    messages.success(request, 'Success: Resources Disabled.')
    return HttpResponseRedirect("/federation/resources")
