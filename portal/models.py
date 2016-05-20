# import datetime
# import hashlib
# import random
import re
from django.db import models
from django.utils import timezone
# from django.conf              import settings
# from django.core.mail         import send_mail
# , transaction
# from django.utils.translation import ugettext_lazy as _
# from django.template.loader   import render_to_string

# from django.core.validators import validate_email


# try:
#    from django.contrib.auth import get_user_model
#    User = get_user_model()
# except ImportError:
# from django.contrib.auth.models import User

# try:

# except ImportError:
#    datetime_now = datetime.datetime.now

SHA1_RE = re.compile('^[a-f0-9]{40}$')


class PendingUser(models.Model):
    # NOTE We might consider migrating the fields to CharField, which would
    # simplify form creation in forms.py
    first_name = models.TextField(null=True)
    last_name = models.TextField(null=True)
    email = models.EmailField(null=True)  # validators=[validate_email])
    password = models.TextField(null=True)
    keypair = models.TextField(null=True)
    authority_hrn = models.TextField(null=True)
    login = models.TextField(null=True)
    user_hrn = models.TextField(null=True)
    # pi  = models.TextField(null=True)
    created = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name


class PendingAuthority(models.Model):
    site_name = models.TextField(null=True)
    site_authority = models.TextField(null=True)
    site_abbreviated_name = models.TextField(null=True)
    site_url = models.TextField(null=True)
    site_latitude = models.TextField(null=True)
    site_longitude = models.TextField(null=True)
    address_city = models.TextField(null=True)
    address_state = models.TextField(null=True)
    address_country = models.TextField(null=True)
    # parent authority of the requested authority
    authority_hrn = models.TextField(null=True)
    created = models.DateTimeField(default=timezone.now)
    # @qursaan: add email field
    email = models.EmailField(null=True)

    def __unicode__(self):
        return self.site_name


class Authority(models.Model):
    site_name = models.TextField(null=True)
    site_authority = models.TextField(null=True)
    site_abbreviated_name = models.TextField(null=True)
    site_url = models.TextField(null=True)
    site_latitude = models.TextField(null=True)
    site_longitude = models.TextField(null=True)
    address_city = models.TextField(null=True)
    address_state = models.TextField(null=True)
    address_country = models.TextField(null=True)
    # parent authority of the requested authority
    authority_hrn = models.TextField(null=True)
    created = models.DateTimeField(default=timezone.now)
    # @qursaan: add email field
    email = models.EmailField(null=True)

    def __unicode__(self):
        return self.site_name


class MyUser(models.Model):
    first_name = models.TextField(null=True)
    last_name = models.TextField(null=True)
    email = models.EmailField(null=True)
    username = models.TextField(null=True)
    password = models.TextField(null=True)
    keypair = models.TextField(null=True)
    # authority    = models.ForeignKey(Authority, to_field=id, null=True)
    authority_hrn = models.TextField(null=True)
    user_hrn = models.TextField(null=True)
    created = models.DateTimeField(default=timezone.now)
    approved_by = models.TextField(null=True)
    # 0=Disable 1=Pending 2=Enable
    status = models.IntegerField(null=True, default=0)
    # activated email 0=Not Active 1=Active
    active_email = models.IntegerField(null=True, default=0)
    is_admin = models.IntegerField(null=True, default=0)

    def __unicode__(self):
        return self.first_name + " " + self.last_name


class PendingSlice(models.Model):
    slice_name = models.TextField(null=True)
    user_hrn = models.TextField(null=True)
    authority_hrn = models.TextField(null=True)
    # TODO: @qursaan to remove
    number_of_nodes = models.TextField(default=0)
    server_type = models.TextField(default='NA')  # 1=omf      2=sim
    request_type = models.TextField(default='NA')  # 1=schedule 2=ontime
    base_image = models.TextField(default='NA')
    purpose = models.TextField(default='NA')
    created = models.DateTimeField(default=timezone.now)
    slice_duration = models.TextField(default='1')
    # status 0-disabled, 1-pending, 3-active, 4-expired, 5-canceled
    status = models.IntegerField(default=0)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    request_date = models.DateTimeField(null=True)
    approve_date = models.DateTimeField(null=True)
    request_state = models.IntegerField(default=0)

    def __unicode__(self):
        return self.slice_name


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

    def __unicode__(self):
        return self.name


class Account(models.Model):
    user_ref = models.ForeignKey(MyUser, null=True)
    platform_ref = models.ForeignKey(Platform, null=True)
    auth_type = models.TextField(null=True)
    config = models.TextField(null=True)

    def __unicode__(self):
        return str(self.pk)


class AccessHistory(models.Model):
    created = models.DateTimeField(default=timezone.now)
    user_ref = models.ForeignKey(MyUser, null=True)

    def __unicode__(self):
        return str(self.pk)


