# -*- coding: utf-8 -*-
import json
import re

from random import randint
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string

from portal.models import MyUser, Account, Platform, Authority
from crc.settings import SUPPORT_EMAIL


class Modules:
    def __init__(self):
        return None


class UserModules:
    @staticmethod
    def is_user_valid(errors, reg_fname, reg_lname ,reg_email, reg_username):
        # POST values validation
        if re.search(r'^[\w+\s.@+-]+$', reg_fname) is None:
            errors.append('First Name may contain only letters, numbers, spaces and @/./+/-/_ characters.')
        if re.search(r'^[\w+\s.@+-]+$', reg_lname) is None:
            errors.append('Last Name may contain only letters, numbers, spaces and @/./+/-/_ characters.')
        if(reg_email != reg_username):
            errors.append('Email address must be matched with login')
        return not errors

    @staticmethod
    def is_user_unique(errors, reg_email, reg_username):
        # user_details = User.objects.all()
        # user_model = get_user_model()

        # checking in django_db !!
        if MyUser.objects.filter(email__iexact=reg_email, status=1):
            errors.append('Email is pending for validation. Please provide a new email address.')

        elif MyUser.objects.filter(email__iexact=reg_email, status=0):
            errors.append('This account is disabled. Please contact the administrator')

        elif MyUser.objects.filter(username__iexact=reg_username):
            errors.append('Username is already registered in CRC Server. Please provide an unique username')

        elif User.objects.filter(email__iexact=reg_email):
            errors.append('Email already registered in CRC Server. Please provide a new email address.')

        # if PendingUser.objects.filter(email__iexact=reg_email):
        #    errors.append('Email is pending for validation. Please provide a new email address.')

        # elif user_model._default_manager.filter(email__iexact=reg_email):
        #    errors.append('This email is used. Please contact the administrator or try with another email.')

        return not errors

    @staticmethod
    def create_keys():
        from Crypto.PublicKey import RSA
        from Crypto import Random

        # generate new key
        random_generator = Random.new().read
        private = RSA.generate(1024,random_generator)
        private_key = json.dumps(private.exportKey())
        public = private.publickey()
        pk = public.exportKey() #format='OpenSSH')
        public_key = json.dumps(pk)
        return private_key, public_key

    @staticmethod
    def save_user_db(reg_email, reg_username, reg_password, reg_fname, reg_lname,
                     reg_auth, account_config, user_hrn, reg_usertype, reg_supervisor):

        # saves the user to django auth_user table [needed for password reset]
        web_user = User.objects.create_user(reg_username, reg_email, reg_password)
        # @qursaan: set user inactive
        web_user.first_name = reg_fname
        web_user.last_name = reg_lname
        web_user.is_active = False
        web_user.save()

        # @qursaan: add create user to backend
        itf_user = MyUser(
            first_name=reg_fname,
            last_name=reg_lname,
            authority_hrn=reg_auth,
            username=reg_username,
            email=reg_email,
            #password=reg_password,
            keypair=account_config,
            user_hrn=user_hrn,
            status=1,  # set 1 = Pending
            active_email=0,  # set 0 = not activated
            user_type=reg_usertype,
        )
        if reg_supervisor:
            itf_user.supervisor_id = reg_supervisor

        itf_user.id = web_user.id
        itf_user.save()

        itf_plf = Platform.objects.get(id=1)
        auth_type = 'managed'
        itf_acc = Account(
            user_ref=itf_user,
            platform_ref=itf_plf,
            auth_type=auth_type,
            config=account_config,
        )
        itf_acc.save()

        return itf_user

    @staticmethod
    def send_email_create_user(public_key, reg_auth, reg_email, reg_fname,
                    reg_lname, reg_username, user_hrn):
        ctx = {
            'first_name': reg_fname,
            'last_name': reg_lname,
            'authority_hrn': reg_auth,
            'email': reg_email,
            'username': reg_username,
            'user_hrn': user_hrn,
            'public_key': public_key,
        }

        # @qursaan: send to authority only
        auth_email = Authority.objects.get(authority_hrn=reg_auth)
        recipients = [auth_email.email]
        # recipients = authority_get_pi_emails(request, reg_auth)
        # backup email: if authority_get_pi_emails fails
        recipients.append(SUPPORT_EMAIL)
        msg = render_to_string('user_request_email.txt', ctx)
        send_mail("CRC New User request for %s submitted" % reg_email, msg,
                  'qursaan@crclab.org', recipients)

    @staticmethod
    def create_user_account(errors, reg_email, reg_username, reg_password,
                            reg_fname, reg_lname, reg_auth, reg_usertype, reg_supervisor):
        # (1)
        UserModules.is_user_valid(errors, reg_fname, reg_lname, reg_email, reg_username)
        UserModules.is_user_unique(errors, reg_email, reg_username)

        ##################################################
        # TODO: Factorize with portal/accountview.py
        # @qursaan: set auto generation
        # (2) If no error
        if not errors:  # 'generate' in request.POST['question']:
            # (3) Generate Keys
            private_key, public_key = UserModules.create_keys()

            # (4) prepare user_hrn
            split_email = reg_email.split("@")[0]
            split_email = split_email.replace(".", "_")
            user_hrn = reg_auth + '.' + split_email + str(randint(1, 1000000))

            # (5) prepare key for Saving in DB
            account_config = '{"user_public_key":' + public_key + \
                             ', "user_private_key":' + private_key + \
                             ', "user_hrn":"' + user_hrn + '"}'

            # (6) prepare key for sending email: removing existing double qoute
            public_key = public_key.replace('"', '')

            # (4) Saving user in DB
            UserModules.save_user_db(reg_email, reg_username, reg_password, reg_fname, reg_lname,
                              reg_auth, account_config, user_hrn, reg_usertype, reg_supervisor)

            # (5) Send email
            UserModules.send_email_create_user(public_key, reg_auth, reg_email, reg_fname,
                                        reg_lname, reg_username, user_hrn)
        return errors

    """def CreateAccount(fname, lname, emal, pwd, logn, utype, authId):
        b = PendingUser(
            first_name=fname,
            last_name=lname,
            email=emal,
            password=pwd,
            authority_hrn=authId,
            login=logn,
            status=0,
            user_type=1
            )
        b.save()
        return 1

    def ValidateUser(userLogin, userPassword):
        q = Query.PendingUser.objects.get(login=userLogin)
        if q.password == userPassword:
            return 1
        return 0

    def ActivateUser(userLogin):
        q = Query.PendingUser.objects.get(login=userLogin)
        q.status = 1
        q.save()
        return 1

    def GetUserInfo(userLogin):
        q = Query.PendingUser.objects.get(login=userLogin)
        return q

    def GetNodeInfo(nodeName):
        q = Query.Node.objects.get(node_name=nodeName)
        return q

    def GetImageInfo(imageName):
        q = Query.Image.objects.get(image_name=imageName)
        return q

    #CreateReservation
    def CreateReservation(userLogin, imageName, rdate, rstartTime, rendTime):
        uId = GetUserInfo(userLogin).id
        gId = GetImageInfo(imageName)
        b = Reservation(
            user_id=uId,
            image_id=gId,
            request_date=rdate,
            start_time=rstartTime,
            end_time=rendTime
         )
        b.save()

    #GetUserReservation
    def GetUserReservation(userLogin):
        uId = GetUserInfo(userLogin).id
        q = Query.Image.objects.get(entry__user_login__contains==userLogin)
        return q"""

# CheckSliceTime

# PrepareNodes

# GetUserAccessLog

# LoadImage

# SaveImage

# CleanNode

# EndSession

# ExecuteScript

# UpdateSystem
