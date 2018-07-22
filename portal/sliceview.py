# import json
from django.shortcuts import render_to_response
from django.template import RequestContext

from manifold.core.query import Query
from portal.user_access_profile import UserAccessProfile
from ui.topmenu import topmenu_items  # , the_user
from unfold.loginrequired import LoginRequiredAutoLogoutView
from unfold.page import Page

# from manifold.manifoldapi            import execute_query

"""from plugins.raw                     import Raw
from plugins.stack                   import Stack
from plugins.tabs                    import Tabs
from plugins.querytable              import QueryTable 
from plugins.querygrid               import QueryGrid
from plugins.queryupdater            import QueryUpdater
from plugins.googlemap               import GoogleMap
from plugins.senslabmap              import SensLabMap
#from plugins.scheduler              import Scheduler
from plugins.scheduler2              import Scheduler2
from plugins.querycode               import QueryCode
# Thierry
# stay away from query editor for now as it seems to make things go very slow
# see https://lists.myslice.info/pipermail/devel-myslice/2013-December/000221.html
from plugins.query_editor            import QueryEditor
from plugins.active_filters          import ActiveFilters
from plugins.quickfilter             import QuickFilter
from plugins.messages                import Messages
from plugins.slicestat               import SliceStat"""

from crc.configengine import ConfigEngine

tmp_default_slice = 'ple.upmc.myslicedemo'

# temporary : turn off the users part to speed things up
# do_query_users=True
do_query_users = False

# do_query_leases=True
do_query_leases = False

insert_grid = False
# insert_grid=True

insert_messages = False


# insert_messages=True


class SliceView(LoginRequiredAutoLogoutView):

    def get(self, request, slicename=tmp_default_slice):
        page = Page(request)
        page.add_css_files('css/slice-view.css')
        page.add_js_files(["js/common.functions.js"])
        page.add_js_chunks('$(function() { messages.debug("sliceview: jQuery version " + $.fn.jquery); });')
        page.add_js_chunks(
            '$(function() { messages.debug("sliceview: users turned %s"); });' % ("on" if do_query_users else "off"))
        page.add_js_chunks(
            '$(function() { messages.debug("sliceview: leases turned %s"); });' % ("on" if do_query_leases else "off"))
        page.add_js_chunks('$(function() { messages.debug("manifold URL %s"); });' % (ConfigEngine().manifold_url()))

        #        metadata = page.get_metadata()
        #        resource_md = metadata.details_by_object('resource')
        #        resource_fields = [column['name'] for column in resource_md['column']]

        #        user_md = metadata.details_by_object('user')
        #        user_fields = ['user_hrn'] # [column['name'] for column in user_md['column']]

        # TODO The query to run is embedded in the URL
        main_query = Query.get('slice').filter_by('slice_hrn', '=', slicename)
        main_query.select(
            'slice_hrn',
            # 'resource.hrn', 'resource.urn',
            'resource.hostname', 'resource.type',
            'resource.network_hrn',
            'lease.urn',
            'user.user_hrn',
            # 'application.measurement_point.counter'
        )
        # for internal use in the querytable plugin;
        # needs to be a unique column present for each returned record
        main_query_init_key = 'hostname'

        # variables that will get passed to the view-unfold1.html template
        template_env = {}

        # define 'unfold_main' to the template engine - the main contents
        #        template_env [ 'unfold_main' ] = main_stack.render(request)

        # more general variables expected in the template
        template_env['title'] = '%(slicename)s' % locals()
        # the menu items on the top
        template_env['topmenu_items'] = topmenu_items('Slice', page.request)
        # so we can sho who is logged
        template_env['username'] = UserAccessProfile(request).username

        # don't forget to run the requests
        #        page.expose_js_metadata()
        # the prelude object in page contains a summary of the requirements() for all plugins
        # define {js,css}_{files,chunks}
        template_env.update(page.prelude_env())

        return render_to_response('view-unfold1.html', template_env,
                                  context_instance=RequestContext(request))
