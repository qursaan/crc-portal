from django.conf.urls import url  # patterns

from federate.fed_view import FedView, control_running_federate, federate_status
from federate.fedInfo_view import FedInfoView, SiteAddView, check_site
from federate.fedlist_view import FedListView, site_enable,site_disable
from federate.fedresource_view import FedResourceView, resource_disable, resource_enable
from federate.fed_tasks import federate_getUsers, federate_getAuth

urlpatterns = [
    url(r'^/?$', FedView.as_view(), name="Federation"),
    url(r'^info/?$', FedInfoView.as_view(), name="Site Information"),
    url(r'^list/?$', FedListView.as_view(), name="Federation List"),
    url(r'^site/e/(\d{1,10})/?$', site_enable),
    url(r'^site/d/(\d{1,10})/?$', site_disable),
    url(r'^add/?$', SiteAddView.as_view(), name="Add Site"),
    url(r'^add/(\d{1,10})/?$', SiteAddView.as_view(), name="Add Site"),
    url(r'^add/site_validate?$', check_site),

    url(r'^resources/?$', FedResourceView.as_view(), name="Federation Resources"),
    url(r'^resources/e/(\d{1,10})/?$', resource_enable),
    url(r'^resources/d/(\d{1,10})/?$', resource_disable),

    url(r'^fed/getUsers/', federate_getUsers),
    url(r'^fed/getAuth/', federate_getAuth),
    url(r'^federate_status/', federate_status),
    url(r'^control_running_federate/?$', control_running_federate),
]
