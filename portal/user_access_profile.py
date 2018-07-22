from portal.actions import get_user_by_email, get_user_type


class UserAccessProfile:
    def __init__(self, request):
        self.username = None
        self.type = None
        self.user_obj = None
        self.user_type = -1

        if request.user.is_authenticated():
            self.username = request.user.email

        if self.username:
            self.user_obj = get_user_by_email(self.username)
            self.user_type = get_user_type(self.user_obj)

    def get_username(self):
        return self.username

    def get_user_object(self):
        return self.user_obj

    def get_user_type(self):
        return self.user_type