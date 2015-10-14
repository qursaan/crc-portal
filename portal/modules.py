# -*- coding: utf-8 -*-
#from django.db import models
#from django.utils import timezone
from portal.models import PendingUser


#from django.contrib.auth.models import User


class Modules:


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




#CheckSliceTime

#PrepareNodes

#GetUserAccessLog

#LoadImage

#SaveImage

#CleanNode

#EndSession

#ExecuteScript

#UpdateSystem

