__author__ = 'pirate'
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse  # HttpResponseRedirect

from portal.backend_actions import get_vm_status
from portal.models import VirtualNode, PhysicalNode
from portal.user_access_profile import UserAccessProfile
from ui.topmenu import topmenu_items  # , the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page


# ********** View Testbed Map Page *********** #
class TestbedView(LoginRequiredAutoLogoutView):
    template_name = "testbed-view.html"

    def dispatch(self, *args, **kwargs):
        return super(TestbedView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        page = Page(self.request)
        vm_list = VirtualNode.objects.all().order_by('node_ref')
        node_list = PhysicalNode.objects.all()

        context = super(TestbedView, self).get_context_data(**kwargs)
        context['vm_list'] = vm_list
        context['node_list'] = node_list
        context['last_update'] = datetime.now()
        context['title'] = 'TESTBEDS VIEW'
        context['username'] = UserAccessProfile(self.request).username
        context['topmenu_items'] = topmenu_items('Testbed View', page.request)
        prelude_env = page.prelude_env()
        context.update(prelude_env)
        return context


@login_required
def check_status(request):
    if "the_post" in request.POST:
        n_id = request.POST.get('the_post')
        ol = get_vm_status(n_id)
        return HttpResponse(ol, content_type="application/json")
    else:
        return HttpResponse('{"Error": "Error"}', content_type="application/json")
