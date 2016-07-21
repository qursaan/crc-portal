from django.contrib import admin
from lab.models import Course, StudentCourses, Experiments
# Register your models here.


@admin.register(Course)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('instructor_ref', 'title', 'code', 'key', 'description', 'is_active', 'max_students' ,'created')


@admin.register(StudentCourses)
class StudentCoursesAdmin(admin.ModelAdmin):
    list_display = ('students_ref', 'course_ref', 'added')


@admin.register(Experiments)
class ExperimentsAdmin(admin.ModelAdmin):
    list_display = ('instructor_ref', 'course_ref', 'title', 'due_date', 'reservation_type', 'description', 'max_duration' ,'server_type','reservation_ref','sim_reservation_ref','created')