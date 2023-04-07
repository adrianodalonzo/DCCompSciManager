from flask import Blueprint, render_template, request, flash
from ..dbmanager import get_db

bp = Blueprint("courses", __name__, url_prefix="/courses/")

@bp.route("/", methods=['GET', 'POST'])
def show_courses():
    courses = get_db().get_all_courses()
    if courses:
        return render_template('courses.html', courses=courses)
    flash("No courses")
    return render_template('courses.html')