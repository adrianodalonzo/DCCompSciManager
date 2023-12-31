from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

bp = Blueprint("elements", __name__, url_prefix="/elements/")

from ..objects.element import Element
from ..dbmanager import get_db

from ..objects.forms import ElementForm

@bp.route("/add/", methods=['GET', 'POST'])
@login_required
def add_element():
    if current_user.is_active:
        if current_user.blocked:
            flash('You Have Been Blocked by an Admin!', category='invalid')
            return redirect(url_for('profile.get_profile', email=current_user.email))
    
    form = ElementForm()
    form.competency_id.choices=get_db().get_comepetency_choices()

    if request.method == 'GET':
        return render_template("modify_element.html", form=form)
    
    elif request.method == 'POST':
        if form.validate_on_submit():
            matchingElement = False

            for element in get_db().get_competency_elements(form.competency_id.data):
                if element.name == form.name.data:
                    matchingElement = True
                    flash("An Element with the same name already exists!", category="invalid")
            
            if not matchingElement:
                elem = Element(form.order.data, form.name.data,
                               form.criteria.data, form.competency_id.data)
                try:
                    get_db().add_competency_element(elem)
                    flash("Added Element: " + elem.name, category='valid')
                except Exception:
                    flash('Error adding element', category='invalid')
    
    return redirect(url_for('competencies.show_competency_elements', comp_id=form.competency_id.data))

@bp.route("/edit/<int:elem_id>/", methods=['GET', 'POST'])
@login_required
def edit_element(elem_id):
    if current_user.is_active:
        if current_user.blocked:
            flash('You Have Been Blocked by an Admin!', category='invalid')
            return redirect(url_for('profile.get_profile', email=current_user.email))
    elem = get_db().get_element(elem_id)
    form = ElementForm(obj=elem)
    competency = get_db().get_competency(elem.competency_id)
    competency_choice = [(competency.id, competency.name)]
    form.competency_id.choices=(competency_choice)

    if request.method == 'GET':
        return render_template('modify_element.html', form=form, element=elem)
    
    elif request.method == 'POST':
        if form.validate_on_submit():

            if form.name.data.isnumeric() or form.criteria.data.isnumeric() or form.competency_id.data.isnumeric():
                flash("Unsuccesfully Edited Element", category='invalid')
                return redirect(url_for('competencies.show_competency_elements', comp_id=elem.competency_id))

            elem_order = form.order.data
            elem_name = form.name.data
            elem_crit = form.criteria.data
            elem_comp_id = form.competency_id.data

            if elem_order is None:
                elem_order = elem.order
            if elem_name is None:
                elem_name = elem.name
            if elem_crit is None:
                elem_crit = elem.criteria
            if elem_comp_id is None:
                elem_comp_id = elem.competency_id
            
            element = Element(elem_order, elem_name, elem_crit, elem_comp_id)
            element.id = elem.id
            try:
                get_db().modify_competency_element(element)
                flash("Edited Element: " + elem_name, category='valid')
            except Exception:
                flash('Error editing element', category='invalid')
            
    return redirect(url_for('competencies.show_competency_elements', comp_id=form.competency_id.data))

@bp.route("/delete/<int:elem_id>")
@login_required
def delete_element(elem_id):
    if current_user.is_active:
        if current_user.blocked:
            flash('You Have Been Blocked by an Admin!', category='invalid')
            return redirect(url_for('profile.get_profile', email=current_user.email))
    element = get_db().get_element(elem_id)
    get_db().delete_competency_element(element)
    flash("Deleted element " + str(elem_id), category='valid')
    return redirect(url_for('competencies.show_competency_elements', comp_id=element.competency_id))