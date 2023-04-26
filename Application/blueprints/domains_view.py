from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import current_user, login_required

from Application.objects.domain import Domain, DomainForm
from ..dbmanager import get_db

bp = Blueprint("domains", __name__, url_prefix="/domains/")

@bp.route("/", methods=['GET', 'POST'])
def show_domains():
    if current_user.blocked:
        flash('You Have Been Blocked by an Admin!', category='invalid')
        return redirect(url_for('profile.get_profile', email=current_user.email))
    domains = get_db().get_all_domains()
    if domains :
        return render_template('domains.html', domains=domains)
    
    flash("No domains", category='invalid')
    return render_template('index.html')

@bp.route("/<int:domain_id>/", methods=['GET'])
def show_domain(domain_id):
    domain = get_db().get_domain(domain_id)
    if domain:
        return render_template('domains.html', domain=domain)
    flash("No domain with this id", category='invalid')
    return render_template('index.html')

@bp.route('/add/', methods=['GET', 'POST'])
@login_required
def add_domain():
    form = DomainForm()
    
    if request.method == 'GET':
        return render_template('modify_domain.html', form=form)
    
    elif request.method == 'POST':
        if form.validate_on_submit():
            matchingDomain = False

            for domain in get_db().get_all_domains():
                if domain.name == form.name.data:
                    matchingDomain = True
                    flash("A Domain with the same name already exists")

            if not matchingDomain:
                dom = Domain(form.name.data, form.description.data)
                get_db().add_domain(dom)
                flash("Added Domain: " + dom.name, category='valid')

    return redirect(url_for('domains.show_domains'))

@bp.route("/edit/<int:dom_id>/")
@login_required
def edit_domain(dom_id):
    dom = get_db().get_domain(dom_id)
    form = DomainForm(obj=dom)

    if request.method == 'GET':
        return render_template('modify_domain.html', form=form, domain=dom)
    
    elif request.method == 'POST':
        if form.validate_on_submit():
            dom_name = form.name.data
            dom_desc = form.description.data

            if form.name.data is None:
                dom_name = dom.name
            if form.description.data is None:
                dom_desc = dom.description
            
            domain = Domain(dom_name, dom_desc)
            domain.id = dom.id
            get_db().modify_domain(domain)
            flash("Edited Domain: " + domain.name, category='valid')
        
        else:
            flash("Domain form is not valid!", category='invalid')
    
    return redirect(url_for('domains.show_domains'))

@bp.route('/delete/<int:dom_id>')
@login_required
def delete_domain(dom_id):
    get_db().delete_domain(dom_id)
    flash("Domain " + dom_id + " has been deleted along with its courses")
    return redirect(url_for('domains.show_domains'))