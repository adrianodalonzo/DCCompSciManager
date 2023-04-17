import os
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash

from ..objects.user import BlockMemberForm, DeleteMemberForm, SignUpForm, User

from ..dbmanager import get_db

bp = Blueprint('members', __name__, url_prefix='/members/')

@bp.route('/')
@login_required
def list_members():
    if current_user.blocked:
        flash('You Have Been Blocked by the User Admin, so Viewing This Page is Unavailable!', category='invalid')
        return redirect(url_for('profile.get_profile', email=current_user.email))
    members = get_db().get_members()
    return render_template('members.html', members=members)
    
@bp.route('/add/', methods=['GET', 'POST'])
@login_required
def add_member():
    if current_user.group == 'Member':
        flash("You Don't Have the Permissions to View This Page", category='invalid')
        return redirect(url_for('members.list_members'))
    members = get_db().get_members()
    form = SignUpForm()
    # will need lots a verification for this
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
                return redirect(url_for('members.list_members'))
            
            hash = generate_password_hash(form.password.data)
            user = User(form.email.data, form.name.data, hash)

            test_user = get_db().get_user(user.email)
            if test_user:
                flash('A Member With That Email Already Exists!', category='invalid')
                return redirect(url_for('members.list_members'))
            else:
                get_db().insert_user(user)
                flash("Member Added Successfully", category='valid')
                members = get_db().get_members()
                return render_template("members.html", form=form, members=members)
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
            return redirect(url_for('members.list_members'))
        
    elif request.method == 'GET':
        return render_template("add_member.html", form=form, members=members)
    
@bp.route('/delete/', methods=['GET', 'POST'])
@login_required
def delete_member():
    if current_user.group == 'Member':
        flash("You Don't Have the Permissions to View This Page", category='invalid')
        return redirect(url_for('members.list_members'))
    form = DeleteMemberForm()
    # assigns select options by looping through the members and adding the emails to the select
    form.members.choices = [member.email for member in get_db().get_members()]

    if request.method == 'POST' and form.validate_on_submit():
        member = get_db().get_user(form.members.data)
        if member:
            get_db().delete_member(member.email)
            flash('Member Successfully Deleted!', category='valid')
            members = get_db().get_members()
            return render_template('members.html', members=members)
    elif request.method == 'GET':
        members = get_db().get_members()
        return render_template('delete_member.html', members=members, form=form)
    
@bp.route('/block/', methods=['GET', 'POST'])
@login_required
def block_member():
    if current_user.group == 'Member':
        flash("You Don't Have the Permissions to View This Page", category='invalid')
        return redirect(url_for('members.list_members'))
    form = BlockMemberForm()
    # assigns select options by looping through the members and adding the emails to the select
    form.members.choices = [member.email for member in get_db().get_unblocked_members()]

    if request.method == 'POST' and form.validate_on_submit():
        member = get_db().get_user(form.members.data)
        if member:
            get_db().block_member(member.email)
            flash('Member Successfully Blocked!', category='valid')
            members = get_db().get_unblocked_members()
            form.members.choices = [member.email for member in get_db().get_unblocked_members()]
            return render_template('block_member.html', members=members, form=form)
    elif request.method == 'GET':
        members = get_db().get_members()
        return render_template('block_member.html', members=members, form=form)
