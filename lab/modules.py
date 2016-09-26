from . import models


# Still to be implemented using
# functions provided from the portal
class User(object):
    @staticmethod
    def get(id):
        pass

    @staticmethod
    def is_instructor(user):
        pass

    @staticmethod
    def is_student(user):
        pass

    @staticmethod
    def list_experiments(user):
        pass

    @staticmethod
    def list_courses(user):
        pass

    @staticmethod
    def list_templates(user):
        pass

    @staticmethod
    def join_course(key):
        pass


class ExperimentTemplate(object):
    # Returns ExperimentTemplate object or None if it doesn't exist
    @staticmethod
    def get(id):
        try:
            return models.ExperimentTemplate.objects.get(id)
        except:
            return None

    # Create new template
    # Returns ExperimentTemplate object or None if error
    @staticmethod
    def new(owner_id, title, description, duration, ssh_allowed):
        owner = User.get(owner_id)
        if owner is not None and User.is_instructor(owner):
            e = models.ExperimentTemplate(
                owner=owner,
                title=title,
                description=description,
                duration=duration,
                ssh_allowed=ssh_allowed
            )
            e.save()
            return e
        else:
            return None

    # Delete template
    @staticmethod
    def delete(id):
        e = ExperimentTemplate.get(id)
        if e is not None:
            e.delete()

    # Edit template
    @staticmethod
    def edit(id, title, description, duration, ssh_allowed):
        e = ExperimentTemplate.get(id)
        if e is not None:
            e.title = title
            e.description = description
            e.duration = duration
            e.ssh_allowed = ssh_allowed
            e.save()


class Experiment(object):
    # Returns Experiment object or None if it doesn't exist
    @staticmethod
    def get(id):
        try:
            return models.Experiments.objects.get(id)
        except:
            return None


class Course(object):
    # Returns Course object or None if it doesn't exist
    # Input (id: course_id)
    @staticmethod
    def get(id):
        try:
            return models.Course.objects.get(id)
        except:
            return None

    # Returns new Course object or None if error
    # Input (owner_id: user id, title: string, description: string)
    @staticmethod
    def new(owner_id, title, description):
        owner = User.get(owner_id)
        if User.is_instructor(owner):
            c = models.Course(owner=owner, title=title,
                              description=description)
            c.save()
            return c
        else:
            return None

    # Deletes course and its experiments
    # Input (id: course_id)
    @staticmethod
    def delete(id):
        c = Course.get(id)
        if c is not None:
            c.delete()

    # Adds instructor to course
    @staticmethod
    def add_instructor(course_id, instructor_id):
        course = Course.get(course_id)
        instructor = User.get(instructor_id)
        if course is not None and User.is_instructor(instructor):
            course.instructors.add(instructor)

    # Remove instructor from course
    @staticmethod
    def remove_instructor(course_id, instructor_id):
        course = Course.get(course_id)
        instructor = User.get(instructor_id)
        if course is not None:
            course.instructors.remove(instructor)

    # Adds student to course
    @staticmethod
    def add_student(course_id, student_id):
        course = Course.get(course_id)
        student = User.get(student_id)
        if course is not None and User.is_student(student):
            course.students.add(student)

    # Remove student from course
    @staticmethod
    def remove_student(course_id, student_id):
        course = Course.get(course_id)
        student = User.get(student_id)
        if course is not None:
            course.students.remove(student)

    # Enables a course
    @staticmethod
    def enable(course_id):
        course = Course.get(course_id)
        if course is not None:
            course.active = True
            course.save()

    # Disables a course
    @staticmethod
    def disable(course_id):
        course = Course.get(course_id)
        if course is not None:
            course.active = False
            course.save()

    # Adds an experiment to course
    @staticmethod
    def add_experiment(course_id, template_id, due_date):
        course = Course.get(course_id)
        template = ExperimentTemplate.get(template_id)
        if course is not None and template is not None:
            e = models.Experiments(course=course, template=template,
                                   due_date=due_date)
            e.save()

    # Change experiment due date
    @staticmethod
    def delay_experiment(experiment_id, due_date):
        experiment = Experiment.get(experiment_id)
        if experiment is not None:
            experiment.due_date = due_date
            experiment.save()

    # Delete experiment from course
    @staticmethod
    def cancel_experiment(experiment_id):
        experiment = Experiment.get(experiment_id)
        if experiment is not None:
            experiment.delete()
