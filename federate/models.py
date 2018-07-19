from django.db import models
from django.utils import timezone

# Create your models here.
class Site(models.Model):
    name = models.TextField('Site Name', default='NA')
    ip = models.TextField('Federation IP', default='NA')
    url = models.TextField('Site URL', default='NA')
    location = models.TextField('Site Location', default='NA')
    contact_email = models.TextField('Contact Email', default='NA')
    # status 0-disabled, 1-pending, 2-active, 3-expired, 4-canceled
    status = models.IntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    public_key = models.TextField(null=True)
    private_key = models.TextField(null=True)

    def __unicode__(self):
        return self.name + " @ " + self.ip + " { " + self.url + " } "

class Users(models.Model):
    site_ref = models.ForeignKey(Site, null=True)
    username = models.TextField(null=True)
