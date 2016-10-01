
from lab.models import StudentCourses, StudentsExperiment, Experiments, Course, LabsParameter
from portal.models import MyUser  # , PendingSlice
from portal.reservation_status import ReservationStatus
from portal.actions import get_user_by_email

from django.utils import timezone


def add_course_by_email(course, student_email):
    std = get_user_by_email(student_email)
    if std:
        dup = StudentCourses.objects.filter(students_ref=std, course_ref=course)
        if not dup:
            sc = StudentCourses(
                students_ref=std,
                course_ref=course,
            )
            sc.save()


def add_all_courses_by_email(user_emails):
    courses = Course.objects.filter(email_list__contains=user_emails)
    for c in courses:
        add_course_by_email(c, user_emails)


def remove_course_by_emails(user_emails, course_id):
    course = Course.objects.filter(id=course_id, email_list__contains=user_emails)
    if course:
        new_email_list = course[0].email_list
        new_email_list = new_email_list.replace(user_emails, "")
        course[0].email_list = new_email_list
        course[0].save()



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
    pending = MyUser.objects.filter(status=1, supervisor_id=c_user.id, user_type=3).all()
    return pending.count()


def get_count_students(c_user):
    status_list = [0, 2]
    students = MyUser.objects.filter(supervisor_id=c_user.id, status__in=status_list, user_type=3).all()
    return students.count()


def get_control_options(stype, reserve_ref):
    allow_img = True
    allow_ssh = True
    allow_crt = True
    supp_file = None
    s_exp = None
    lab_param_list = []
    
    if stype == "omf":
        s_exp = StudentsExperiment.objects.filter(reservation_ref=reserve_ref)
    elif stype == "sim":
        s_exp = StudentsExperiment.objects.filter(sim_reservation_ref=reserve_ref)
    if s_exp:
        allow_crt = s_exp[0].experiment_ref.allow_crt
        allow_ssh = s_exp[0].experiment_ref.allow_ssh
        allow_img = s_exp[0].experiment_ref.allow_img
        supp_file = s_exp[0].experiment_ref.sup_files
        lab_temp_ref = s_exp[0].experiment_ref.lab_template_ref
        if lab_temp_ref:
            lab_param_list = LabsParameter.objects.filter(lab_ref=lab_temp_ref.lab_ref)
    return allow_crt, allow_img, allow_ssh, supp_file, lab_temp_ref, lab_param_list


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

