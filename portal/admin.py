from django.contrib import admin
from portal.models import MyUser, Platform, Account, MyUserImage, Node, Image, Authority, PendingSlice


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    #fieldsets = [
        #(None,               {'fields': ['login']}),
        #('User information', {'fields': ['first_name','last_name','email',
					#'password','authority_hrn','status'],}),
    #]
    list_display = ('id', 'name', 'longname')
    #list_filter = ['created']
    #search_fields = ['first_name','last_name','authority_hrn']


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'status', 'created')


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'node_name', 'node_ip', 'status', 'location')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_ref', 'platform_ref', 'auth_type', 'config')


@admin.register(Authority)
class AuthorityAdmin(admin.ModelAdmin):
    list_display = ('id', 'site_name', 'site_authority', 'authority_hrn', 'created', 'email')


#@admin.register(PendingUser):
#class AccountPendingUser(admin.ModelAdmin):


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_name', 'location', 'image_type',)


@admin.register(PendingSlice)
class PendingSliceAdmin(admin.ModelAdmin):
    list_display = ('id', 'slice_name', 'user_hrn', 'authority_hrn', 'type_of_nodes', 'start_time', 'end_time', 'status')


@admin.register(MyUserImage)
class MyUserImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_ref', 'image_name', 'location', 'image_type', 'created')

