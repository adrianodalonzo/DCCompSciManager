from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

from ..dbmanager import get_db

bp = Blueprint('index', __name__, url_prefix='/')

@bp.route('/')
def index():
    try:
        if current_user.blocked:
            flash('You Have Been Blocked by an Admin!', category='invalid')
            return redirect(url_for('profile.get_profile', email=current_user.email))
        return render_template('index.html')
    except Exception:
        return render_template('index.html')

@bp.route('/terms/')
def show_terms():
    terms = get_db().get_all_terms()
    return render_template('terms.html', terms=terms)