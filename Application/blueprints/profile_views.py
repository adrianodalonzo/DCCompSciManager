import os
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from ..objects.forms import EditProfileForm, ResetPasswordForm
from ..dbmanager import get_db
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('profile', __name__, url_prefix='/profile/')

@bp.route('/<email>/')
@login_required
def get_profile(email):
    if not isinstance(email, str):
        return TypeError("Email MUST be a string!")
    user = get_db().get_user(email)
    if user:
        is_my_profile = email == current_user.email
        return render_template('specific_profile.html', user=user, is_my_profile=is_my_profile)
    flash("A User With That Email Doesn't Exist!", category='invalid')
    return redirect(url_for('index.index'))

@bp.route('/<email>/edit/', methods=['GET', 'POST'])
@login_required
def edit_profile(email):
    if not isinstance(email, str):
        flash("Email Passed MUST be a string!", category='invalid')
        return redirect(url_for('index.index'))
    if get_db().get_user(email) not in get_db().get_users():
        flash("Can't Edit Profile of User which Doesn't Exist!", category='invalid')
        return redirect(url_for('index.index'))
    
    if current_user.group != 'Admin' and current_user.email != email:
        flash("You Don't Have Permissions to Edit Other User's Profiles!", category='invalid')
        return redirect(url_for('index.index'))
    
    user = get_db().get_user(email)
    form = EditProfileForm(obj=user)
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.name.data
            username_exists = False

            for user_iterator in get_db().get_users():
                username_exists = user_iterator.name == username

            if username_exists:
                flash('A User with that Username Already Exists!', category='invalid')
                return redirect(url_for('index.index'))

            file = form.avatar.data
            avatar_dir = os.path.join(current_app.config['IMAGE_PATH'], email)
            if not os.path.exists(avatar_dir):
                os.makedirs(avatar_dir)
            avatar_path = os.path.join(avatar_dir, 'avatar.png')
            if file:
                try:
                    file.save(avatar_path)
                except Exception:
                    flash('An error occurred with saving the avatar!', category='invalid')
                    return redirect(url_for('auth.signup'))

            get_db().update_user_username(email, username)
            flash('Profile Edited Successfully!', category='valid')
            return redirect(url_for('profile.get_profile', email=user.email))
        else:
            for error in form.errors:
                if error == 'avatar':
                    flash("Avatar Inputed Must Have a '.png' Extension!", category='invalid')
                else:
                    if error == 'name':
                        flash("Username Can't Contain any Spaces!", category='invalid')
                    elif len(form.errors) == 1:   
                        flash(f"{error} is Invalid!", category='invalid')
                    else:
                        errors = ""
                        errors += f"{error.capitalize()}, "
                        flash(f"{errors} are Invalid!", category='invalid')  
            return redirect(url_for('profile.get_profile', email=email))
    elif request.method == 'GET':
        return render_template('edit_profile.html', user=get_db().get_user(email), is_my_profile=True, form=form)

@bp.route('/<email>/reset-password/', methods=['GET', 'POST'])
@login_required
def reset_password(email):
    if not isinstance(email, str):
        flash("Email Passed MUST be a string!", category='invalid')
        return redirect(url_for('index.index'))
    if get_db().get_user(email) not in get_db().get_users():
        flash("Can't Reset Password of User which Doesn't Exist!", category='invalid')
        return redirect(url_for('index.index'))
    
    if current_user.group != 'Admin' and current_user.email != email:
        flash("You Don't Have Permissions to Reset Other User's Passwords!", category='invalid')
        return redirect(url_for('index.index'))

    user = get_db().get_user(email)
    form = ResetPasswordForm()
    if request.method == 'POST':
        if not form.old_password.data:
            new_password = form.new_password.data
            retyped_new_password = form.retype_new_password.data
            if new_password == retyped_new_password:
                hashed_password = generate_password_hash(new_password)
                get_db().update_user_password(user.email, hashed_password)
                flash('Password Successfully Resetted!', category='valid')
                return render_template('specific_profile.html', user=user)
            else:
                flash("The New Password and Retyped New Password Must Both Match!", category='invalid')
                return redirect(url_for('profile.reset_password', email=user.email))
        if form.validate_on_submit():
            old_password = form.old_password.data
            if check_password_hash(user.password, old_password):
                new_password = form.new_password.data
                retyped_new_password = form.retype_new_password.data
                if new_password == retyped_new_password:
                    if new_password == old_password:
                        flash("If You Want to Reset your Password, Your Old and New Passwords Must be Different!", category='message')
                        return redirect(url_for('profile.reset_password', email=user.email))
                    hashed_password = generate_password_hash(new_password)
                    get_db().update_user_password(user.email, hashed_password)
                    flash('Password Successfully Resetted!', category='valid')
                    return render_template('specific_profile.html', user=user)
                else:
                    flash("The New Password and Retyped New Password Must Both Match!", category='invalid')
                    return redirect(url_for('profile.reset_password', email=user.email))
            else:
                flash("The Password You Entered Doesn't Match Your Old Password!", category='invalid')
                return redirect(url_for('profile.reset_password', email=user.email))
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
            return redirect(url_for('profile.get_profile', email=email))
    elif request.method == 'GET':
        is_my_profile = email == current_user.email
        return render_template('reset_password.html', form=form, is_my_profile=is_my_profile)