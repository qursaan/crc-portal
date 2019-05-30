import re, uuid
from django.db import models
from django.utils import timezone

SHA1_RE = re.compile('^[a-f0-9]{40}$')


class SiteConf(models.Model):
#    # federation services 0-disabled 1-enabled
    fed_status = models.IntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.fed_status


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

    def __str__(self):
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

    def __str__(self):
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

    def __str__(self):
        return self.site_name


class Quota(models.Model):
    quota_title = models.TextField(null=True)
    quota_size = models.IntegerField(null=True, default=10)
    quota_duration = models.IntegerField(null=True, default=30)

    def __str__(self):
        return self.quota_title + " [" + str(self.quota_size) + "] credit  per [" + str(self.quota_duration) + "] days";


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
    # 0=admin 1=researcher 2=instructor 3=student 4=federate
    user_type = models.IntegerField(null=True, default=0)
    # supervisor
    supervisor_id = models.IntegerField(null=True)

    def __str__(self):
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
    slice_duration = models.IntegerField(default=1)
    # status 0-disabled, 1-pending, 2-waiting, 3-active, 4-expired, 5-canceled, 6-bulk
    status = models.IntegerField(default=0)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    request_date = models.DateTimeField(null=True)
    approve_date = models.DateTimeField(null=True)
    request_state = models.IntegerField(default=0)

    def __str__(self):
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

    def __str__(self):
        return self.name


class Account(models.Model):
    user_ref = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE)
    platform_ref = models.ForeignKey(Platform, null=True, on_delete=models.DO_NOTHING)
    quota_ref = models.ForeignKey(Quota, null=True, on_delete=models.DO_NOTHING)
    auth_type = models.TextField(null=True)
    config = models.TextField(null=True)

    def __str__(self):
        return str(self.pk)


class AccessHistory(models.Model):
    created = models.DateTimeField(default=timezone.now)
    user_ref = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)


# Resources *******************************************************
class ResourcesInfo(models.Model):
    type = models.TextField(default='NA')
    description = models.TextField(default='NA')
    # credit value
    credit_value = models.IntegerField(default=1)
    image_name = models.TextField(default='NA')

    def __str__(self):
        return self.type


class PhysicalNode(models.Model):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    # public_name = models.TextField(default='NA')
    # false = private , true = public
    shared = models.BooleanField(default=False)
    node_name = models.CharField(max_length=200, null=True)
    location = models.TextField(null=True)
    status = models.IntegerField(default=0)
    num_interface = models.IntegerField(default=0)
    num_virtual = models.IntegerField(default=0)
    num_connection = models.IntegerField(default=0)
    node_ip = models.TextField(default='NA')
    # 0=testbed , 1= simulation
    type = models.IntegerField(default=0)

    def __str__(self):
        return self.node_name


class FrequencyRanges(models.Model):
    group_name = models.TextField(null=True)
    freq_start = models.TextField(null=True)
    freq_end = models.TextField(null=True)

    def __str__(self):
        return self.freq_start + ":" + self.freq_end

    def frequency_value(self):
        return str((float(self.freq_start) + float(self.freq_end)) / 2 + "e6")


class VirtualNode(models.Model):
    vm_name = models.TextField('Virtual Node Name', default='NA')
    node_ref = models.ForeignKey(PhysicalNode, null=True, on_delete=models.CASCADE)
    device_ref = models.ForeignKey(ResourcesInfo, null=True, on_delete=models.CASCADE)
    hv_name = models.TextField('Hypervisor Name', default='NA')
    # false = private , true = public
    shared = models.BooleanField(default=False)

    def __str__(self):
        return str(self.node_ref.node_name + " @ " + self.hv_name + " { " + self.device_ref.type + " } ")


# class ResourceProfile(models.Model):
# uid = models.UUIDField(default=uuid.uuid4, editable=False)
# public_name = models.TextField(default='NA')
# false = private , true = public
# shared = models.BooleanField(default=False)
# resource_ref = models.ForeignKey(VirtualNode, null=True, on_delete=models.DO_NOTHING)

# def __str__(self):
#    return self.public_name