# Resources *******************************************************
class ResourcesInfo(models.Model):
    type = models.TextField(default='NA')
    description = models.TextField(default='NA')

    def __unicode__(self):
        return self.type


class PhysicalNode(models.Model):
    node_name = models.CharField(max_length=200, null=True)
    location = models.TextField(null=True)
    status = models.IntegerField(default=0)
    num_interface = models.IntegerField(default=0)
    num_virtual = models.IntegerField(default=0)
    num_connection = models.IntegerField(default=0)
    node_ip = models.TextField(default='NA')

    def __unicode__(self):
        return self.node_name


class FrequencyRanges(models.Model):
    group_name = models.TextField(null=True)
    freq_start = models.TextField(null=True)
    freq_end = models.TextField(null=True)

    def __unicode__(self):
        return self.freq_start + ":" + self.freq_end


class VirtualNode(models.Model):
    node_ref = models.ForeignKey(PhysicalNode, null=True)
    device_ref = models.ForeignKey(ResourcesInfo, null=True)
    vm_name = models.TextField('Virtual Node Name', default='NA')
    hv_name = models.TextField('Hypervisor Name', default='NA')

    def __unicode__(self):
        return self.node_ref.node_name + " @ " + self.hv_name + " { " + self.device_ref.type + " } "


class NodeConnection(models.Model):
    description = models.TextField(default='NA')
    node_src_ref = models.ForeignKey(VirtualNode, null=True, related_name='src_node')
    node_dst_ref = models.ForeignKey(VirtualNode, null=True, related_name='des_node')


class SimulationVM(models.Model):
    vm_name = models.TextField('Virtual Node Name', default='NA')
    hv_name = models.TextField('Hypervisor Name', default='NA')
    specification = models.TextField(default='NA')

    def __str__(self):  # __unicode__ on Python 2
        return "Simulation @ " + self.hv_name


# Images *******************************************************
class UserImage(models.Model):
    user_ref = models.ForeignKey(MyUser, null=True)
    image_name = models.CharField(max_length=300, null=True)
    location = models.TextField(default='NA')
    image_type = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(default=timezone.now)
    last_load = models.DateTimeField(null=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.image_name


class TestbedImage(models.Model):
    image_name = models.CharField(max_length=200, null=True)
    location = models.TextField(default='NA')
    image_type = models.CharField(max_length=200, null=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.image_name


class SimulationImage(models.Model):
    image_name = models.CharField(max_length=200, null=True)
    location = models.TextField(default='NA')
    image_type = models.CharField(max_length=200, null=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.image_name


# Reservations *******************************************************
class Reservation(models.Model):
    user_ref = models.ForeignKey(MyUser, null=True)
    authority_hrn = models.TextField(null=True)
    start_time = models.DateTimeField('Actual Start Time', null=True)
    end_time = models.DateTimeField('Actual End Time', null=True)
    f_start_time = models.DateTimeField('Estimate Start Time', null=True)
    f_end_time = models.DateTimeField('Estimate End Time', null=True)
    slice_name = models.TextField(null=True)
    slice_duration = models.TextField(default='1')
    approve_date = models.DateTimeField(null=True)
    request_date = models.DateTimeField(default=timezone.now)
    request_type = models.TextField(default='NA')  # 1=schedule 2=ontime
    base_image_ref = models.ForeignKey(TestbedImage, null=True)
    purpose = models.TextField(default='NA')
    # status 0-disabled, 1-pending, 3-active, 4-expired, 5-canceled
    status = models.IntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return str(self.id)


class ReservationDetail(models.Model):
    reservation_ref = models.ForeignKey(Reservation, null=True)
    node_ref = models.ForeignKey(VirtualNode, null=True)
    image_ref = models.ForeignKey(TestbedImage, null=True)
    last_action = models.DateTimeField(null=True)
    details = models.TextField(default='NA')


class ReservationFrequency(models.Model):
    reservation_ref = models.ForeignKey(Reservation, null=True)
    frequency_ref = models.ForeignKey(FrequencyRanges, null=True)


class SimReservation(models.Model):
    user_ref = models.ForeignKey(MyUser, null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    authority_hrn = models.TextField(null=True)
    f_start_time = models.DateTimeField(null=True)
    f_end_time = models.DateTimeField(null=True)
    slice_name = models.TextField(null=True)
    slice_duration = models.TextField(default='1')
    approve_date = models.DateTimeField(null=True)
    request_date = models.DateTimeField(default=timezone.now)
    request_type = models.TextField(default='NA')  # 1=schedule 2=onday
    node_ref = models.ForeignKey(SimulationVM, null=True)
    image_ref = models.ForeignKey(SimulationImage, null=True)
    purpose = models.TextField(default='NA')
    # status 0-disabled, 1-pending, 3-active, 4-expired, 5-canceled
    status = models.IntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    last_action = models.DateTimeField(null=True)
    details = models.TextField(default='NA')

