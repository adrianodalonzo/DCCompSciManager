from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

bp = Blueprint('user_admins', __name__, url_prefix='/user_admins/')

@bp.route('/')
@login_required
def list_user_admins():
    if current_user.group != 'Admin':
        flash("You Don't Have Permissions to View this Page!", category='invalid')
        return redirect(url_for('index.index'))
    return render_template('user_admins.html')