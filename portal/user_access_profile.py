from portal.actions import get_user_by_email, get_user_type


class UserAccessProfile:
    def __init__(self, request):
        self.username = None
        self.session_username = None
        self.access_all = True
        self.user_obj = None
        self.user_type = -1

        if request.user.is_authenticated:
            self.username = request.user.email
            self.session_username = request.session.get('username', None)
            if 'FedUser' in self.username:
                self.access_all = False


        print("Session username:", self.session_username)
        if self.username:
            self.user_obj = get_user_by_email(self.username)
            self.user_type = get_user_type(self.user_obj)