class NodeConnection(models.Model):
    description = models.TextField(default='NA')
    node_src_ref = models.ForeignKey(VirtualNode, null=True, related_name='src_node', on_delete=models.CASCADE)
    node_dst_ref = models.ForeignKey(VirtualNode, null=True, related_name='des_node', on_delete=models.CASCADE)


class SimulationVM(models.Model):
    vm_name = models.TextField('Virtual Node Name', default='NA')
    hv_name = models.TextField('Hypervisor Name', default='NA')
    specification = models.TextField(default='NA')

    def __str__(self):  # __unicode__ on Python 2
        return "Simulation @ " + self.hv_name


# Images *******************************************************
class UserImage(models.Model):
    user_ref = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE)
    username = models.TextField(default=None, null=True)
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
    user_ref = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE)
    # reservation from federation sites
    fed_site_ref = models.IntegerField('Site Name', default=None, null=True)

    username = models.TextField(default=None, null=True)
    authority_hrn = models.TextField(null=True)
    start_time = models.DateTimeField('Actual Start Time', null=True)
    end_time = models.DateTimeField('Actual End Time', null=True)
    f_start_time = models.DateTimeField('Estimate Start Time', null=True)
    f_end_time = models.DateTimeField('Estimate End Time', null=True)
    slice_name = models.TextField(null=True)
    slice_duration = models.IntegerField(default=1)
    approve_date = models.DateTimeField(null=True)
    request_date = models.DateTimeField(default=timezone.now)
    request_type = models.TextField(default='NA')  # 1=schedule 2=ontime
    base_image_ref = models.ForeignKey(TestbedImage, null=True, on_delete=models.DO_NOTHING)
    purpose = models.TextField(default='NA')
    # status 0-disabled, 1-pending, 3-active, 4-expired, 5-canceled
    status = models.IntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)


class ReservationDetail(models.Model):
    reservation_ref = models.ForeignKey(Reservation, null=True, on_delete=models.CASCADE)
    node_ref = models.ForeignKey(VirtualNode, null=True, on_delete=models.DO_NOTHING)
    image_ref = models.ForeignKey(TestbedImage, null=True, on_delete=models.DO_NOTHING)
    last_action = models.DateTimeField(null=True)
    details = models.TextField(default='NA')


class ReservationFrequency(models.Model):
    reservation_ref = models.ForeignKey(Reservation, null=True, on_delete=models.CASCADE)
    frequency_ref = models.ForeignKey(FrequencyRanges, null=True, on_delete=models.CASCADE)


class SimReservation(models.Model):
    user_ref = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE)
    username = models.TextField(default=None, null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    authority_hrn = models.TextField(null=True)
    f_start_time = models.DateTimeField(null=True)
    f_end_time = models.DateTimeField(null=True)
    slice_name = models.TextField(null=True)
    slice_duration = models.IntegerField(default=1)
    approve_date = models.DateTimeField(null=True)
    request_date = models.DateTimeField(default=timezone.now)
    request_type = models.TextField(default='NA')  # 1=schedule 2=onday
    node_ref = models.ForeignKey(SimulationVM, null=True, on_delete=models.DO_NOTHING)
    image_ref = models.ForeignKey(SimulationImage, null=True, on_delete=models.DO_NOTHING)
    n_processor = models.IntegerField(default=1)
    n_ram = models.IntegerField(default=1024)
    purpose = models.TextField(default='NA')
    # status 0-disabled, 1-pending, 3-active, 4-expired, 5-canceled
    status = models.IntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    last_action = models.DateTimeField(null=True)
    details = models.TextField(default='NA')


class SharingPolicy(models.Model):
    policy_name = models.TextField('Policy Name', default='Unnamed Policy')
    # 0=Forbidden , 1=Allow
    type = models.IntegerField(default=0)
    sharing_start_time = models.DateTimeField('Start Time', null=True)
    sharing_end_time = models.DateTimeField('End Time', null=True)

    def __str__(self):
        return str(self.policy_name + " @ " + " { " + ("Forbidden" if self.type == 0 else "Allow") + " } ")
