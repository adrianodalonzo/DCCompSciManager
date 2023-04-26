from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import current_user, login_required

from Application.objects.course import Course, CourseForm
from Application.objects.element import CourseElementForm
from ..dbmanager import get_db

from werkzeug.datastructures import MultiDict

bp = Blueprint("courses", __name__, url_prefix="/courses/")

@bp.route("/", methods=['GET', 'POST'])
@login_required
def show_courses():
    if current_user.blocked:
        flash('You Have Been Blocked by an Admin!', category='invalid')
        return redirect(url_for('profile.get_profile', email=current_user.email))
    courses = get_db().get_all_courses()
    if courses:
        return render_template('courses.html', courses=courses)
    flash("No courses", category='invalid')
    return render_template('index.html')

@bp.route("/<string:course_id>/", methods=['GET', 'POST'])
@login_required
def show_course(course_id):
    course = get_db().get_course(course_id)
    elements = get_db().get_course_elements(course_id)

    if course:
        return render_template('course.html', course=course, elements=elements)
    flash("The course does not exist.", category='invalid')
    return render_template('index.html') 

@bp.route("/domain/<int:domain_id>/", methods=['GET', 'POST'])
@login_required
def show_courses_by_domain(domain_id):
    courses = get_db().get_courses_by_domain(domain_id)
    if courses:
        domain = get_db().get_domain(domain_id)
        return render_template('courses.html', courses=courses, domain=domain)
    flash("No courses by this domain", category='invalid')
    return render_template('index.html')

@bp.route("/term/<int:term_id>/", methods=['GET', 'POST'])
@login_required
def show_courses_by_term(term_id):
    courses = get_db().get_courses_by_term(term_id)
    if courses:
        return render_template('courses.html', courses=courses, term=term_id)
    flash("No courses by this term", category='invalid')
    return render_template('index.html')

@bp.route("/add/", methods=['GET', 'POST'])
@login_required
def add_course():
    form = CourseForm()
    form.domain_id.choices=get_db().get_domain_choices()

    if request.method == 'GET':
        return render_template('modify_course.html', form=form)

    elif request.method == 'POST':
        if form.validate_on_submit():
            matchingCourse = False

            for course in get_db().get_all_courses():
                if course.id == form.id.data:
                    matchingCourse = True
                    flash("A Course with the same number already exists!", category='invalid')
            
            if not matchingCourse:
                course = Course(form.id.data, form.title.data, form.theory_hours.data, 
                                form.lab_hours.data, form.work_hours.data, 
                                form.description.data, form.domain_id.data, form.term_id.data)
                get_db().add_course(course)
                flash("Added Course: " + course.title, category='valid')
    
    return redirect(url_for('show_courses'))

@bp.route("/edit/<string:course_id>/", methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    course = get_db().get_course(course_id)
    form = CourseForm(obj=course)
    form.domain_id.choices=get_db().get_domain_choices()

    if request.method == 'GET':
        return render_template('modify_course.html', form=form, course=course)
    
    elif request.method == 'POST':
        if form.validate_on_submit():
            
            course_title = form.title.data
            course_theo_hours = form.theory_hours.data
            course_lab_hours = form.lab_hours.data
            course_work_hours = form.work_hours.data
            course_desc = form.description.data
            course_dom_id = form.domain_id.data
            course_term_id = form.term_id.data

            if course_title is None:
                course_title = course.title
            if course_theo_hours is None:
                course_theo_hours = course.theory_hours
            if course_lab_hours is None:
                course_lab_hours = course.lab_hours
            if course_work_hours is None:
                course_work_hours = course.work_hours
            if course_desc is None:
                course_desc = course.description
            if course_dom_id is None:
                course_dom_id = course.domain_id
            if course_term_id is None:
                course_term_id = course.term_id
            
            edited_course = Course(course_id, course_title, course_theo_hours, course_lab_hours,
                                   course_work_hours, course_desc, course_dom_id, course_term_id)
            get_db().modify_course(edited_course)
            flash("Edited Course: " + course_title, category='valid')

    return redirect(url_for('show_courses'))

@bp.route("/delete/<string:course_id>/")
@login_required
def delete_course(course_id):
    get_db().delete_course(course_id)
    flash("Course " + course_id + " has been deleted", category='valid')
    return redirect(url_for('show_courses'))

@bp.route("/element/add/<string:course_id>/", methods=['GET', 'POST'])
@login_required
def add_course_element(course_id):
    if get_db().get_course(course_id) is None:
        flash("Could not find course " + course_id, category='invalid')
        return redirect(url_for('courses.show_course', course_id=course_id))
    
    form = CourseElementForm()
    form.id.choices = get_db().get_all_elements()

    if request.method == 'GET':
        return render_template("modify_course_elements.html", form=form)
    
    elif request.method == 'POST':
        if form.validate_on_submit():
            matchingCourseElement = False

            for element in get_db().get_course_elements(course_id):
                if form.id.data == str(element.id):
                    matchingCourseElement = True
                    flash("Course " + course_id + " already has this element!", category='invalid')    

            if not matchingCourseElement:
                get_db().add_course_element(course_id, form.id.data, form.hours.data)
                flash("Course Element Added Succesfully", category='valid')
    
    return redirect(url_for('courses.show_course', course_id=course_id))

@bp.route("/element/edit/<string:course_id>/<string:elem_id>", methods=['GET', 'POST'])
@login_required
def edit_course_element(course_id, elem_id):
    if get_db().get_course(course_id) is None:
        flash("Could not find course " + course_id, category='invalid')
        return redirect(url_for('courses.show_course', course_id=course_id))
    
    element = get_db().get_element_by_both_id(course_id, elem_id)

    form = CourseElementForm()
    form.id.choices = [(elem_id, element.name)]

    if request.method == 'GET':
        return render_template('modify_course_elements.html', form=form, elem_id=elem_id)
    
    elif request.method == 'POST':
        form.id.data = elem_id
        if form.validate_on_submit():
            get_db().edit_course_element(course_id, elem_id, form.hours.data)
            flash("Edited Course Element Succesfully", category='valid')
        else:
            flash("Unsuccesfully Edited Course Element", category='invalid')

    return redirect(url_for('courses.show_course', course_id=course_id))

@bp.route("/element/delete/<string:course_id>/<string:elem_id>")
@login_required
def delete_course_element(course_id, elem_id):
    get_db().delete_course_element(course_id, elem_id)
    flash("Deleted Course Element Succesfully", category='valid')
    return redirect(url_for('courses.show_course', course_id=course_id))