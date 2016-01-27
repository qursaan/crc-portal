__author__ = 'pirate'
from unfold.page            import Page
from django.http            import HttpResponse  # HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from portal.models          import VirtualNode
from portal.backend_actions import get_vm_status
from unfold.loginrequired   import LoginRequiredAutoLogoutView
from ui.topmenu             import topmenu_items, the_user
from datetime               import datetime
# from django.contrib        import messages
# from django.shortcuts      import render
# from unfold.page           import Page


# ********** View Testbed Map Page *********** #
class TestbedView(LoginRequiredAutoLogoutView):
    template_name = "testbed-view.html"

    def dispatch(self, *args, **kwargs):
        return super(TestbedView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        page = Page(self.request)
        node_list = VirtualNode.objects.all()

        context = super(TestbedView, self).get_context_data(**kwargs)
        context['node_list'] = node_list
        context['last_update'] = datetime.now()
        context['title'] = 'TESTBEDS VIEW'
        context['username'] = the_user(self.request)
        context['topmenu_items'] = topmenu_items('Testbed View', page.request)
        prelude_env = page.prelude_env()
        context.update(prelude_env)
        return context


@login_required
def check_status(request):
    n_id = request.POST.get('the_post')
    ol = get_vm_status(n_id)
    return HttpResponse(ol, content_type="application/json")
