from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
#from rest_framework import viewsets
from portal.serializers import UserSerializer, GroupSerializer
from django.views.defaults import page_not_found

#class UserViewSet(viewsets.ModelViewSet):
#    """
#    API endpoint that allows users to be viewed or edited.
#    """
#    queryset = User.objects.all().order_by('-date_joined')
#    serializer_class = UserSerializer


#class GroupViewSet(viewsets.ModelViewSet):
#    """
#    API endpoint that allows groups to be viewed or edited.
#    """
#    queryset = Group.objects.all()
 #   serializer_class = GroupSerializer

def handler404(request, exception, template_name='uncomplete.html'):
    return  page_not_found(request, exception, template_name=template_name)