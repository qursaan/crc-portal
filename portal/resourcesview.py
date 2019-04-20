__author__ = 'qursaan'

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from portal.user_access_profile import UserAccessProfile
from portal.collections import getLocalResources
#from portal.actions import get_user_by_email, get_user_type
#from portal.modules import UserModules
from ui.topmenu import topmenu_items#, the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page
#from federate.rest_objects import GetLocalResources
from portal.models import ResourcesInfo
import json


# TODO: @qursaan
class ResourcesView(LoginRequiredAutoLogoutView):
    def __init__(self):
        self.user_email = ''
        self.errors = []

    def post(self, request):
        return self.get_or_post(request, 'POST')

    def get(self, request):
        return self.get_or_post(request, 'GET')

    def get_or_post(self, request, method):
        usera = UserAccessProfile(request)
        self.user_email = usera.username # the_user(request)
        page = Page(request)

        self.errors = []
        #user = get_user_by_email(the_user(self.request))
        user_type = usera.user_type #get_user_type(user)
        if user_type != 0:
            messages.error(page.request, 'Error: You have not permission to access this page.')
            return HttpResponseRedirect("/")
        local_resources = getLocalResources()
        remote_resources = None

        template_name = "resources-view.html"
        template_env = {
            'topmenu_items': topmenu_items('Resources View', page.request),
            'username': usera.username, #the_user(self.request),
            'local_resources': local_resources,
            'remote_resources' : remote_resources,
            'site_name': 'Current site',
            'title': 'Site Information',
        }
        template_env.update(page.prelude_env())
        return render(request, template_name, template_env)