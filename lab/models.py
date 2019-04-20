from django.db import models
from django.utils import timezone
from portal.models import Reservation, SimReservation, MyUser  # as User

'''
class SupervisorStudents(models.Model):
    instructor_ref = models.ForeignKey(MyUser, null=True)
    student_ref = models.ForeignKey(MyUser, null=True)
'''


class InstalledLab(models.Model):
    title = models.CharField(max_length=64)
    requirement = models.CharField(max_length=256, null=True)

    def __str__(self):
        return self.title


class LabsTemplate(models.Model):
    title = models.CharField(max_length=64)
    lab_ref = models.ForeignKey(InstalledLab, null=True, on_delete=models.CASCADE)
    exp_param = models.CharField(max_length=256, null=True)

    def __str__(self):
        return self.title


class LabsParameter(models.Model):
    title = models.CharField(max_length=64)
    param_id = models.CharField(max_length=30, null=True)
    lab_ref = models.ForeignKey(InstalledLab, null=False, on_delete=models.CASCADE)
    type = models.CharField(max_length=64, null=True)
    def_value = models.CharField(max_length=64, null=True)
    values = models.CharField(max_length=256, null=True)

    def values_as_list(self):
        return self.values.split(',')

    def __str__(self):
        return self.title


class Course(models.Model):
    instructor_ref = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    code = models.CharField(max_length=32, null=True)
    key = models.CharField(max_length=30, null=False)
    # key = models.UUIDField(default=uuid.uuid4, editable=False)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    max_students = models.IntegerField(default=10)
    email_list = models.TextField(null=True)
    created = models.DateTimeField(default=timezone.now)

    # owner = models.ForeignKey(User)
    # instructors = models.ManyToManyField(User)
    # students = models.ManyToManyField(User)
    # experiments = models.ManyToManyField(ExperimentTemplate,through='Experiment')

    def __str__(self):
        return self.title


class StudentCourses(models.Model):
    students_ref = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE)
    # students_email = models.CharField(null=True, max_length=64)
    course_ref = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    # 0-Unbinding, 1-Binding
    status = models.IntegerField(default=0)
    added = models.DateTimeField(default=timezone.now)
    # def __str__(self):
    # return self.students_ref.first_name + " @ " + self.course_ref


class Experiments(models.Model):
    title = models.CharField(max_length=64)
    course_ref = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    instructor_ref = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE)
    due_date = models.DateTimeField(null=True)
    description = models.TextField(null=True)
    created = models.DateTimeField(default=timezone.now)
    # 0=Block 1=Racing
    reservation_type = models.IntegerField(default=0, null=True)
    max_duration = models.IntegerField(default=1)
    server_type = models.CharField(max_length=16, null=True)
    reservation_ref = models.ForeignKey(Reservation, null=True, on_delete=models.CASCADE)
    sim_reservation_ref = models.ForeignKey(SimReservation, null=True, on_delete=models.CASCADE)
    # 0-Open, 1-Expired, 2-Deleted
    status = models.IntegerField(default=0)
    # controls
    allow_crt = models.BooleanField(default=False)
    allow_ssh = models.BooleanField(default=False)
    allow_img = models.BooleanField(default=False)
    # files
    sup_files = models.CharField(max_length=256, null=True)
    # existing labs
    lab_template_ref = models.ForeignKey(LabsTemplate, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title


class StudentsExperiment(models.Model):
    students_ref = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE)
    experiment_ref = models.ForeignKey(Experiments, null=True, on_delete=models.CASCADE)
    reservation_ref = models.ForeignKey(Reservation, null=True, on_delete=models.CASCADE)
    sim_reservation_ref = models.ForeignKey(SimReservation, null=True, on_delete=models.CASCADE)
    start_time = models.DateTimeField('Start Time', null=True)
    end_time = models.DateTimeField('End Time', null=True)
    # 0-Reserved, 1-Finish, 2-Cancel
    status = models.IntegerField(default=0)


class CustomLibrary(models.Model):
    user_ref = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=True)
    author = models.CharField(max_length=256, null=True)
    type = models.CharField(max_length=256, null=True)
    tag = models.CharField(max_length=256, null=True)
    external_link = models.TextField(null=True)
    description = models.TextField(null=True)
    file = models.TextField(null=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

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
