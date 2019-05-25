from django.contrib import admin

from portal.models import MyUser, Platform, Account, \
    PhysicalNode, ResourcesInfo, VirtualNode, NodeConnection, SimulationVM, FrequencyRanges, \
    UserImage, TestbedImage, SimulationImage, \
    Authority, PendingSlice, SiteSettings, \
    Reservation, SimReservation, ReservationFrequency, Quota , ReservationDetail


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    # fieldsets = [
    # (None,               {'fields': ['login']}),
    # ('User information', {'fields': ['first_name','last_name','email',
    # 'password','authority_hrn','status'],}),
    # ]
    list_display = ('id', 'name', 'longname')
    # list_filter = ['created']
    # search_fields = ['first_name','last_name','authority_hrn']


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'first_name', 'last_name', 'username', 'email', 'authority_hrn', 'supervisor_id', 'active_email', 'status',
    'user_type', 'created')


@admin.register(Quota)
class QuotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'quota_title', 'quota_size', 'quota_duration')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_ref', 'platform_ref', 'quota_ref', 'auth_type', 'config')


@admin.register(Authority)
class AuthorityAdmin(admin.ModelAdmin):
    list_display = ('id', 'site_name', 'site_authority', 'authority_hrn', 'created', 'email')


# Resources ****************************************************
# @admin.register(ResourceProfile)
# class ResourceProfileAdmin(admin.ModelAdmin):
#    list_display = ('id', 'uid', 'public_name', 'shared', 'resource_ref')


@admin.register(ResourcesInfo)
class ResourceInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'credit_value', 'image_name')


@admin.register(PhysicalNode)
class PhysicalNodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'node_name', 'node_ip', 'num_virtual', 'num_interface', 'status', 'location')


@admin.register(VirtualNode)
class VirtualNodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'node_ref', 'device_ref', 'vm_name', 'hv_name')


@admin.register(NodeConnection)
class NodeConnectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'node_src_ref', 'node_dst_ref')


@admin.register(SimulationVM)
class SimulationVMAdmin(admin.ModelAdmin):
    list_display = ('id', 'vm_name', 'specification')


@admin.register(FrequencyRanges)
class FrequencyRangesAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_name', 'freq_start', 'freq_end',)


# Images *******************************************************
@admin.register(TestbedImage)
class TestbedImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_name', 'location', 'image_type',)


@admin.register(SimulationImage)
class SimulationImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_name', 'location', 'image_type',)


@admin.register(UserImage)
class MyUserImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_ref', 'username', 'image_name', 'location', 'image_type', 'created')


# Reservations *******************************************************
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_ref', 'username', 'start_time', 'end_time', 'f_start_time', 'f_end_time',
                    'slice_name', 'slice_duration', 'approve_date', 'request_date',
                    'request_type', 'base_image_ref', 'purpose', 'status', 'created')


@admin.register(ReservationDetail)
class ReservationDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'reservation_ref', 'node_ref', 'image_ref',)


@admin.register(ReservationFrequency)
class ReservationFrequencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'reservation_ref', 'frequency_ref')


@admin.register(SimReservation)
class SimReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_ref', 'username', 'start_time', 'end_time', 'f_start_time', 'f_end_time',
                    'slice_name', 'slice_duration', 'approve_date', 'request_date',
                    'request_type', 'node_ref', 'image_ref', 'purpose', 'status', 'created')


# Old *******************************************************
@admin.register(PendingSlice)
class PendingSliceAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'slice_name', 'user_hrn', 'authority_hrn', 'server_type', 'request_type', 'start_time', 'end_time',
        'status',)


@admin.register(SiteSettings)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'fed_status')
