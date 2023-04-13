from flask import Blueprint, render_template
from flask_login import login_required
from ..dbmanager import get_db

bp = Blueprint('profile', __name__, url_prefix='/profile/')

@bp.route('/<email>/')
@login_required
def get_profile(email):
    if not isinstance(email, str):
        raise Exception('Email MUST be a string!')
    return render_template('profile.html')

@bp.route('/reset-password/')
@login_required
def reset_password():
    return render_template('reset_password.html')