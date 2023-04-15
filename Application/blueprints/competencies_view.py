from flask import Blueprint, redirect, render_template, request, flash, url_for

from Application.objects.competency import Competency
from ..dbmanager import get_db

bp = Blueprint("competencies", __name__, url_prefix="/competencies/")

@bp.route("/<string:course_id>/", methods=['GET', 'POST'])
def show_course_competencies(course_id):
    if request.method == 'GET':
        competencies = get_db().get_course_competencies(course_id)
        if competencies:
            elements_array = []
            for competency in competencies:
                elements_array.append(get_db().get_competency_elements(competency.id))
            return render_template('competencies.html', competencies=competencies, elements_array=elements_array)
        
        flash("The competencies does not exist.")
    return render_template('index.html')

@bp.route("/")
def show_all_competencies():
    competencies = get_db().get_all_competencies() # not implemented yet

    if competencies:
        return render_template('competencies.html', competencies=competencies)
    flash('No Competencies')
    return render_template('index.html')

@bp.route("/<string:comp_id>/")
def show_competency_elements(comp_id):
    competency = get_db().get_competency(comp_id)
    elements = get_db().get_competency_elements(comp_id)

    if competency:
        return render_template('competencies.html', competencies=competency, elements_array=elements)
    flash('No Competency Found')
    return redirect(url_for('show_all_competencies'))