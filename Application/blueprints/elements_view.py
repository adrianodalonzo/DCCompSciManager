from flask import Blueprint, flash, redirect, render_template, request, url_for

bp = Blueprint("elements", __name__, url_prefix="/elements/")

from Application.objects.element import Element, ElementForm
from ..dbmanager import get_db

@bp.route("/add/", methods=['GET', 'POST'])
def add_element():
    form = ElementForm()

    if request.method == 'GET':
        return render_template("modify_element.html", form=form)
    
    elif request.method == 'POST':
        if form.validate_on_submit():
            matchingElement = False

            for element in get_db().get_competency_elements(form.competency.data):
                if element.name == form.name.data:
                    matchingElement = True
                    flash("An Element with the same name already exists!")
            
            if not matchingElement:
                elem = Element(form.order.data, form.name.data,
                               form.criteria.data, form.competency.data)
                get_db().add_competency_element(elem)
    
    return redirect(url_for('show_all_competencies'))

@bp.route("/edit/<string:elem_nm>/", methods=['GET', 'POST'])
def edit_element(elem_nm):
    form = ElementForm()
    elem = get_db().get_element(elem_nm)

    if request.method == 'GET':
        return render_template('modify_element.html', form=form, element=elem)
    
    elif request.method == 'POST':
        if form.validate_on_submit():

            elem_order = form.order.data
            elem_name = form.name.data
            elem_crit = form.criteria.data
            elem_comp_id = form.competency.data

            if elem_order is None:
                elem_order = elem.order
            if elem_name is None:
                elem_name = elem.name
            if elem_crit is None:
                elem_crit = elem.criteria
            if elem_comp_id is None:
                elem_comp_id = elem.competency_id
            
            element = Element(elem_order, elem_name, elem_crit, elem_comp_id)
            get_db().modify_competency_element(element)
            
    return redirect(url_for('show_all_competencies'))

@bp.route("/delete/<string:elem_nm>")
def delete_element(elem_nm):
    element = get_db().get_element(elem_nm)
    get_db().delete_competency_element(element)
    flash("Deleted element " + elem_nm, category='valid')
    return redirect(url_for('show_all_competencies'))