from flask import Blueprint, render_template, request, flash
from ..dbmanager import get_db


bp = Blueprint("course", __name__, url_prefix="/course/")

@bp.route("/<course_id>", methods=['GET', 'POST'])
def show_course(course_id):
    course = get_db().get_course(course_id)
    if course:
        return render_template('course.html', course=course)
    flash("The course does not exist.")
    return render_template('index.html') 
