from flask import Blueprint, render_template, request, flash
from ..dbmanager import get_db

bp = Blueprint("competencies", __name__, url_prefix="/competencies/")

@bp.route("/<competency_id>", methods=['GET', 'POST'])
def show_competencies(competency_id):
    if request.method == 'GET':
        competencies = get_db().get_course_competencies(competency_id)
        if competencies:
            return render_template('competencies.html', competencies=competencies)
        else:
            flash("404, The competency does not exist.")
    return render_template('competencies.html', competencies=competencies)