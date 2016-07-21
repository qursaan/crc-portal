
from lab.models import StudentCourses, Experiments
from portal.models import MyUser  # , PendingSlice
from portal.reservation_status import ReservationStatus

from django.utils import timezone


def get_std_requests(supervisor_id):
    print "get_request_by_supervisor = ", supervisor_id
    pending_users = None

    if supervisor_id:
        pending_users = MyUser.objects.filter(status=1, supervisor_id=supervisor_id).all()

    requests = []
    if pending_users:
        for _user in pending_users:
            requests.append(make_request_user(_user))

    return requests


# ******** Generate user request from user Object ***** #
def make_request_user(user):
    request = {}
    request['type'] = 'user'
    request['id'] = user.id
    request['timestamp'] = user.created  # XXX in DB ?
    request['first_name'] = user.first_name
    request['last_name'] = user.last_name
    request['email'] = user.email
    request['login'] = user.username
    return request


def get_count_students_course(c_user):
    course_list = StudentCourses.objects.filter(students_ref=c_user)
    return course_list.count()


def get_count_students_pending(c_user):
    pending = MyUser.objects.filter(status=1, supervisor_id=c_user.id).all()
    return pending.count()


def get_count_students_experiments(c_user):
    student_course_list = StudentCourses.objects.filter(students_ref=c_user)
    total_count = 0
    for sc in student_course_list:
        active_list_1 = Experiments.objects.filter(course_ref=sc.course_ref, status=0)
        total_count += active_list_1.count()
    return total_count


def get_count_bulk_experiments(c_user):
    active_list_1 = Experiments.objects.filter(instructor_ref=c_user, status=0)

    total_count = active_list_1.count()
    # confirm open session
    for al in active_list_1:
        if al.reservation_ref:
            if al.reservation_ref.status == ReservationStatus.get_expired():
                al.status = 1
                al.save()
                total_count -= 1
        elif al.sim_reservation_ref:
            if al.sim_reservation_ref.status == ReservationStatus.get_expired():
                    al.status = 1
                    al.save()
                    total_count -= 1
    return total_count

