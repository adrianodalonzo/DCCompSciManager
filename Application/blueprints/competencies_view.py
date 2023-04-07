from flask import Blueprint, render_template, request, flash
from ..dbmanager import get_db

bp = Blueprint("competencies", __name__, url_prefix="/competencies/")

@bp.route("/<course_id>", methods=['GET', 'POST'])
def show_competencies(course_id):
    if request.method == 'GET':
        competencies = get_db().get_course_competencies(course_id)
        if competencies:
            elements_array = []
            for competency in competencies:
                elements_array.append(get_db().get_competency_elements(competency.id))
            return render_template('competencies.html', competencies=competencies, elements_array=elements_array)
        
        flash("The competencies does not exist.")
    return render_template('index.html')
