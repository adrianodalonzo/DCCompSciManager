from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

bp = Blueprint('index', __name__, url_prefix='/')

@bp.route('/')
def index():
    if current_user.blocked:
        flash('You Have Been Blocked by the User Admin, so Viewing This Page is Unavailable!', category='invalid')
        return redirect(url_for('profile.get_profile', email=current_user.email))
    return render_template('index.html')