__author__ = 'qursaan'
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from federate.models import Site
from portal.user_access_profile import UserAccessProfile
# from portal.actions import  get_user_by_email, get_user_type
from ui.topmenu import topmenu_items  # , the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page


# TODO: @qursaan


class FedListView(LoginRequiredAutoLogoutView):
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

        fedlist = Site.objects.all()

        if method == 'POST':
            self.errors = []
            '''site_name = request.POST.get('site_name', '')
            site_url = request.POST.get('site_url', '')
            site_ip = request.POST.get('site_ip', '')
            site_location = request.POST.get('site_location', '')
            site_contact = request.POST.get('site_contact', '')

            if not self.errors and site:
                site.name = site_name
                site.url = site_url
                site.ip = site_ip
                site.location = site_location
                site.contact_email = site_contact
                site.save()
                messages.success(request, 'Success: Update site information')'''

        template_name = "fed-list.html"
        template_env = {
            'topmenu_items': topmenu_items('Site Information', page.request),
            'username': usera.username,  # the_user(self.request),
            'fedlist': fedlist,
            'title': 'Site Information',
        }
        template_env.update(page.prelude_env())
        return render(request, template_name, template_env)


@login_required
def site_enable(request, site_id):
    return site_update(request, site_id, 2, "Enabled")


@login_required
def site_disable(request, site_id):
    return site_update(request, site_id, 0, "Disabled")


def site_update(request, site_id, status_val, txt):
    site_id = int(site_id)
    current_site = Site.objects.get(id=site_id)
    current_site.status = status_val
    current_site.save()
    messages.success(request, 'Success: Site ' + txt)
    return HttpResponseRedirect("/federation/list")
