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
        #    request = token['request']
        #    # @qursaan: comments
        #    auth = {'AuthMethod': 'password', 'Username': username, 'AuthString': password}
        #    api = ManifoldAPI(auth)
        #    sessions_result = api.forward(Query.create('local:session').to_dict())
        #    print "result"
        #    sessions = sessions_result.ok_value()
        #    print "ok"
        #    if not sessions:
        #        print "GetSession failed", sessions_result.error()
        #        return
        #    print "first", sessions
        #    session = sessions[0]

        #    # Change to session authentication
        #    api.auth = {'AuthMethod': 'session', 'session': session['session']}
        #    self.api = api

            # Get account details
            # the new API would expect Get('local:user') instead
        #    persons_result = api.forward(Query.get('local:user').to_dict())
        #    persons = persons_result.ok_value()
        #    if not persons:
        #        print "GetPersons failed",persons_result.error()
        #        return
        #    person = persons[0]
        #    print "PERSON=", person

        #    request.session['manifold'] = {'auth': api.auth, 'person': person, 'expires': session['expires']}
        #except ManifoldException, e:
        #    print "ManifoldBackend.authenticate caught ManifoldException, returning corresponding ManifoldResult"
        #    return e.manifold_result
        except Exception, e:
        #    print "E: manifoldbackend", e
        #    import traceback
        #    traceback.print_exc()
            return None

        try:
            # Check if the user exists in Django's local database
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # @qursaan: user not found
            user = None
            # Create a user in Django's local database
        #    user = User.objects.create_user(username, username, 'passworddoesntmatter')
        #    user.first_name = "DUMMY_FIRST_NAME" #person['first_name']
        #    user.last_name = "DUMMY LAST NAME" # person['last_name']
        #    user.email = person['email']
        return user

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


