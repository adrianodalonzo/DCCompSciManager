from flask import Blueprint, render_template
from flask_login import login_required

from ..dbmanager import get_db

bp = Blueprint('members', __name__, url_prefix='/members/')

@bp.route('/')
@login_required
def list_members():
    members = get_db().get_members()
    return render_template('members.html', members=members)