from flask import Blueprint, render_template, request

bp = Blueprint("course", __name__, url_prefix="/course/")

@bp.route("/", methods=['GET', 'POST'])
def show_course():
    return render_template('course.html')