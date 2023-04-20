import os
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash

from ..dbmanager import get_db
from ..objects.user import DeleteUserAdminForm, MoveUserAdminForm, SignUpForm, User

bp = Blueprint('user_admins', __name__, url_prefix='/user_admins/')

@bp.route('/')
@login_required
def list_user_admins():
    if current_user.group != 'Admin':
        flash("You Don't Have Permissions to View this Page!", category='invalid')
        return redirect(url_for('index.index'))
    user_admins = get_db().get_user_admins()
    return render_template('user_admins.html', user_admins=user_admins)

@bp.route('/add/', methods=['GET', 'POST'])
@login_required
def add_user_admin():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            
            file = form.avatar.data
            avatar_dir = os.path.join(current_app.config['IMAGE_PATH'], form.email.data)
            if not os.path.exists(avatar_dir):
                os.makedirs(avatar_dir)
            avatar_path = os.path.join(avatar_dir, 'avatar.png')
            try:
                file.save(avatar_path)
            except Exception:
                flash('An error occurred with saving the avatar!', category='invalid')
                return redirect(url_for('user_admins.list_user_admins'))
            
            hash = generate_password_hash(form.password.data)
            user = User(form.email.data, form.name.data, hash)

            test_user = get_db().get_user(user.email)
            if test_user:
                flash('A User With That Email Already Exists!', category='invalid')
                return redirect(url_for('user_admins.list_user_admins'))
            else:
                get_db().insert_user(user, 'User Admin')
                flash("User Admin Added Successfully", category='valid')
                user_admins = get_db().get_user_admins()
                return render_template("user_admins.html", form=form, user_admins=user_admins)
        else:
            for error in form.errors:
                if error == 'avatar':
                    flash("Avatar Inputed Must Have a '.png' Extension!", category='invalid')
                else:
                    if len(form.errors) == 1:
                        flash(f"{error} is Invalid!", category='invalid')
                    else:
                        errors = ""
                        errors += f"{error.capitalize()}, "
                        flash(f"{errors} are Invalid!", category='invalid')
            return redirect(url_for('user_admins.list_user_admins'))
        
    elif request.method == 'GET':
        return render_template("add_user.html", form=form, user_type='User Admin')
    
@bp.route('/move/', methods=['GET', 'POST'])
@login_required
def move_user_admin():
    if not get_db().get_user_admins():
        flash('There Are No User Admins to Move!', category='message')
        return redirect(url_for('user_admins.list_user_admins'))
    form = MoveUserAdminForm()
    form.user_admins.choices = [user_admin.email for user_admin in get_db().get_user_admins()]
    form.groups.choices = ['Member', 'Admin']

    if request.method == 'POST' and form.validate_on_submit():
        user_admin = get_db().get_user(form.user_admins.data)
        if user_admin:
            get_db().move_member(user_admin.email, form.groups.data)
            flash(f'User Admin Successfully Moved to {form.groups.data} Group!', category='valid')
            user_admins = get_db().get_user_admins()
            form.user_admins.choices = [user_admin.email for user_admin in user_admins]
            return render_template('user_admins.html', form=form, user_admins=user_admins)
    elif request.method == 'GET':
        return render_template('move_user_admin.html', form=form)
    
@bp.route('/delete/', methods=['GET', 'POST'])
@login_required
def delete_user_admin():
    if not get_db().get_user_admins():
        flash('There Are No User Admins to Delete!', category='message')
        return redirect(url_for('user_admins.list_user_admins'))
    form = DeleteUserAdminForm()
    # assigns select options by looping through the members and adding the emails to the select
    form.user_admins.choices = [user_admin.email for user_admin in get_db().get_user_admins()]

    if request.method == 'POST' and form.validate_on_submit():
        user_admin = get_db().get_user(form.user_admins.data)
        if user_admin:
            get_db().delete_user(user_admin.email)
            flash('User Admin Successfully Deleted!', category='valid')
            user_admins = get_db().get_user_admins()
            return render_template('user_admins.html', user_admins=user_admins)
    elif request.method == 'GET':
        return render_template('delete_user_admin.html', form=form)