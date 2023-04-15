from flask import Blueprint, render_template, request, flash

from Application.objects.course import Course, CourseForm
from ..dbmanager import get_db

bp = Blueprint("courses", __name__, url_prefix="/courses/")

@bp.route("/", methods=['GET', 'POST'])
def show_courses():
    courses = get_db().get_all_courses()
    if courses:
        return render_template('courses.html', courses=courses)
    flash("No courses")
    return render_template('index.html')

@bp.route("/domain/<int:domain_id>/", methods=['GET', 'POST'])
def show_courses_by_domain(domain_id):
    courses = get_db().get_courses_by_domain(domain_id)
    if courses:
        domain = get_db().get_domain(domain_id)
        return render_template('courses.html', courses=courses, domain=domain)
    flash("No courses by this domain")
    return render_template('index.html')

@bp.route("/term/<int:term_id>/", methods=['GET', 'POST'])
def show_courses_by_term(term_id):
    courses = get_db().get_courses_by_term(term_id)
    if courses:
        return render_template('courses.html', courses=courses, term=term_id)
    flash("No courses by this term")
    return render_template('index.html')

@bp.route("/add/", methods=['GET', 'POST'])
def add_course():
    form = CourseForm()

    if request.method == 'GET':
        return render_template('modify_course.html', form=form)

    elif request.method == 'POST':
        if form.validate_on_submit():
            matchingCourse = False

            for course in get_db().get_all_courses():
                if course.id == form.id.data:
                    matchingCourse = True
                    flash("A Course with the same number already exists!")
            
            if not matchingCourse:
                course = Course(form.id.data, form.title.data, form.theory_hours.data, 
                                form.lab_hours.data, form.work_hours.data, 
                                form.description.data, form.domain_id.data, form.term_id.data)
                # get_db().add_course(course)
                # ^ not implemented yet

@bp.route("/edit/<string:course_id>/", methods=['GET', 'POST'])
def edit_course(course_id):
    form = CourseForm()
    course = get_db().get_course(course_id)

    if request.method == 'GET':
        return render_template('modify_course.html', form=form, course=course)
    
    elif request.method == 'POST':
        if form.validate_on_submit():
            pass