from flask import Blueprint, render_template
from flask_login import login_required

from ..objects.user import SignUpForm

from ..dbmanager import get_db

bp = Blueprint('members', __name__, url_prefix='/members/')

@bp.route('/')
@login_required
def list_members():
    members = get_db().get_members()
    add_form = SignUpForm()
    return render_template('members.html', members=members, add_form=add_form)