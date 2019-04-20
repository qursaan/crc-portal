# from django.core.context_processors import csrf
# from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext

# from django.views.generic      import View
# from django.http               import Http404, HttpResponse
# from django.template.loader    import get_template
# from django.template           import Context
# from portal.models             import PendingUser
from portal.models import SiteConfig
from federate.models import Site
from crc import settings
from crc.configengine import ConfigEngine
from federate.fed_tasks import auth_federate_user
from portal.user_access_profile import UserAccessProfile
# from manifold.manifoldresult import ManifoldResult
from ui.topmenu import topmenu_items  # , topmenu_items_live
from unfold.loginrequired import FreeAccessView


class HomeView(FreeAccessView):

    def default_env(self):
        # print "qursaan", ConfigEngine().manifold_url()
        return {
            'MANIFOLD_URL': ConfigEngine().manifold_url(),
            'title': 'Home Page',
        }

    def post(self, request):
        env = self.default_env()
        username = request.POST.get('username')
        password = request.POST.get('password')
        login_site = request.POST.get('login_site')

        # pass request within the token, so manifold session key can be attached to the request session.
        token = {'username': username,
                 'password': password,
                 'request': request}

        auth_result = authenticate(username=username, password=password)
        # @qursaan
        # check local user
        if auth_result is not None:
            user = auth_result
            if user.is_active:
                print ("LOGGING IN")
                login(request, user)
                request.session['username'] = username
                return HttpResponseRedirect('/login-ok')
            else:
                env['state'] = "Your account is not active, please contact the site admin."
                env['layout_1_or_2'] = "layout-unfold2.html"
                # return render_to_response('home-view.html', env, context_instance=RequestContext(request))

        # check a federated user
        elif auth_result is None and auth_federate_user(username, password, login_site):
            # TODO: @qursaan test login function
            # auth_result = authenticate(username="feduser", password=settings.FED_PASS)
            auth_result = auth_federate_user(username, password, login_site)
            print ("LOGGING IN")
            login(request, auth_result)
            request.session['username'] = username
            return HttpResponseRedirect('/login-ok')
        # otherwise
        else:
            env['state'] = "Your username and/or password were incorrect."
            env['layout_1_or_2'] = "layout-unfold2.html"
            # return render_to_response('home-view.html', env, context_instance=RequestContext(request))

        return render(request, 'home-view.html', env)

    # login-ok sets state="Welcome to CRC" in urls.py
    def get(self, request, state=None):
        try:
            site_conf = SiteConfig.objects.get(id=1)
        except SiteConfig.DoesNotExist:
            site_conf = SiteConfig(id=1)
            site_conf.fed_status = 0
            site_conf.save()

        site_list = None
        if site_conf.fed_status == 1:
            site_list = Site.objects.filter(status__in=[2]) #only active sites
        env = self.default_env()

        env = {
            'username' : UserAccessProfile(request).username,
            #'topmenu_items' : topmenu_items(None, request),
            'fed_status':site_conf.fed_status,
            'site_list': site_list
        }
        if state:
            env['state'] = state
        elif not env['username']:
            env['state'] = None
        # use one or two columns for the layout - not logged in users will see the login prompt
        env['layout_1_or_2'] = "layout-unfold2.html" if not env['username'] else "layout-unfold1.html"
        # return render_to_response('home-view.html', env, context_instance=RequestContext(request))
        return render(request,'home-view.html',env)
