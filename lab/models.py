from django.db import models
import uuid
from portal.models import MyUser as User


class ExperimentTemplate(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=128)
    description = models.TextField()
    duration = models.DurationField()
    ssh_allowed = models.BooleanField()


class Course(models.Model):
    owner = models.ForeignKey(User)
    instructors = models.ManyToManyField(User)
    students = models.ManyToManyField(User)
    title = models.CharField(max_length=64)
    description = models.TextField()
    active = models.BooleanField()
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    experiments = models.ManyToManyField(ExperimentTemplate,
                                         through='Experiment')


class Experiment(models.Model):
    course = models.ForeignKey(Course)
    template = models.ForeignKey(ExperimentTemplate)
    due_date = models.DateTimeField()
