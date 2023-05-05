from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import current_user, login_required
from werkzeug.datastructures import MultiDict

from ..objects.competency import Competency
from ..objects.forms import CompetencyForm
from ..dbmanager import get_db

bp = Blueprint("competencies", __name__, url_prefix="/competencies/")

@bp.route("/")
def show_all_competencies():
    if current_user.is_active:
        if current_user.blocked:
            flash('You Have Been Blocked by an Admin!', category='invalid')
            return redirect(url_for('profile.get_profile', email=current_user.email))
    competencies, prev_page, next_page = get_db().get_all_competencies(page_size=500)

    if competencies:
        return render_template('competencies.html', competencies=competencies)
    flash('No Competencies', category='invalid')
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
            competencies, prev_page, next_page = get_db().get_all_competencies(page_size=500)

            for competency in competencies:
                if competency.id == form.id.data:
                    matchingCompetency = True
                    flash("A Competency with the same id already exists!", category='invalid')
            
            if not matchingCompetency:
                comp = Competency(form.id.data, form.name.data,
                                  form.achievement.data, form.type.data)
                try:
                    get_db().add_competency(comp)
                    flash("Added Competency: " + comp.name, category='valid')
                except Exception:
                    flash("Error adding competency", cateogry='invalid')
    
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

            if form.name.data.isnumeric() or form.achivement.data.isnumeric() or form.type.data.isnumeric():
                flash("Unsuccesfully Edited Competency", category='invalid')
                return redirect(url_for('competencies.show_all_competencies'))
            
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
            try:
                get_db().modify_competency(comp)
                flash("Edited Competency: " + comp_name, category='valid')
            except Exception:
                flash("Error editing competency", category='invalid')

    return redirect(url_for('competencies.show_all_competencies'))

@bp.route("/delete/<string:comp_id>/")
@login_required
def delete_competency(comp_id):
    try:
        get_db().delete_competency(comp_id)
        flash('Competency ' + comp_id + ' has been deleted, along with its elements', category='valid')
    except Exception:
        flash('Error deleting competency', category='invalid')
    return redirect(url_for('competencies.show_all_competencies'))