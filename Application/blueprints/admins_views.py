import os
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash

from ..dbmanager import get_db
from ..objects.user import DeleteAdminForm, MoveAdminForm, SignUpForm, User

bp = Blueprint('admins', __name__, url_prefix='/admins/')

@bp.route('/')
@login_required
def list_admins():
    if current_user.group != 'Admin':
        flash("You Don't Have the Permissions to View this Page!", category='invalid')
        return redirect(url_for('index.index'))
    admins = get_db().get_admins()
    return render_template('admins.html', admins=admins)

@bp.route('/add/', methods=['GET', 'POST'])
@login_required
def add_admin():
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
                return redirect(url_for('admins.list_admins'))
            
            hash = generate_password_hash(form.password.data)
            user = User(form.email.data, form.name.data, hash)

            test_user = get_db().get_user(user.email)
            if test_user:
                flash('A User With That Email Already Exists!', category='invalid')
                return redirect(url_for('admins.list_admins'))
            else:
                get_db().insert_user(user, 'Admin')
                flash("Admin Added Successfully", category='valid')
                admins = get_db().get_admins()
                return render_template("admins.html", form=form, admins=admins)
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
            return redirect(url_for('admins.list_admins'))
        
    elif request.method == 'GET':
        return render_template("add_user.html", form=form, user_type='Admin')
    
@bp.route('/move/', methods=['GET', 'POST'])
@login_required
def move_admin():
    if not get_db().get_admins():
        flash('There Are No Admins to Move!', category='message')
        return redirect(url_for('admins.list_admins'))
    form = MoveAdminForm()
    form.admins.choices = [admin.email for admin in get_db().get_admins()]
    form.groups.choices = ['Member', 'User Admin']

    if request.method == 'POST' and form.validate_on_submit():
        admin = get_db().get_user(form.admins.data)
        if admin:
            get_db().move_member(admin.email, form.groups.data)
            flash(f'Admin Successfully Moved to {form.groups.data} Group!', category='valid')
            admins = get_db().get_admins()
            form.admins.choices = [admin.email for admin in admins]
            return render_template('admins.html', form=form, admins=admins)
    elif request.method == 'GET':
        return render_template('move_admin.html', form=form)
    
@bp.route('/delete/', methods=['GET', 'POST'])
@login_required
def delete_admin():
    if not get_db().get_admins():
        flash('There Are No Admins to Delete!', category='message')
        return redirect(url_for('admins.list_admins'))
    form = DeleteAdminForm()
    # assigns select options by looping through the members and adding the emails to the select
    form.admins.choices = [admin.email for admin in get_db().get_admins()]

    if request.method == 'POST' and form.validate_on_submit():
        admin = get_db().get_user(form.admins.data)
        if admin:
            get_db().delete_user(admin.email)
            flash('Admin Successfully Deleted!', category='valid')
            admins = get_db().get_admins()
            return render_template('admins.html', admins=admins)
    elif request.method == 'GET':
        admins = get_db().get_members()
        return render_template('delete_admin.html', form=form)

