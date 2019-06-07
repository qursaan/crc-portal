from django.urls import re_path

from howdy import views

urlpatterns = [

    # url(r'^/upload/$', views.simple_upload),  # Add this /about/ route
    # url(r'^/viewdevices/$', views.simple_viewdevices.as_view()),  # Add this /about/ route
    re_path(r'^viewdevices/$', views.simple_viewdevices),  # Add this /about/ route

    #  url(r'^/assiut/$', views.HomePageView.as_view()),

]
