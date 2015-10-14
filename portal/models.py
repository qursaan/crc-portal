#import datetime
#import hashlib
#import random
import re

#from django.conf              import settings
#from django.core.mail         import send_mail
from django.db                import models #, transaction
#from django.utils.translation import ugettext_lazy as _
#from django.template.loader   import render_to_string

#from django.core.validators import validate_email


#try:
#    from django.contrib.auth import get_user_model
#    User = get_user_model()
#except ImportError:
#from django.contrib.auth.models import User

#try:
from django.utils import timezone
#except ImportError:
#    datetime_now = datetime.datetime.now

SHA1_RE = re.compile('^[a-f0-9]{40}$')


class PendingUser(models.Model):
    # NOTE We might consider migrating the fields to CharField, which would
    # simplify form creation in forms.py
    first_name    = models.TextField(null=True)
    last_name     = models.TextField(null=True)
    email         = models.EmailField(null=True) #validators=[validate_email])
    password      = models.TextField(null=True)
    keypair       = models.TextField(null=True)
    authority_hrn = models.TextField(null=True)
    login         = models.TextField(null=True)
    user_hrn      = models.TextField(null=True)
#    pi            = models.TextField(null=True)
    created       = models.DateTimeField(default=timezone.now)


class PendingAuthority(models.Model):
    site_name             = models.TextField(null=True)
    site_authority        = models.TextField(null=True)
    site_abbreviated_name = models.TextField(null=True)
    site_url              = models.TextField(null=True)
    site_latitude         = models.TextField(null=True)
    site_longitude        = models.TextField(null=True)
    address_city          = models.TextField(null=True)
    address_state         = models.TextField(null=True)
    address_country       = models.TextField(null=True)
    # parent authority of the requested authority
    authority_hrn         = models.TextField(null=True)
    created               = models.DateTimeField(default=timezone.now)
    # @qursaan: add email field
    email                 = models.EmailField(null=True)


class Authority(models.Model):
    site_name             = models.TextField(null=True)
    site_authority        = models.TextField(null=True)
    site_abbreviated_name = models.TextField(null=True)
    site_url              = models.TextField(null=True)
    site_latitude         = models.TextField(null=True)
    site_longitude        = models.TextField(null=True)
    address_city          = models.TextField(null=True)
    address_state         = models.TextField(null=True)
    address_country       = models.TextField(null=True)
    # parent authority of the requested authority
    authority_hrn         = models.TextField(null=True)
    created               = models.DateTimeField(default=timezone.now)
    # @qursaan: add email field
    email                 = models.EmailField(null=True)


class MyUser(models.Model):
    first_name    = models.TextField(null=True)
    last_name     = models.TextField(null=True)
    email         = models.EmailField(null=True)
    password      = models.TextField(null=True)
    keypair       = models.TextField(null=True)
    #authority     = models.ForeignKey(Authority, to_field=id, null=True)
    authority_hrn = models.TextField(null=True)
    user_hrn      = models.TextField(null=True)
    created       = models.DateTimeField(default=timezone.now)
    approved_by   = models.TextField(null=True)
    # 0=Disable 1=Pending 2=Enable
    status        = models.IntegerField(null=True, default=0)
    is_admin         = models.IntegerField(null=True, default=0)


class PendingSlice(models.Model):
    slice_name      = models.TextField(null=True)
    user_hrn        = models.TextField(null=True)
    authority_hrn   = models.TextField(null=True)
    number_of_nodes = models.TextField(default=0)
    type_of_nodes   = models.TextField(default='NA')
    purpose         = models.TextField(default='NA')
    created         = models.DateTimeField(default=timezone.now)
    # status 0-disabled, 1-pending, 3-active, 4-expired, 5-canceled
    status          = models.IntegerField(default=0)
    start_time      = models.DateTimeField(null=True)
    end_time        = models.DateTimeField(null=True)
    request_date    = models.DateTimeField(null=True)
    approve_date   = models.DateTimeField(null=True)
    request_state  = models.IntegerField(default=0)

"""
class Slice(models.Model):
    slice_name      = models.TextField(null=True)
    user_hrn        = models.TextField(null=True)
    authority_hrn   = models.TextField(null=True)
    number_of_nodes = models.TextField(default=0)
    type_of_nodes   = models.TextField(default='NA')
    purpose         = models.TextField(default='NA')
    created         = models.DateTimeField(default=timezone.now)
    status          = models.IntegerField(default=0)
    start_time      = models.DateTimeField(null=True)
    end_time        = models.DateTimeField(null=True)
    request_date    = models.DateTimeField(null=True)
    approve_date   = models.DateTimeField(null=True)
    request_state  = models.IntegerField(default=0)
"""


class Platform(models.Model):
     name = models.TextField(null=True)
     longname = models.TextField(null=True)
    # gateway_type= models.TextField(null=True)
    # gateway_conf= models.TextField(null=True)


class Account(models.Model):
    user_ref      = models.ForeignKey(MyUser, null=True)
    platform_ref  = models.ForeignKey(Platform, null=True)
    auth_type     = models.TextField(null=True)
    config        = models.TextField(null=True)


class AccessHistory(models.Model):
    created     = models.DateTimeField(default=timezone.now)
    user_id     = models.ForeignKey(MyUser, null=True)


class Node(models.Model):
    node_name   = models.CharField(max_length=200, null=True)
    location    = models.TextField(null=True)
    status      = models.IntegerField(default=0)
    num_intface = models.IntegerField(default=0)
    num_virtual = models.IntegerField(default=0)
    num_connect = models.IntegerField(default=0)
    node_ip     = models.TextField(default='NA')


class NodeConnection(models.Model):
    description = models.TextField(null=True)
    node_src    = models.ForeignKey(Node, null=True, related_name='src_node')
    node_dst    = models.ForeignKey(Node, null=True, related_name='des_node')


class MyUserImage(models.Model):
    user_ref   = models.ForeignKey(MyUser, null=True)
    image_name = models.CharField(max_length=300, null=True)
    location   = models.TextField(default='NA')
    image_type = models.CharField(max_length=200, null=True)
    created    = models.DateTimeField(default=timezone.now)
    last_load  = models.DateTimeField(null=True)


class Image(models.Model):
    image_name = models.CharField(max_length=200, null=True)
    location   = models.TextField(default='NA')
    image_type = models.CharField(max_length=200, null=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.image_name


class Reservation(models.Model):
    user_id       = models.ForeignKey(PendingUser, null=True)
    created       = models.DateTimeField(default=timezone.now)
    request_date  = models.DateTimeField(default=timezone.now)
    start_time    = models.DateTimeField(null=True)
    end_time      = models.DateTimeField(null=True)
    approve_date  = models.DateTimeField(null=True)
    request_state = models.IntegerField(default=0)


class ReservationDetail(models.Model):
    reservation_id = models.ForeignKey(Reservation, null=True)
    node_id       = models.ForeignKey(Node, null=True)
    image_id      = models.ForeignKey(Image, null=True)

