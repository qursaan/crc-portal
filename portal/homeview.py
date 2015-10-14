#from django.core.context_processors import csrf
from django.http         import HttpResponseRedirect
#from django.contrib.auth import logout
from django.contrib.auth import authenticate,login
from django.template     import RequestContext
from django.shortcuts    import render_to_response

from unfold.loginrequired    import FreeAccessView
#from manifold.manifoldresult import ManifoldResult
from ui.topmenu              import the_user, topmenu_items #, topmenu_items_live
from crc.configengine        import ConfigEngine

#from django.views.generic      import View
#from django.http               import Http404, HttpResponse
#from django.template.loader    import get_template
#from django.template           import Context
#from portal.models             import PendingUser


class HomeView(FreeAccessView):

    def default_env (self):
        #print "qursaan", ConfigEngine().manifold_url()
        return {
                'MANIFOLD_URL': ConfigEngine().manifold_url(),
                'title': 'Home Page',
             }

    def post(self, request):
        env = self.default_env()
        username = request.POST.get('username')
        password = request.POST.get('password')

        # pass request within the token, so manifold session key can be attached to the request session.
        token = {'username': username,
                 'password': password,
                 'request': request}

        # our authenticate function returns either
        # . a ManifoldResult - when something has gone wrong, like e.g. backend is unreachable
        # . a django User in case of success
        # . or None if the backend could be reached but the authentication failed
        auth_result = authenticate(username=username, password=password)
        # use one or two columns for the layout - not logged in users will see the login prompt
        # high-level errors, like connection refused or the like
        # @qursaan
        # if isinstance(auth_result, ManifoldResult):
        #    manifoldresult = auth_result
        #    # let's use ManifoldResult.__repr__
        #    env['state']="%s"%manifoldresult
        #    env['layout_1_or_2']="layout-unfold2.html"
        #    return render_to_response('home-view.html',env, context_instance=RequestContext(request))
        # user was authenticated at the backend
        #el
        if auth_result is not None:
            user = auth_result
            if user.is_active:
                print "LOGGING IN"
                login(request, user)
                return HttpResponseRedirect('/login-ok')
            else:
                env['state'] = "Your account is not active, please contact the site admin."
                env['layout_1_or_2'] = "layout-unfold2.html"
                return render_to_response('home-view.html', env, context_instance=RequestContext(request))
        # otherwise
        else:
            env['state'] = "Your username and/or password were incorrect."
            env['layout_1_or_2'] = "layout-unfold2.html"
            return render_to_response('home-view.html', env, context_instance=RequestContext(request))

    # login-ok sets state="Welcome to CRC" in urls.py
    def get(self, request, state=None):

        env = self.default_env()
        env['username'] = the_user(request)
        env['topmenu_items'] = topmenu_items(None, request)
        if state : env['state'] = state
        elif not env['username'] : env['state'] = None
        # use one or two columns for the layout - not logged in users will see the login prompt
        env['layout_1_or_2'] = "layout-unfold2.html" if not env['username'] else "layout-unfold1.html"
        return render_to_response('home-view.html', env, context_instance=RequestContext(request))
