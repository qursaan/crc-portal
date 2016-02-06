# import json
# from manifold.core.query         import Query
# from manifold.manifoldapi        import execute_query
# from plugins.lists.testbedlist   import TestbedList
# from plugins.lists.slicelist     import SliceList
from unfold.page import Page
from unfold.loginrequired import LoginRequiredAutoLogoutView
from ui.topmenu import topmenu_items, the_user
from portal.actions import get_count_active_slice, get_user_by_email

# This view requires login
class DashboardView(LoginRequiredAutoLogoutView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        # We might have slices on different registries with different user accounts 
        # We note that this portal could be specific to a given registry, to which we register users, but i'm not sure that simplifies things
        # Different registries mean different identities, unless we identify via SFA HRN or have associated the user email to a single hrn

        # messages.info(self.request, 'You have logged in')
        page = Page(self.request)

        print "Dashboard page"
        # Slow...
        # slice_query = Query().get('slice').filter_by('user.user_hrn', 'contains', user_hrn).select('slice_hrn')
        # testbed_query  = Query().get('network').select('network_hrn','platform','version')
        # DEMO GEC18 Query only PLE
        #        user_query  = Query().get('local:user').select('config','email')
        #        user_details = execute_query(self.request, user_query)

        # not always found in user_details...
        #        config={}
        #      for user_detail in user_details:
        #          #email = user_detail['email']
        #          if user_detail['config']:
        #              config = json.loads(user_detail['config'])
        #      user_detail['authority'] = config.get('authority',"Unknown Authority")
        #
        #        print user_detail
        #        if user_detail['authority'] is not None:
        #            sub_authority = user_detail['authority'].split('.')
        #            root_authority = sub_authority[0]
        #            slice_query = Query().get(root_authority+':user').filter_by('user_hrn', '==', '$user_hrn').select('user_hrn', 'slice.slice_hrn')
        #        else:

        # @qursaan
        # slice_query = Query().get('user').filter_by('user_hrn', '==', '$user_hrn').select('slice.slice_hrn')
        # page.enqueue_query(slice_query)
        # page.enqueue_query(testbed_query)

        # slicelist = SliceList(
        #    page  = page,
        #    title = "slices",
        #    warning_msg = "<a href='../slice_request'>Request Slice</a>",
        #    query = slice_query,
        # )
        # testbedlist = TestbedList(
        #    page  = page,
        #    title = "testbeds",
        #    query = testbed_query,
        # )
        c_user = the_user(self.request)
        context = super(DashboardView, self).get_context_data(**kwargs)
        # context['person']   = self.request.user
        # context['testbeds'] = testbedlist.render(self.request)
        # context['slices']   = slicelist.render(self.request)

        # XXX This is repeated in all pages
        # more general variables expected in the template
        context['title'] = 'Dashboard'
        # the menu items on the top
        # @qursaan: remove __live
        context['topmenu_items'] = topmenu_items('Dashboard', page.request)
        # so we can sho who is logged
        context['username'] = the_user(self.request)
        context['active_count'] = get_count_active_slice(get_user_by_email(c_user))
        # page.expose_js_metadata()

        # the page header and other stuff
        context.update(page.prelude_env())

        return context
