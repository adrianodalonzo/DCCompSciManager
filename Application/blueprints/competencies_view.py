from flask import Blueprint, redirect, render_template, request, flash, url_for

from Application.objects.competency import Competency, CompetencyForm
from ..dbmanager import get_db

bp = Blueprint("competencies", __name__, url_prefix="/competencies/")

# Should prob be in courses_view
# @bp.route("/<string:course_id>/", methods=['GET', 'POST'])
# def show_course_competencies(course_id):
#     if request.method == 'GET':
#         competencies = get_db().get_course_competencies(course_id)
#         if competencies:
#             elements_array = []
#             for competency in competencies:
#                 elements_array.append(get_db().get_competency_elements(competency.id))
#             return render_template('competencies.html', competencies=competencies, elements_array=elements_array)
        
#         flash("The competencies does not exist.")
#     return render_template('index.html')

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
    competencies = []
    competencies.append(competency)
    elements = get_db().get_competency_elements(comp_id)
    elements_array = []
    elements_array.append(elements)

    if competency:
        return render_template('competencies.html', competencies=competencies, elements_array=elements_array)
    flash('No Competency Found')
    return redirect(url_for('show_all_competencies'))

@bp.route("/add/", methods=['GET', 'POST'])
def add_competency():
    form = CompetencyForm()

    if request.method == 'GET':
        return render_template('modify_competency.html', form=form)
    
    elif request.method == 'POST':
        if form.validate_on_submit():
            matchingCompetency = False

            for competency in get_db().get_all_competencies():
                if competency.id == form.id.data:
                    matchingCompetency = True
                    flash("A Competency with the same id already exists!")
            
            if not matchingCompetency:
                comp = Competency(form.id.data, form.name.data,
                                  form.achievement.data, form.type.data)
                get_db().add_competency(comp)
    
    return redirect(url_for('show_all_competencies'))

@bp.route("/edit/<string:comp_id>/", methods=['GET', 'POST'])
def edit_competency(comp_id):
    form = CompetencyForm()
    competency = get_db().get_competency(comp_id)

    if request.method == 'GET':
        return render_template('modify_competency.html', form=form, competency=competency)
    
    elif request.method == 'POST':
        if form.validate_on_submit():

            if form.name.data is None:
                comp_name = competency.name
            if form.achievement.data is None:
                comp_achieve = competency.achievement
            if form.type.data is None:
                comp_type = competency.type

            comp = Competency(comp_id, comp_name, comp_achieve, comp_type)
            # get_db().update_competency(comp)
            # ^ not implemented yet