from django.db import models
from django.utils import timezone
import uuid


# Create your models here.
class Site(models.Model):
    name = models.TextField('Site Name', default=None, null=True)
    ip = models.TextField('Federation IP', default=None, null=True)
    url = models.TextField('Site URL', default=None, null=True)
    location = models.TextField('Site Location', default=None, null=True)
    contact_email = models.TextField('Contact Email', default=None, null=True)
    # status 0-disabled, 1-pending, 2-active, 3-expired, 4-canceled
    status = models.IntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    credits = models.IntegerField(default=0)
    public_key = models.TextField(null=True)
    private_key = models.TextField(null=True)

    def __str__(self):
        return self.name + " @ " + self.ip + " { " + self.url + " } "


class Users(models.Model):
    site_ref = models.ForeignKey(Site, null=True, on_delete=models.CASCADE)
    username = models.TextField(null=True)

    def __str__(self):
        return self.username + " @ " + self.site_ref.name


#class Resources(models.Model):
#    resource_uid = models.UUIDField(default=uuid.uuid4)

