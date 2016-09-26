from django.contrib import admin
from lab.models import Course, StudentCourses, Experiments,StudentsExperiment, InstalledLab, LabsTemplate, LabsParameter
# Register your models here.


@admin.register(Course)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('id', 'instructor_ref', 'title', 'code', 'key', 'description', 'is_active', 'max_students' ,'created')


@admin.register(StudentCourses)
class StudentCoursesAdmin(admin.ModelAdmin):
    list_display = ('id', 'students_ref', 'course_ref', 'added')


@admin.register(StudentsExperiment)
class StudentsExperimentAdmin(admin.ModelAdmin):
    list_display = ('id', 'students_ref', 'experiment_ref', 'reservation_ref','sim_reservation_ref','start_time','end_time','status')


@admin.register(Experiments)
class ExperimentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'instructor_ref', 'course_ref', 'title', 'due_date', 'reservation_type', 'description', 'max_duration' ,'server_type','reservation_ref','sim_reservation_ref','created')


@admin.register(InstalledLab)
class InstalledLabAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(LabsTemplate)
class LabsTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'lab_ref', 'exp_param')


@admin.register(LabsParameter)
class LabsParameterAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'lab_ref', 'def_value', 'values', 'type')
