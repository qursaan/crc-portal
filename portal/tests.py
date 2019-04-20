from django.test import TestCase
import unittest
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
        errors = None
        errors = UserModules.create_user_account(errors, reg_email, reg_username, reg_password,
                                                 reg_fname, reg_lname, reg_auth)
        self.assertEqual(errors, None)
