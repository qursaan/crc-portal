import json
import os
import urllib2
from subprocess import Popen

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from crc import settings
from federate.fed_backend import fed_status, fed_start, fed_stop
from federate.models import Users, Site
from portal.models import MyUser,ResourceProfile
from portal.modules import UserModules
from portal.backend_actions import create_backend_user
from portal.user_access_profile import UserAccessProfile
from ui.topmenu import topmenu_items  # , the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page


class FedView(LoginRequiredAutoLogoutView):
    template_name = "fed-home.html"

    def dispatch(self, *args, **kwargs):
        return super(FedView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        page = Page(self.request)
        n_local_user = MyUser.objects.filter().count()
        n_remote_user = Users.objects.filter().count()
        n_remote_site = Site.objects.filter().count()  # - 1
        n_local_resources = ResourceProfile.objects.filter(shared__exact=True).count()

        context = super(FedView, self).get_context_data(**kwargs)
        context['fed_service'] = settings.FED_RUN
        context['n_local_user'] = n_local_user
        context['n_remote_user'] = n_remote_user
        context['n_remote_site'] = n_remote_site
        context['n_local_res'] = n_local_resources
        context['username'] = UserAccessProfile(self.request).username # the_user(self.request)
        context['topmenu_items'] = topmenu_items('Testbed View', page.request)
        prelude_env = page.prelude_env()
        context.update(prelude_env)
        return context


@login_required
def get_n_local_users(request):
    if request.method != 'GET':
        return HttpResponseRedirect("/")
    n = MyUser.get.all().count()
    if n:
        return HttpResponse(n, content_type="text/plain")
    return HttpResponse('error', content_type="text/plain")


@login_required
def federate_status(request):
    if request.method != 'GET':
        return HttpResponseRedirect("/")
    n = settings.FED_RUN
    if n is not None:
        return HttpResponse(n, content_type="text/plain")
    return HttpResponse('error', content_type="text/plain")


@login_required
def control_running_federate(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")
    is_running = request.POST.get('is_running', None)
    if is_running is None:
        return HttpResponse("error: Please go back and try again", content_type="text/plain")

    issuccess = 0
    print "Running: ", is_running
    if is_running == "1":
        print "##### START Federation #####"

        #Check the service is running and try to start if not
        try:
            fed_status()
        except Exception as es:
            print "ERROR FED SERVICE:", es.message
            # kill file
            os.system("pkill -9 -f fed_service.py")
            # exe file
            # v = os.system("& python "+os.path.dirname(os.path.abspath("fed_service.py"))+"/federate/fed_service.py")
            Popen(["python", os.path.dirname(os.path.abspath("fed_service.py"))+"/federate/fed_service.py"])

        try:
            # check again
            curr_state = fed_start()
            if curr_state == 1:
                settings.FED_RUN = 1  # Run service flag

                # CREATE DUMMY FED USER
                if not MyUser.objects.filter(username__iexact="feduser"):
                    fed_user =  UserModules.save_user_db("FedUser@CRC.com", "feduser", settings.FED_PASS, "FED", "USER",
                                 None, None, None, 4, 1)

                    web_user = User.objects.get(id=fed_user.id)
                    # TODO: Create user file here
                    result = create_backend_user(fed_user.username, fed_user.password)
                    if result == 1:
                        fed_user.status = 2
                        fed_user.save()
                        web_user.is_active = True
                        web_user.save()

                    # u = MyUser.objects.filter(username__iexact="feduser")

                sites = Site.objects.all()

                for s in sites:
                    if s.status != 2:
                        print "SITE: ", s.name, " DISABLED"
                        continue

                    # READ REMOTE SITE
                    print "READ USERS FROM ", s.name
                    try:
                        response_data = urllib2.urlopen(s.url + 'federation/fed/getUsers/')
                    except:
                        print "ERROR CONNECT TO SITE ", s.name
                        response_data = None

                    if response_data:
                        readd = response_data.read()
                        loadd = json.loads(json.loads(readd).encode("ascii", "replace"))

                        print "DATA: "
                        for x in loadd:
                            print x['fields']['username']
                            reg_username = x['fields']['username']

                            # INSERT DATA INTO TABLES
                            if not Users.objects.filter(username__iexact=reg_username):

                                # USER NOT FOUND ADD TO TABLE
                                luser = Users(
                                    username=reg_username,
                                    site_ref=Site.objects.get(id=s.id),
                                )
                                # SAVE USER
                                luser.save()
                                print "SAVED ", reg_username
            issuccess = 1
        except:
            print "ERROR READING"
            settings.FED_RUN = 0
            issuccess = 0
    else:
        print "##### STOP Federation #####"
        try:
            fed_stop()
            issuccess = 1
        except:
            print "CANNOT STOP: Server not response"

        settings.FED_RUN = 0

    if issuccess == 1:
        return HttpResponse('success', content_type="text/plain")
    return HttpResponse('error', content_type="text/plain")
