from django.conf.urls import url  # patterns

from lab.Ins_coursesview import CoursesView
from lab.Ins_addcourse import AddCourseView
from lab.Ins_experimentsview import ExperimentsView
from lab.ins_validationview import ValidatePendingView

from lab.std_courseview import StudentCoursesView
from lab.std_addcourse import StudentAddCourseView
from lab.std_experimentsview import StudentExperimentsView
from lab.std_reserve import StudentReserveView, check_availability_bulk
from portal.reservationview import ReservationView, check_availability


urlpatterns = [
    # Instructors
    url(r'^validate/?$', ValidatePendingView.as_view(), name="Validation" ),

    url(r'^courses/?$', CoursesView.as_view(), name='Courses List'),
    url(r'^courses/add?$', AddCourseView.as_view(), name='Add Course'),
    url(r'^experiments/?$', ExperimentsView.as_view(), name='Experiments List'),
    url(r'^experiments/(bulk)?$', ReservationView.as_view(), name='Add Experiments'),
    # url(r'^experiments/cancel/?P<exp>[0-9]+)/$', ),
    url(r'^experiments/check_availability?$', check_availability),

    # Students
    url(r'^my_courses/?$', StudentCoursesView.as_view(), name='My Courses'),
    url(r'^my_courses/add?$', StudentAddCourseView.as_view(), name='Enroll a new Course'),
    url(r'^my_courses/experiments?$', StudentExperimentsView.as_view(), name='Enroll a new Course'),
    url(r'^my_courses/reserve/(?P<exp>[0-9]+)/$', StudentReserveView.as_view(), name='Reserve'),
    url(r'^my_courses/reserve/check_availability?$', check_availability_bulk),

]
