import os
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_required
from werkzeug.security import generate_password_hash

from ..objects.user import SignUpForm, User

from ..dbmanager import get_db

bp = Blueprint('members', __name__, url_prefix='/members/')

@bp.route('/', methods=['GET', 'POST'])
@login_required
def list_members():
    members = get_db().get_members()
    add_form = SignUpForm()
    # will need lots a verification for this
    if request.method == 'POST':
        if add_form.validate_on_submit():
            
            file = add_form.avatar.data
            avatar_dir = os.path.join(current_app.config['IMAGE_PATH'], add_form.email.data)
            if not os.path.exists(avatar_dir):
                os.makedirs(avatar_dir)
            avatar_path = os.path.join(avatar_dir, 'avatar.png')
            try:
                file.save(avatar_path)
            except Exception:
                flash('An error occurred with saving the avatar!', category='invalid')
                return redirect(url_for('members.list_members'))
            
            hash = generate_password_hash(add_form.password.data)
            user = User(add_form.email.data, add_form.name.data, hash)

            test_user = get_db().get_user(user.email)
            if test_user:
                flash('A Member With That Email Already Exists!', category='invalid')
                return redirect(url_for('members.list_members'))
            else:
                get_db().insert_user(user)
                flash("Member Added Successfully", category='valid')
                members = get_db().get_members()
                return render_template("members.html", add_form=add_form, members=members)
        else:
            for error in add_form.errors:
                if error == 'avatar':
                    flash("Avatar Inputed Must Have a '.png' Extension!", category='invalid')
                else:
                    if len(add_form.errors) == 1:
                        flash(f"{error} is Invalid!", category='invalid')
                    else:
                        errors = ""
                        errors += f"{error.capitalize()}, "
                        flash(f"{errors} are Invalid!", category='invalid')
            return redirect(url_for('members.list_members'))
        
    elif request.method == 'GET':
        return render_template("members.html", add_form=add_form, members=members)