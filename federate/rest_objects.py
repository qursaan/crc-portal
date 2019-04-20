from rest_framework import serializers, viewsets, permissions
from django.contrib.auth.models import User
from portal.collections import getLocalResources, getSharedResources
from portal.models import VirtualNode, PhysicalNode

# Serializers define the API representation.
class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ResourcesSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only=True)
    count = serializers.IntegerField(read_only=True)
    class Meta:
        model = VirtualNode
        fields = ('type', 'count')


class ResourcesViewSet(viewsets.ModelViewSet):
    queryset = getLocalResources()
    serializer_class = ResourcesSerializer
    http_method_names = ['get']

class SharedResourcesViewSet(viewsets.ModelViewSet):
    queryset = getSharedResources()
    serializer_class = ResourcesSerializer
    http_method_names = ['get']