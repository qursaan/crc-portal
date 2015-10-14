from django.contrib.auth.decorators     import login_required
from django.utils.decorators            import method_decorator
from django.http                        import HttpResponseRedirect
# for 'as_view' that we need to call in urls.py and the like
from django.views.generic.base          import TemplateView
# @qursaan
"""from manifold.manifoldresult            import ManifoldException
"""

###
# IMPORTANT NOTE
# the implementation of the classes in this file rely on redefining 'dispatch'
# for this reason if you inherit any of these, please do not redefine 'dispatch' yourself,
# but rather redefine 'get' and 'post' instead
###

########## the base class for views that require a login
class LoginRequiredView (TemplateView):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredView, self).dispatch(request, *args, **kwargs)


########## the base class for views that need to protect against ManifoldException
# a decorator for view classes to catch manifold exceptions
# by design views should not directly exercise a manifold query
# given that these are asynchroneous, you would expect a view to just
# return a mundane skeleton
# however of course this is not always true,
# e.g. we deal with metadata some other way, and so
# it is often a good idea for a view to monitor these exceptions
# and to take this opportunity to logout people
# @qursaan
"""def logout_on_manifold_exception(fun_that_returns_httpresponse):
    def wrapped(request, *args, **kwds):
        # print 'wrapped by logout_on_manifold_exception'
        try:
            return fun_that_returns_httpresponse(request,*args, **kwds)
        except ManifoldException, manifold_result:
            # xxx we need a means to display this message to user...
            from django.contrib.auth import logout
            # in some unusual cases, this might fail
            try: logout(request)
            except: pass
            return HttpResponseRedirect ('/')
        except Exception, e:
            # xxx we need to sugarcoat this error message in some error template...
            print "Unexpected exception",e
            import traceback
            traceback.print_exc()
            return HttpResponseRedirect ('/')
    return wrapped
"""

# at first sight this matters only for views that require login
# so for now we expose a single class that behaves like
# login_required + logout_on_manifold_exception
class LoginRequiredAutoLogoutView (TemplateView):
    # @qursaan
    # @logout_on_manifold_exception
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwds):
        return super(LoginRequiredAutoLogoutView, self).dispatch(request, *args, **kwds)

# we have more and more views that actually send manifold queries
# so for these we need to protect against manifold exceptions
# even though login is not required
class FreeAccessView (TemplateView):

    def dispatch(self, request, *args, **kwds):
        return super(FreeAccessView, self).dispatch(request, *args, **kwds)
