from django.conf.urls import url  # patterns

from federate.fed_view import FedView, control_running_federate, federate_status
from federate.fedInfo_view import FedInfoView, SiteAddView, check_site
from federate.fedlist_view import FedListView, site_enable,site_disable
from federate.fed_tasks import federate_getUsers, federate_getAuth

urlpatterns = [
    url(r'^/?$', FedView.as_view(), name="Federation"),
    url(r'^info/?$', FedInfoView.as_view(), name="Site Information"),
    url(r'^list/?$', FedListView.as_view(), name="Federation List"),
    url(r'^site/e/(\d{1,10})/?$', site_enable),
    url(r'^site/d/(\d{1,10})/?$', site_disable),
    url(r'^list/?$', FedListView.as_view(), name="Federation List"),
    url(r'^add/?$', SiteAddView.as_view(), name="Add Site"),
    url(r'^add/(\d{1,10})/?$', SiteAddView.as_view(), name="Add Site"),
    url(r'^fed/getUsers/', federate_getUsers),
    url(r'^fed/getAuth/', federate_getAuth),
    url(r'^federate_status/', federate_status),
    url(r'^add/site_validate?$', check_site),

    url(r'^control_running_federate/?$', control_running_federate),
]
