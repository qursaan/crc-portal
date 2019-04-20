__author__ = 'pirate'

import json
# noinspection PyCompatibility
import urllib

from federate.models import Site


# from crc.settings import BACKENDIP


def validate_key(site, pkey):
    post_data = {
        'pkey': pkey
    }

    try:
        post_data = json.dumps(post_data).encode('utf8')
        req = urllib.request.Request(site + 'federation/api/valid/key/', data=post_data,
                                     headers={'Content-Type': 'application/json'})
        result = urllib.request.urlopen(req)
        print("Results:", result)
        if result.getcode() == 200:
            data = result.read()
            if "ok" in data:
                return 1
    except Exception as ins:
        print("ERROR: ", ins.message)
        return 2

    return 0


def api_fed_valid_key(request):
    json_req = request.get_json(force=True, silent=True)

    if json_req is None or 'pkey' not in json_req:
        return json.dumps({'status': 'false'})
    try:
        pkey = json_req['pkey']
        print("Pkey: ", pkey)
        site = Site.objects.get(id=1)
        if site:
            try:
                from Crypto.PublicKey import RSA

                newkey = RSA.importKey(json.loads(pkey))
                enc_data = newkey.encrypt("1234567", 32)
                print(enc_data)
                pkey = RSA.importKey(json.loads(site.private_key))
                dec_data = pkey.decrypt(enc_data)
                print(dec_data)
            except Exception as ins:
                print("ERROR: ", ins.message)

            if dec_data == "1234567":
                print('ok')
                return json.dumps({'status': 'ok'})
            else:
                return json.dumps({'status': 'false'})
    except:
        return json.dumps({'status': 'false'})
    return json.dumps({'status': 'false'})


def get_fed_resources():
    list = {}
    for s in Site.objects.exclude(id__in=[1]):
        result = urllib.request.urlopen(s.url + 'federate/rest/resources/')
