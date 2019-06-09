import time
from mx.Tools import username

from django.contrib.auth.models import User
# @qursaan
#from manifold.manifoldapi import ManifoldAPI, ManifoldException, ManifoldResult
#from manifold.core.query import Query


# Name my backend 'ManifoldBackend'
class ManifoldBackend:

    # Create an authentication method
    # This is called by the standard Django login procedure
    def authenticate(self, token=None):

        if not token:
            return None

        try:
            username = token['username']
            password = token['password']

        except Exception as e:
            return None

        try:
            # Check if the user exists in Django's local database
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # @qursaan: user not found
            user = None

        return user

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


