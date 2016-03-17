"""crc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
import portal.dashboardview
import portal.homeview

# qursaan: removed
# from filebrowser.sites import site

# to enable insert_above stuff
from django.template.base import add_to_builtins
add_to_builtins('insert_above.templatetags.insert_tags')




#import portal.platformsview
home_view       = portal.homeview.HomeView.as_view()
dashboard_view  = portal.dashboardview.DashboardView.as_view()
#dashboard_view = portal.navigation.dashboard
#portal.dashboardview.DashboardView.as_view()
#platforms_view=portal.platformsview.PlatformsView.as_view()

the_default_view        = dashboard_view
the_after_login_view    = dashboard_view
the_login_view          = home_view
#admin.autodiscover()

urlpatterns = [
    # default view
    url(r'^/?$', the_default_view),
    # Portal
    url(r'^portal/', include('portal.urls')),
    # filer
    # url(r'^filer/', include('filer.urls')),

    # File Browsers
    #url(r'^admin/filebrowser/', include(site.urls)),
    #url(r'^grappelli/', include('grappelli.urls')),
    # Admin Pages
    url(r'^admin/', include(admin.site.urls)),
    # login / logout
    url(r'^login-ok/?$', the_after_login_view, {'state': 'Welcome to CRC'}),
    url(r'^login/?$', the_login_view),
    url(r'^logout/?$', 'auth.views.logout_user'),
    # seems to be what login_required uses to redirect ...
    url(r'^accounts/login/$', the_login_view),

    # captcha
    url(r'^captcha/', include('captcha.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

