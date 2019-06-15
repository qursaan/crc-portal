# from django.views.generic      import TemplateView
# from django.views              import generic
from django.urls import path, re_path, include  # patterns

from portal.accountview import AccountView
from portal.actions import validate_action
from portal.contactview import ContactView
from portal.dashboardview import DashboardView
# from portal.filemanagerview import FileManagerView
from portal.graphicview import GraphicBuilderView
from portal.homeview import HomeView
# from portal.documentationview import DocumentationView
from portal.navigation import *
from portal.registrationview import RegistrationView
from portal.reservationview import ReservationView, check_availability
from portal.resourcesview import ResourcesView
# from portal.emulationview import EmulationView
from portal.schedulerview import SchedulerView, check_scheduler
from portal.slicecontrolview import SliceControlView, \
    control_load_image, control_save_image, \
    control_check_load, control_check_save, \
    control_remote_node, control_access_token, \
    control_exe_script, control_check_exe, control_exe_abort, \
    control_lab_run, control_lab_check, control_lab_result
from portal.slicependingview import SliceCurrentView, SliceHistoryView, \
    slice_o_pending_process, slice_s_pending_process, \
    slice_o_pending_cancel, slice_s_pending_cancel
from portal.statview import StatsView, StatsAdminView, stat_report
from portal.supportview import GuideView, TGuideView  # SupportView,
# from portal.sliceview import SliceView
from portal.testbedview import TestbedView, check_status
from portal.validationview import ValidatePendingView
from portal.experimentview import ExperimentView
# from django.conf.urls import url, include
# from rest_framework import routers
# from portal import views
from portal.assuitcontrolview import simple_upload, manage_variables,\
    manage_variables_user
# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    # url(r'^', include(router.urls)),
    # Restful Framework
    # url(r'^api-auth/', include('rest_framework.urls')),

    path('access/', HomeView.as_view(), name='access'),
    # User registration
    re_path(r'^register/?$', RegistrationView.as_view(), name='registration'),
    # url(r'^user/register/complete/$',
    #    TemplateView.as_view(template_name='user_register_complete.html'),
    #    name='user_register_complete'),

    # password management
    #re_path(r'^pass_reset/$', 'portal.django_passresetview.password_reset',
    #    {'post_reset_redirect': '/portal/password/reset/done/'}),
    #re_path(r'^password/reset/done/$', 'portal.django_passresetview.password_reset_done'),
    #re_path(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
    #    'portal.django_passresetview.password_reset_confirm',
    #    {'post_reset_redirect': '/portal/password/done/'}),
    #re_path(r'^password/done/$', 'portal.django_passresetview.password_reset_complete'),

    # Profile
    re_path(r'^account/?$', AccountView.as_view()),
    # url(r'^account/account_process/?$', account_process),

    # Support and Contacts
    path('contact/', ContactView.as_view(), name='contact'),
    path('support/', ContactView.as_view(), name='support'),
    path('guide/', GuideView.as_view(), name='guide'),
    path('tguide/', TGuideView.as_view(), name='teach guide'),
    path('support/documentation/', GuideView.as_view(), name='guide'),  # DocumentationView.as_view(), name='FAQ'),
    path('experiment/', ExperimentView.as_view(), name='experiment'),

    # Validate pending requests
    re_path(r'^validate/?$', ValidatePendingView.as_view()),
    path('validate_action/<str:id>/', validate_action),

    # Log and History
    re_path(r'^history/?$', un_complete_page),
    re_path(r'^stats/?$' , StatsView.as_view(), name="Statistics"),
    re_path(r'^stats_site/?$' , StatsAdminView.as_view(), name="Statistics"),
    re_path(r'^stats_site/stat_report?$', stat_report),

    # Dashboard
    path('', DashboardView.as_view(), {'state': 'Welcome'}),
    path('dashboard/', DashboardView.as_view(), {'state': 'Welcome'}),

    # Testbeds
    re_path(r'^testbeds/map/?$', TestbedView.as_view(), name="testbeds"),
    re_path(r'^testbeds/resources', ResourcesView.as_view(), name='resources'),
    # re_path(r'^testbeds/emulation/?$', EmulationView.as_view(), name="node_emulation"),
    re_path(r'^testbeds/map/check_status?$', check_status),
    # url(r'^testbeds/timeline/?$', TimelineView.as_view(), name='Timeline'),
    re_path(r'^testbeds/scheduler/?$', SchedulerView.as_view(), name='Scheduler'),
    re_path(r'^testbeds/scheduler/check_scheduler?$', check_scheduler),
    # url(r'^testbeds/slice/?$', SliceView.as_view(), name='slice'),

    # Tools
    re_path(r'^lab/tools/builder/?$', GraphicBuilderView.as_view(), name="g_builder"),
    # url(r'^lab/tools/file_manager/?$', FileManagerView.as_view(), name="file_manager"),

    # Reservation
    re_path(r'^lab/current/?$', SliceCurrentView.as_view(), name="slice_pending"),
    re_path(r'^lab/current/slice_o_process/(\d{1,10})/?$', slice_o_pending_process),
    re_path(r'^lab/current/slice_s_process/(\d{1,10})/?$', slice_s_pending_process),
    re_path(r'^lab/current/slice_o_cancel/(\d{1,10})/?$', slice_o_pending_cancel),
    re_path(r'^lab/current/slice_s_cancel/(\d{1,10})/?$', slice_s_pending_cancel),
    re_path(r'^lab/control/?$', SliceControlView.as_view(), name="slice_control"),
    re_path(r'^lab/control/gen_access_token/?$', control_access_token),
    re_path(r'^lab/control/control_load_image/?$', control_load_image),
    re_path(r'^lab/control/control_save_image/?$', control_save_image),
    re_path(r'^lab/control/control_check_load/?$', control_check_load),
    re_path(r'^lab/control/control_check_save/?$', control_check_save),
    re_path(r'^lab/control/control_check_exe/?$', control_check_exe),
    re_path(r'^lab/control/control_exe_script/?$', control_exe_script),
    re_path(r'^lab/control/control_exe_abort/?$', control_exe_abort),
    re_path(r'^lab/control/control_remote_node?$', control_remote_node),
    re_path(r'^lab/control/control_lab_run?$', control_lab_run),
    re_path(r'^lab/control/control_lab_check?$', control_lab_check),
    re_path(r'^lab/control/control_lab_result?$', control_lab_result),

    # url(r'^lab/control/load_samples?$', control_load_sample),
    re_path(r'^lab/history/?$', SliceHistoryView.as_view(), name="slice_history"),
    # url(r'^lab/slice_request/?$', SliceRequestView.as_view(), name='slice_request'),
    re_path(r'^lab/(reservation)/?$', ReservationView.as_view(), name='Reservation'),
    re_path(r'^lab/(reservation_a)/?$', ReservationView.as_view(), name='Admin Reservation'),
    re_path(r'^lab/reservation/check_availability?$', check_availability),
    re_path(r'^lab/reservation_a/check_availability?$', check_availability),

    # Profile
    re_path(r'^upload/?$', simple_upload, name='account'),
    re_path(r'^Manage_Varaibles/?$', manage_variables, name='account'),
    re_path(r'^Manage_Varaibles_user/?$', manage_variables_user, name='account'),
    # Others
    # url(r'/?$', un_complete_page),
    # url(r'^reservation/new/?$', uncomplete),

]

handler404 = 'portal.views.handler404'
