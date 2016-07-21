from django.db import models
import uuid
from portal.models import Reservation, SimReservation, MyUser  # as User
from django.utils import timezone

'''
class SupervisorStudents(models.Model):
    instructor_ref = models.ForeignKey(MyUser, null=True)
    student_ref = models.ForeignKey(MyUser, null=True)
'''


class Course(models.Model):
    instructor_ref = models.ForeignKey(MyUser, null=True)
    title = models.CharField(max_length=64)
    code = models.CharField(max_length=32, null=True)
    key = models.CharField(max_length=30, null=False)
    # key = models.UUIDField(default=uuid.uuid4, editable=False)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    max_students = models.IntegerField(default=10)
    created = models.DateTimeField(default=timezone.now)

    # owner = models.ForeignKey(User)
    # instructors = models.ManyToManyField(User)
    # students = models.ManyToManyField(User)
    # experiments = models.ManyToManyField(ExperimentTemplate,through='Experiment')

    def __unicode__(self):
        return self.title


class StudentCourses(models.Model):
    students_ref = models.ForeignKey(MyUser, null=True)
    course_ref = models.ForeignKey(Course, null=True)
    added = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.students_ref + "@" + self.course_ref


class Experiments(models.Model):
    title = models.CharField(max_length=64)
    course_ref = models.ForeignKey(Course, null=True)
    instructor_ref = models.ForeignKey(MyUser, null=True)
    due_date = models.DateTimeField(null=True)
    description = models.TextField(null=True)
    created = models.DateTimeField(default=timezone.now)
    # 0=Block 1=Racing
    reservation_type = models.IntegerField(default=0, null=True)
    max_duration = models.IntegerField(default=1)
    server_type = models.CharField(max_length=16, null=True)
    reservation_ref = models.ForeignKey(Reservation, null=True)
    sim_reservation_ref = models.ForeignKey(SimReservation, null=True)
    # 0-Open, 1-Expired
    status = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title


class StudentsExperiment(models.Model):
    students_ref = models.ForeignKey(MyUser, null=True)
    experiment_ref = models.ForeignKey(Experiments, null=True)
    start_time = models.DateTimeField('Start Time', null=True)
    end_time = models.DateTimeField('End Time', null=True)
    # 0-Reserved, 1-Finish, 2-Cancel
    status = models.IntegerField(default=0)

'''
class ExperimentTemplate(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=128)
    description = models.TextField()
    duration = models.DurationField()
    ssh_allowed = models.BooleanField()


class Experiment(models.Model):
    course = models.ForeignKey(Course)
    template = models.ForeignKey(ExperimentTemplate)
    due_date = models.DateTimeField()
'''
