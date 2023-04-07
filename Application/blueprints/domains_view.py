from flask import Blueprint, render_template, request, flash
from ..dbmanager import get_db

bp = Blueprint("domains", __name__, url_prefix="/domains/")

@bp.route("/", methods=['GET', 'POST'])
def show_domains():
    domains = get_db().get_all_domains()
    if domains :
        return render_template('domains.html', domains=domains)
    
    flash("No domains")
    return render_template('index.html')

@bp.route("/<int:domain_id>", methods=['GET'])
def show_domain(domain_id):
    domain = get_db().get_domain(domain_id)
    if domain:
        return render_template('domains.html', domain=domain)
    flash("No domain with this id")
    return render_template('index.html')
