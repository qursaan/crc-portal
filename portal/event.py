# !/usr/bin/python
# -*-coding: utf-8-*-

import pickle
import os.path
import xmlrpclib
import ast
import time

class Event:
    def __init__(self, structure):
        self.srv=""
        self.structure = structure
        self.authType = ""
        self.server = ""
        self.methode = ""
        self.parameters = {}
        self.return_fields = []
        
        self.auth = {}
        self.print_method=""
        self.print_options=""
        self.geo_methode=""
        self.id=""
        
        ##APE###
        self.raw = ""
        self.channel = ""
        #######

        self.data = self.make_data()

    def split(self):
        args = self.structure.split(";");
        self.raw = args[0]
        self.channel = args[1]
        self.print_method = args[2]
        self.print_options = ast.literal_eval(args[3])
        self.authType = args[4]
        self.server = ast.literal_eval(args[5])
        self.server = self.server["server"]
        self.methode = args[6]
        self.parameters = ast.literal_eval(args[7])
        self.return_fields = eval(args[8])
        
    def makeAuth(self): 
        if self.authType=="anonymous":
            self.auth["AuthMethod"] = "anonymous"
        elif type=="password":
            self.auth["AuthMethod"] = "password"
            self.auth["Username"] = "XXX"
            self.auth["AuthString"] = "XXX"
        elif self.authType=="session":
            self.auth["AuthMethod"] = "session"
            self.auth["session"] = "XXX"
        elif self.authType=="gpg":
            self.auth["AuthMethod"] = "gpg"
            self.auth["name"] = "XXX"
            self.auth["signature"] = "XXX"
    
    def include_geoposition(self, data):
        list=[]
        if len(data)<8:
            for i in data:
                i["ape_position"] = self.get_geoposition(i) 
                list.append(i)
            return list
        else:
            try:
                sites_id = self.srv.GetSites(self.auth,{},["site_id","latitude","longitude"])
            except :
                return 45
            try:
                for i in data:
                    for j in sites_id:
                        if i["site_id"]==j["site_id"]:
                            try:
                                pos=[{"latitude": j["latitude"], "longitude": j["longitude"]}]
                            except:
                                return 83
                            #
                            i["ape_position"] = pos
                            list.append(i)
            except:
                return 82      
            return list
        
    def get_geoposition(self,i):
        if self.geo_methode == "site_id":
            id = i["site_id"]
            try:
                geo_pos =  self.srv.GetSites(self.auth, {"site_id": id}, ["latitude","longitude"])
            except:
                geo_pos = 43
            return geo_pos
        else:
            return 42

    def get_event_list_from_xmlrpc(self):
        self.srv = xmlrpclib.Server(self.server, allow_none = 1)
        if self.methode=="GetSites":
            self.geo_methode="site_id";
            try :
                if len(self.return_fields)==0:
                    return self.srv.GetSites(self.auth, self.parameters) 
                else :
                    return self.srv.GetSites(self.auth, self.parameters, self.return_fields)
            except:
                    return 0
        else:
            return 0
    
    def make_data(self):
        try :
            self.split()
            self.makeAuth()
        except:
            return 43

        try :
            rototo = self.get_event_list_from_xmlrpc()
        except: 
            return 44

        try:
            return self.include_geoposition(rototo)
        except:
            return 47