from django.db import models

# Create your models here.
from portal.models import MyUser, PhysicalNode


class Values(models.Model):
    usernameID = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    deviceID = models.ForeignKey(PhysicalNode, on_delete=models.CASCADE)
    varValue = models.CharField(max_length=50)
    varname = models.CharField(max_length=50)
    timestamp = models.DateTimeField()


def __unicode__(self):
    return self.usernameID + " :" + self.deviceID + " :" + self.varname + " :" + self.varValue + " :" + self.timestamp


class Node_Phy_Details(models.Model):
    deviceID = models.ForeignKey(PhysicalNode, on_delete=models.CASCADE)
    deviceDescr = models.CharField(max_length=150)
    devicePort = models.CharField(max_length=50)
    deviceBaud = models.CharField(max_length=50)
    deviceSignture = models.CharField(max_length=10)
    deviceRbAddress = models.CharField(max_length=20)
    DevType = models.CharField(max_length=1)


def __unicode__(self):
    return self.deviceID + " " + self.deviceDescr + " " + self.devicePort


# MyUser PhysicalNode

class Variable(models.Model):
    usernameID = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    deviceID = models.ForeignKey(PhysicalNode, on_delete=models.CASCADE)
    varName = models.CharField(max_length=50)


def __unicode__(self):
    return self.usernameID + " " + self.deviceID + " " + self.varName


class output(models.Model):
    deviceID = models.ForeignKey(PhysicalNode, on_delete=models.CASCADE)
    outputName = models.CharField(max_length=50)
    value = models.IntegerField()


def __unicode__(self):
    return self.usernameID + " " + self.deviceID + " " + self.value
