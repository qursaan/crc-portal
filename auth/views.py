
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

# hard question : where should we redirect requests to logout if user is not logged in ?
def logout_user (request):
    # check that we're indeed logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect ('/')
    print ("LOGGING OUT")
    logout(request)
    return HttpResponseRedirect ('/')


