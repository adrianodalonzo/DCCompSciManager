from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import current_user, login_required

from ..objects.domain import Domain
from ..dbmanager import get_db

from ..objects.forms import DomainForm

bp = Blueprint("domains", __name__, url_prefix="/domains/")

@bp.route("/", methods=['GET', 'POST'])
def show_domains():
    if current_user.is_active:
        if current_user.blocked:
            flash('You Have Been Blocked by an Admin!', category='invalid')
            return redirect(url_for('profile.get_profile', email=current_user.email))
        
    domains, prev_page, next_page = get_db().get_all_domains(page_size=100)
    if domains:
        return render_template('domains.html', domains=domains)
    
    flash("No domains", category='invalid')
    return render_template('index.html')

@bp.route("/<int:domain_id>/", methods=['GET'])
def show_domain(domain_id):
    domain = get_db().get_domain(domain_id)
    courses = get_db().get_courses_by_domain(domain_id)

    if domain:
        return render_template('domains.html', domain=domain, courses=courses)
    
    flash("No domain with this id", category='invalid')
    return redirect(url_for('domains.show_domains'))

@bp.route('/add/', methods=['GET', 'POST'])
@login_required
def add_domain():
    form = DomainForm()
    
    if request.method == 'GET':
        return render_template('modify_domain.html', form=form)
    
    elif request.method == 'POST':
        if form.validate_on_submit():
            matchingDomain = False
            domains, prev_page, next_page = get_db().get_all_domains(page_size=100)

            for domain in domains:
                if domain.name == form.name.data:
                    matchingDomain = True
                    flash("A Domain with the same name already exists")

            if not matchingDomain:
                dom = Domain(form.name.data, form.description.data)
                try:
                    get_db().add_domain(dom)
                    flash("Added Domain: " + dom.name, category='valid')
                except Exception:
                    flash('Error adding domain', category='invalid')

    return redirect(url_for('domains.show_domains'))

@bp.route("/edit/<int:dom_id>/", methods=['GET', 'POST'])
@login_required
def edit_domain(dom_id):
    dom = get_db().get_domain(dom_id)
    form = DomainForm(obj=dom)

    if request.method == 'GET':
        return render_template('modify_domain.html', form=form, domain=dom)
    
    elif request.method == 'POST':
        if form.validate_on_submit():

            if form.name.data.isnumeric() or form.description.data.isnumeric():
                flash("Unsuccesfully Edited Domain", category='invalid')
                return redirect(url_for('domains.show_domains'))
            
            dom_name = form.name.data
            dom_desc = form.description.data

            if form.name.data is None:
                dom_name = dom.name
            if form.description.data is None:
                dom_desc = dom.description
            
            domain = Domain(dom_name, dom_desc)
            domain.id = dom.id
            try:
                get_db().modify_domain(domain)
                flash("Edited Domain: " + domain.name, category='valid')
            except Exception:
                flash('Error editing domain', category='invalid')
        
        else:
            flash("Domain form is not valid!", category='invalid')
    
    return redirect(url_for('domains.show_domains'))

@bp.route('/delete/<int:dom_id>')
@login_required
def delete_domain(dom_id):
    try:
        get_db().delete_domain(int(dom_id))
        flash(f"Domain {dom_id} has been deleted along with its courses", category='valid')
    except Exception:
        flash('Error deleting domain', category='invalid')
    return redirect(url_for('domains.show_domains'))