from flask import Blueprint, render_template

from Application.dbmanager import get_db

bp = Blueprint('index', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/domains/')
def show_domains():
    domains = get_db().get_all_domains()
    return render_template('domains.html', domains=domains)

@bp.route('/terms/')
def show_terms():
    terms = get_db().get_all_terms()
    return render_template('terms.html', terms=terms)