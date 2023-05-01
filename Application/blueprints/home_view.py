from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

from ..dbmanager import get_db

bp = Blueprint('index', __name__, url_prefix='/')

@bp.route('/')
def index():
    if current_user.is_active:
        if current_user.blocked:
            flash('You Have Been Blocked by an Admin!', category='invalid')
            return redirect(url_for('profile.get_profile', email=current_user.email))
        
    return render_template('index.html')

@bp.route('/terms/')
def show_terms():
    terms = get_db().get_all_terms()
    return render_template('terms.html', terms=terms)

@bp.route("/terms/<int:term_id>/", methods=['GET', 'POST'])
def show_courses_by_term(term_id):
    courses = get_db().get_courses_by_term(term_id)

    if courses:
        return render_template('terms.html', courses=courses, term=term_id)
    
    flash("No courses by this term", category='invalid')
    return redirect(url_for('index.show_terms'))