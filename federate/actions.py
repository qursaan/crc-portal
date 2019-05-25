from portal.models import SiteSettings


def getFedStatus():
    if SiteSettings.objects.count()>0:
        return  SiteSettings.objects.get(id=1).fed_status
    return 0


def setFedStatus(enabled):
    newStatus = 0
    if enabled:
        newStatus = 1
    site_conf = SiteSettings.objects.get(id=1)
    site_conf.fed_status = newStatus
    site_conf.save()
    return site_conf.fed_status
