__author__ = 'qursaan'

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from portal.user_access_profile import UserAccessProfile
# from portal.actions import get_user_by_email, get_user_type
from portal.modules import UserModules
from ui.topmenu import topmenu_items  # , the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page
from federate.models import Site
from federate.fed_backend import validate_key
import json


# TODO: @qursaan
class FedInfoView(LoginRequiredAutoLogoutView):
    def __init__(self):
        self.user_email = ''
        self.errors = []

    def post(self, request):
        return self.get_or_post(request, 'POST')

    def get(self, request):
        return self.get_or_post(request, 'GET')

    def get_or_post(self, request, method):
        user_a = UserAccessProfile(request)
        self.user_email = user_a.username  # the_user(request)
        page = Page(request)

        self.errors = []
        user_type = user_a.user_type  # get_user_type(user)
        if user_type != 0:
            messages.error(page.request, 'Error: You have not permission to access this page.')
            return HttpResponseRedirect("/")

        # site = None
        try:
            site = Site.objects.get(id=1)
        except Site.DoesNotExist:
            site = None

        if site is None:
            site = Site(id=1)
            private_key, public_key = UserModules.create_keys()
            site.private_key = private_key
            site.public_key = public_key
            site.save()

        if method == 'POST':
            self.errors = []
            site_name = request.POST.get('site_name', None)
            site_url = request.POST.get('site_url', None)
            #site_ip = request.POST.get('site_ip', None)
            site_ip = request.POST.get('site_url', None)
            site_location = request.POST.get('site_location', None)
            site_contact = request.POST.get('site_contact', None)

            if not self.errors and site:
                site.name = site_name
                site.url = site_url
                site.ip = site_ip
                site.location = site_location
                site.contact_email = site_contact
                site.save()
                messages.success(request, 'Success: Update site information')

        template_name = "fed-site.html"
        template_env = {
            'topmenu_items': topmenu_items('Site Information', page.request),
            'username': user_a.username,  # the_user(self.request),
            'site_name': site.name,
            'site_url': site.url,
            'site_ip': site.ip,
            'site_location': site.location,
            'site_contact': site.contact_email,
            'site_pkey': site.public_key,
            'site_info': 1,
            'title': 'Site Information',
        }
        template_env.update(page.prelude_env())
        return render(request, template_name, template_env)


class SiteAddView(LoginRequiredAutoLogoutView):

    def __init__(self):
        self.user_email = ''
        self.errors = []

    def post(self, request, fid=0):
        return self.get_or_post(request, fid, 'POST')

    def get(self, request, fid=0):
        return self.get_or_post(request, fid, 'GET')

    def get_or_post(self, request, fid, method):
        usera = UserAccessProfile(request)
        self.user_email = usera.username  # the_user(request)
        page = Page(request)

        self.errors = []
        user_type = usera.user_type  # get_user_type(user)
        if user_type != 0:
            messages.error(page.request, 'Error: You have not permission to access this page.')
            return HttpResponseRedirect("/")

        site = None
        if fid:
            try:
                site = Site.objects.get(id=fid)
            except Site.DoesNotExist:
                site = None

        if site:
            site_name = site.name
            site_url = site.url
            site_ip = site.ip
            site_location = site.location
            site_contact = site.contact_email
            site_pkey = site.public_key
        else:
            site_name = ''
            site_url = ''
            site_ip = ''
            site_location = ''
            site_contact = ''
            site_pkey = ''

        if method == 'POST':
            self.errors = []
            site_name = request.POST.get('site_name', '')
            site_url = request.POST.get('site_url', '')
            site_ip = request.POST.get('site_ip', '')
            site_location = request.POST.get('site_location', '')
            site_contact = request.POST.get('site_contact', '')
            site_pkey = request.POST.get('site_pkey', '')

            # UPDATE
            if not self.errors and site:
                site.name = site_name
                site.url = site_url
                site.ip = site_ip
                site.location = site_location
                site.contact_email = site_contact
                site.public_key = site_pkey
                site.save()
                messages.success(request, 'Success: Update site information')
                return HttpResponseRedirect('/federation/list')
            else:  # create new site
                site = Site(
                    name=site_name,
                    url=site_url,
                    ip=site_ip,
                    location=site_location,
                    contact_email=site_contact,
                    public_key=site_pkey,
                )
                site.save()
                messages.success(request, 'Success: Add new site information')
                return HttpResponseRedirect('/federation/list')

        template_name = "fed-site.html"
        template_env = {
            'topmenu_items': topmenu_items('Site Information', page.request),
            'username': usera.username,  # the_user(self.request),
            'site_name': site_name,
            'site_url': site_url,
            'site_ip': site_ip,
            'site_location': site_location,
            'site_contact': site_contact,
            'site_pkey': site_pkey,
            'site_info': 0,
            'title': 'Site Information',
        }
        template_env.update(page.prelude_env())
        return render(request, template_name, template_env)


def check_site(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")
    site_ip = request.POST.get('site_url', None)
    site_pkey = request.POST.get('site_pkey', None)

    print("Check site:", site_ip)
    msg = validate_key(site_ip, site_pkey)

    key = 0
    site = 0

    if msg == 1:
        key = 1
        site = 1
    elif msg == 2:
        key = 0
        site = 1

    output = {
        "key": key,
        "site": site,
        # "busy": busy_list
    }

    post_data = json.dumps(output)
    return HttpResponse(post_data, content_type="application/json")
