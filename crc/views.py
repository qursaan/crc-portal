# from django.core.context_processors import csrf
# from django.http import HttpResponseRedirect
# from django.contrib.auth import authenticate, login, logout
# from django.template import RequestContext
# from django.shortcuts import render_to_response

from django.http import HttpResponse
from django.template import Context
# Http404,
from django.template.loader import get_template


# from unfold.loginrequired import FreeAccessView
# from manifold.manifoldresult import ManifoldResult
# from ui.topmenu import topmenu_items, the_user
# from crc.configengine import ConfigEngine
# class HomeView():#FreeAccessView):


def hello(request):
    t = get_template('m1.html')
    c = Context({'title': "HOME PAGE"})
    html = t.render(c)
    return HttpResponse(html)



