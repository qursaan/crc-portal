from portal.models import SiteConfig


def getFedStatus():
    return SiteConfig.objects.get(id=1).fed_status


def setFedStatus(enabled):
    newStatus = 0
    if enabled:
        newStatus = 1
    site_conf = SiteConfig.objects.get(id=1)
    site_conf.fed_status = newStatus
    site_conf.save()
    return site_conf.fed_status
