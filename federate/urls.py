from django.conf.urls import include, url
from django.urls import path, re_path  # patterns
from rest_framework import routers

from federate.fedInfo_view import FedInfoView, SiteAddView, check_site
from federate.fed_backend import api_fed_valid_key
from federate.fed_tasks import federate_getAuth
from federate.fed_view import FedView, control_running_federate, federate_status
from federate.fedlist_view import FedListView, site_enable, site_disable
from federate.fedresource_view import FedResourceView, resource_disable, resource_enable
from federate.rest_objects import UserViewSet, SharedResourcesViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'resources', SharedResourcesViewSet)

urlpatterns = [
    # Restful Framework
    url(r'^rest/', include(router.urls)),

    path('', FedView.as_view(), name="Federation"),
    re_path(r'^info/?$', FedInfoView.as_view(), name="Site Information"),
    re_path(r'^list/?$', FedListView.as_view(), name="Federation List"),
    re_path(r'^site/e/(\d{1,10})/?$', site_enable),
    re_path(r'^site/d/(\d{1,10})/?$', site_disable),
    re_path(r'^add/?$', SiteAddView.as_view(), name="Add Site"),
    re_path(r'^add/(\d{1,10})/?$', SiteAddView.as_view(), name="Add Site"),
    re_path(r'^add/site_validate?$', check_site),

    re_path(r'^resources/?$', FedResourceView.as_view(), name="Federation Resources"),
    re_path(r'^resources/e/(\d{1,10})/?$', resource_enable),
    re_path(r'^resources/d/(\d{1,10})/?$', resource_disable),

    re_path(r'^', include(router.urls)),
    #re_path(r'^fed/getUsers/', federate_getUsers),
    re_path(r'^fed/getAuth/', federate_getAuth),
    #re_path(r'^fed/update/',  get_site_users),
    re_path(r'^federate_status/', federate_status),
    re_path(r'^control_running_federate/?$', control_running_federate),


    re_path(r'^api/valid/key/',api_fed_valid_key),
]
