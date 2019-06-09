#from django.conf.urls import url  # patterns
from django.urls import re_path  # patterns

from lab.Ins_addcourse import AddCourseView
from lab.Ins_coursesview import CoursesView
from lab.Ins_experimentsview import ExperimentsView, experiments_cancel
from lab.ins_manage_std import ManageStudentView, student_disable, student_enable
from lab.ins_validationview import ValidatePendingView
from lab.library_addview import AddLibraryView
from lab.library_view import LibraryView, download
from lab.std_addcourse import StudentAddCourseView
from lab.std_courseview import StudentCoursesView, student_course_cancel
from lab.std_experimentsview import StudentExperimentsView
from lab.std_reserve import StudentReserveView, check_availability_bulk
from portal.reservationview import ReservationView, check_availability

urlpatterns = [
    # Instructors
    re_path(r'^validate/?$', ValidatePendingView.as_view(), name="Validation"),
    re_path(r'^students/?$', ManageStudentView.as_view(), name="Manage Students"),
    re_path(r'^students/en/(?P<sid>[0-9]+)/$', student_enable ),
    re_path(r'^students/de/(?P<sid>[0-9]+)/$', student_disable ),

    re_path(r'^courses/?$', CoursesView.as_view(), name='Courses List'),
    re_path(r'^courses/add?$', AddCourseView.as_view(), name='Add Course'),
    re_path(r'^courses/(?P<cid>[0-9]+)/$', AddCourseView.as_view(), name='Edit Course'),
    re_path(r'^experiments/?$', ExperimentsView.as_view(), name='Experiments List'),
    re_path(r'^experiments/(bulk)?$', ReservationView.as_view(), name='Add Experiments'),
    re_path(r'^experiments/cancel/(?P<exp>[0-9]+)/$', experiments_cancel),
    re_path(r'^experiments/check_availability?$', check_availability),

    # Students
    re_path(r'^my_courses/?$', StudentCoursesView.as_view(), name='My Courses'),
    re_path(r'^my_courses/add?$', StudentAddCourseView.as_view(), name='Enroll a new Course'),
    re_path(r'^my_courses/del/(?P<cid>[0-9]+)/$', student_course_cancel),
    re_path(r'^my_courses/experiments?$', StudentExperimentsView.as_view(), name='Enroll a new Course'),
    re_path(r'^my_courses/reserve/(?P<exp>[0-9]+)/$', StudentReserveView.as_view(), name='Reserve'),
    re_path(r'^my_courses/reserve/check_availability?$', check_availability_bulk),

    # library
    re_path(r'^library/add?$', AddLibraryView.as_view(), name='Add Library'),
    re_path(r'^library?$', LibraryView.as_view(), name='Library View'),

    re_path(r'^download/(?P<path>.*)$', download),
]
