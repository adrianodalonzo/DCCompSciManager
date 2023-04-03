from flask import Blueprint, render_template, request

bp = Blueprint("courses", __name__, url_prefix="/courses/")

@bp.route("/", methods=['GET', 'POST'])
def show_courses():
    return render_template('courses.html')