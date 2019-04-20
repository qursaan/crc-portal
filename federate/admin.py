from django.contrib import admin
from federate.models import Site, Users
# Register your models here.
@admin.register(Site)
class MySiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ip', 'location', 'url', 'contact_email')



# Register your models here.
@admin.register(Users)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')


    