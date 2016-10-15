from django.conf.urls import url  # patterns

from lab.Ins_coursesview import CoursesView
from lab.Ins_addcourse import AddCourseView
from lab.Ins_experimentsview import ExperimentsView, experiments_cancel
from lab.ins_validationview import ValidatePendingView
from lab.ins_manage_std import ManageStudentView, student_disable, student_enable
from lab.std_courseview import StudentCoursesView, student_course_cancel
from lab.std_addcourse import StudentAddCourseView
from lab.std_experimentsview import StudentExperimentsView
from lab.std_reserve import StudentReserveView, check_availability_bulk
from lab.library_addview import AddLibraryView
from lab.library_view import LibraryView
from portal.reservationview import ReservationView, check_availability


urlpatterns = [
    # Instructors
    url(r'^validate/?$', ValidatePendingView.as_view(), name="Validation"),
    url(r'^students/?$', ManageStudentView.as_view(), name="Manage Students"),
    url(r'^students/en/(?P<sid>[0-9]+)/$', student_enable ),
    url(r'^students/de/(?P<sid>[0-9]+)/$', student_disable ),

    url(r'^courses/?$', CoursesView.as_view(), name='Courses List'),
    url(r'^courses/add?$', AddCourseView.as_view(), name='Add Course'),
    url(r'^courses/(?P<cid>[0-9]+)/$', AddCourseView.as_view(), name='Edit Course'),
    url(r'^experiments/?$', ExperimentsView.as_view(), name='Experiments List'),
    url(r'^experiments/(bulk)?$', ReservationView.as_view(), name='Add Experiments'),
    url(r'^experiments/cancel/(?P<exp>[0-9]+)/$', experiments_cancel),
    url(r'^experiments/check_availability?$', check_availability),

    # Students
    url(r'^my_courses/?$', StudentCoursesView.as_view(), name='My Courses'),
    url(r'^my_courses/add?$', StudentAddCourseView.as_view(), name='Enroll a new Course'),
    url(r'^my_courses/del/(?P<cid>[0-9]+)/$', student_course_cancel),
    url(r'^my_courses/experiments?$', StudentExperimentsView.as_view(), name='Enroll a new Course'),
    url(r'^my_courses/reserve/(?P<exp>[0-9]+)/$', StudentReserveView.as_view(), name='Reserve'),
    url(r'^my_courses/reserve/check_availability?$', check_availability_bulk),

    # library
    url(r'^library/add?$', AddLibraryView.as_view(), name='Add Library'),
    url(r'^library?$', LibraryView.as_view(), name='Library View'),
]
