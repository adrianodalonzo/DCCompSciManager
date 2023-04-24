from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import current_user, login_required
from ..dbmanager import get_db

bp = Blueprint("domains", __name__, url_prefix="/domains/")

@bp.route("/", methods=['GET', 'POST'])
@login_required
def show_domains():
    if current_user.blocked:
        flash('You Have Been Blocked by an Admin!', category='invalid')
        return redirect(url_for('profile.get_profile', email=current_user.email))
    domains = get_db().get_all_domains()
    if domains :
        return render_template('domains.html', domains=domains)
    
    flash("No domains", category='invalid')
    return render_template('index.html')

@bp.route("/<int:domain_id>", methods=['GET'])
@login_required
def show_domain(domain_id):
    domain = get_db().get_domain(domain_id)
    if domain:
        return render_template('domains.html', domain=domain)
    flash("No domain with this id", category='invalid')
    return render_template('index.html')
