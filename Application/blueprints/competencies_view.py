from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import current_user, login_required
from werkzeug.datastructures import MultiDict

from ..objects.competency import Competency
from ..objects.forms import CompetencyForm
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
@login_required
def show_all_competencies():
    if current_user.blocked:
        flash('You Have Been Blocked by an Admin!', category='invalid')
        return redirect(url_for('profile.get_profile', email=current_user.email))
    competencies = get_db().get_all_competencies()

    if competencies:
        return render_template('competencies.html', competencies=competencies)
    flash('No Competencies', category='invalid')
    return render_template('index.html')

@bp.route("/<string:comp_id>/")
@login_required
def show_competency_elements(comp_id):
    competency = get_db().get_competency(comp_id)
    competencies = []
    competencies.append(competency)
    elements = get_db().get_competency_elements(comp_id)
    elements_array = []
    elements_array.append(elements)

    if competency:
        return render_template('competencies.html', competencies=competencies, elements_array=elements_array)
    flash('No Competency Found', category='invalid')
    return redirect(url_for('competencies.show_all_competencies'))

@bp.route("/add/", methods=['GET', 'POST'])
@login_required
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
                    flash("A Competency with the same id already exists!", category='invalid')
            
            if not matchingCompetency:
                comp = Competency(form.id.data, form.name.data,
                                  form.achievement.data, form.type.data)
                get_db().add_competency(comp)
                flash("Added Competency: " + comp.name, category='valid')
    
    return redirect(url_for('elements.add_element'))

@bp.route("/edit/<string:comp_id>/", methods=['GET', 'POST'])
@login_required
def edit_competency(comp_id):
    competency = get_db().get_competency(comp_id)
    form = CompetencyForm(obj=competency)

    if request.method == 'GET':
        return render_template('modify_competency.html', form=form, competency=competency)
    
    elif request.method == 'POST':
        if form.validate_on_submit():

            comp_name = form.name.data
            comp_achieve = form.achievement.data
            comp_type = form.type.data

            if form.name.data is None:
                comp_name = competency.name
            if form.achievement.data is None:
                comp_achieve = competency.achievement
            if form.type.data is None:
                comp_type = competency.type

            comp = Competency(comp_id, comp_name, comp_achieve, comp_type)
            get_db().modify_competency(comp)
            flash("Edited Competency: " + comp_name, category='valid')

    return redirect(url_for('competencies.show_all_competencies'))

@bp.route("/delete/<string:comp_id>/")
@login_required
def delete_competency(comp_id):
    get_db().delete_competency(comp_id)
    flash('Competency ' + comp_id + ' has been deleted, along with its elements', category='valid')
    return redirect(url_for('competencies.show_all_competencies'))