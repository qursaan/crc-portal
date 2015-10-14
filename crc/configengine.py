import os.path
from ConfigParser import RawConfigParser
from crc.settings import ROOT

#
# DO NOT EDIT !!!
#
# This file does not contain any user-modifiable data
#
# te defaults here are, well, only default values,
# and, you have the option to override them
# by writing a file myslice/myslice.ini
# that looks like this
#[manifold]
#url = http://manifold.pl.sophia.inria.fr:7080/
#admin_user = admin
#admin_password = admin
#[googlemap]
#api_key=theapikeyasprovidedbygoogle

# use a singleton instead of staticmethods
from manifold.util.singleton import Singleton

class ConfigEngine(object):
    __metaclass__ = Singleton

    # the OpenLab-wide backend as managed by UPMC
    # xxx production should probably use https of course
    default_manifold_url = "https://test.crclab.org:7080/"
    # the devel/unstable version runs on "https://dev.myslice.info:7080/"
    # if you use a development backend running on this box, use "http://localhost:7080/"
    # the INRIA setup is with "https://manifold.pl.sophia.inria.fr:7080/"

    default_manifold_admin_user     = 'admin'
    default_manifold_admin_password = '123'


    def __init__ (self):
        parser = RawConfigParser ()
        parser.add_section('manifold')
        parser.set ('manifold', 'url', ConfigEngine.default_manifold_url)
        parser.set ('manifold', 'admin_user', ConfigEngine.default_manifold_admin_user)
        parser.set ('manifold', 'admin_password', ConfigEngine.default_manifold_admin_password)
#q        parser.add_section('googlemap')
#q        parser.set ('googlemap','api_key', None)
        parser.read (os.path.join(ROOT,'crc/crc.ini.localhost'))
        #print "qursaan", os.path.join(ROOT,'crc/crc.ini')
        self.config_parser=parser

    def manifold_url (self):
        return self.config_parser.get('manifold', 'url')

    def manifold_admin_user_password(self):
        return (self.config_parser.get('manifold', 'admin_user'),
                self.config_parser.get('manifold', 'admin_password'))

#q    def googlemap_api_key (self):
#q        return self.config_parser.get('googlemap','api_key')

    # exporting these details to js
    def manifold_js_export (self):
        return "var MANIFOLD_URL = '%s';\n"%self.manifold_url();
