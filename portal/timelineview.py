__author__ = 'pirate'
from datetime import datetime

from portal.user_access_profile import UserAccessProfile
# from unfold.page           import Page
from ui.topmenu import topmenu_items  # , the_user
# from django.http            import HttpResponse #HttpResponseRedirect
# from django.contrib        import messages
# from django.contrib.auth.decorators import login_required
# from portal.navigation      import check_node
# from portal.actions         import update_node_status
from unfold.loginrequired import LoginRequiredAutoLogoutView
# from django.shortcuts       import render
from unfold.page import Page


# ********** View Testbed Map Page *********** #
class TimelineView(LoginRequiredAutoLogoutView):
    template_name = "timeline-view.html"

    def dispatch(self, *args, **kwargs):
        return super(TimelineView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        page = Page(self.request)

        #node_list = Node.objects.all()

        context = super(TimelineView, self).get_context_data(**kwargs)
        #context['node_list'] = node_list
        context['last_update'] = datetime.now()
        context['title'] = 'TIMELINE VIEW'
        context['username'] = UserAccessProfile(self.request).username
        context['topmenu_items'] = topmenu_items('Timeline View', page.request)
        prelude_env = page.prelude_env()
        context.update(prelude_env)
        return context
