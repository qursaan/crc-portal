from django.test import TestCase

from portal.modules import *


# Create your tests here.


class PortalTestCase(TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def Create_users(self):
        reg_fname = 'firstname'
        reg_lname = 'lastname'
        reg_auth = 'authority_hrn'
        reg_username = 'username'
        reg_email = 'email'
        reg_password = 'password'
        reg_usertype = 'usertype'
        reg_supervisor = 'supervisor'
        reg_quota = 'quota'
        errors = None
        errors = UserModules.create_user_account(errors, reg_email, reg_username, reg_password,
                                                 reg_fname, reg_lname, reg_auth, reg_usertype,
                                                 reg_supervisor, reg_quota)
        self.assertEqual(errors, None)
