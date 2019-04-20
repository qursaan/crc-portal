from django.db.models import Count
from django.db.models import F

from federate.actions import getFedStatus
from portal.models import VirtualNode


def getLocalResources():
    resources = VirtualNode.objects.annotate(type=F('device_ref__type')).values('type').annotate(count=Count('type'))
    return resources


def getSharedResources():
    resources = VirtualNode.objects.none()
    if getFedStatus() == 1:
        resources = VirtualNode.objects.filter(node_ref__shared=False).annotate(type=F('device_ref__type')) \
            .values('type').annotate(count=Count('type'))

    return resources
