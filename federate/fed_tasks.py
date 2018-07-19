from crc import settings
from portal.models import MyUser
from django.contrib.auth import authenticate
from federate.models import Users, Site
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
import base64
import json
import urllib2
import urllib
from django.core import serializers


def auth_federate_user(username, password):
    if settings.FED_RUN == 1:
        curr_user = Users.objects.filter(username__iexact=username)
        if curr_user:
            s = curr_user[0].site_ref
            # Site is Active
            if s.status == 2:
                # READ REMOTE SITE
                print "READ USERS AUTH FROM ", s.name
                try:

                    try:
                        from Crypto.PublicKey import RSA

                        newkey = RSA.importKey(json.loads(s.public_key))
                        enc_username = newkey.encrypt(username, 32)
                        enc_password = newkey.encrypt(password, 32)
                        # pkey = RSA.importKey(json.loads(s.private_key))
                        # dec_data = pkey.decrypt(enc_data)
                        # print dec_data

                    except Exception as ins:
                        print "ERROR: ", ins.message

                    post_data = {
                        "username": enc_username,
                        "password": enc_password
                    }
                    print post_data
                    post_data = urllib.urlencode(post_data)

                    response_data = urllib2.urlopen(s.url + 'federation/fed/getAuth?' + post_data)
                except Exception as inst:
                    print "ERROR CONNECT TO SITE ", s.name
                    response_data = None
                if response_data:
                    readd = response_data.read()
                    loadd = json.loads(json.loads(readd).encode("ascii", "replace"))

                    print "DATA: ", loadd
                    if loadd == 1:
                        return True
    return False


def federate_getAuth(request):
    if request.method != 'GET':
        return HttpResponseRedirect("/")
    try:
        response_data = {}
        print settings.FED_RUN
        if settings.FED_RUN == 1:
            username = request.GET.get('username', None);
            password = request.GET.get('password', None);

            try:
                s = Site.objects.get(id=1)
                from Crypto.PublicKey import RSA
                pkey = RSA.importKey(json.loads(s.private_key))
                dec_username = pkey.decrypt(username)
                dec_password = pkey.decrypt(password)
                # print dec_data

            except Exception as ins:
                print "ERROR: ", ins.message

            auth_result = authenticate(username=dec_username, password=dec_password)
            if auth_result:
                response_data = "1"
            else:
                response_data = "0"

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except:
        return HttpResponse(json.dumps({"error": "this isn't happening"}), content_type="application/json")


# @login_required
def federate_getUsers(request):
    if request.method != 'GET':
        return HttpResponseRedirect("/")

    try:
        response_data = {}
        print settings.FED_RUN
        if settings.FED_RUN == 1:
            response_data = serializers.serialize('json', MyUser.objects.all(), fields=('username'))
            s = Site.objects.get(id=1)
            '''try:
                from Crypto.PublicKey import RSA

                newkey = RSA.importKey(json.loads(s.public_key))
                enc_data = newkey.encrypt( "1234567",32)
                print enc_data
                pkey = RSA.importKey(json.loads(s.private_key))
                dec_data = pkey.decrypt(enc_data)
                print dec_data
            except Exception as ins:
                print "ERROR: " , ins.message'''

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except:
        return HttpResponse(json.dumps({"error": "this isn't happening"}), content_type="application/json")
