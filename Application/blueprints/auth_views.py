from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app, send_from_directory
from flask_login import current_user, login_required, login_user, logout_user
import os
from werkzeug.security import check_password_hash, generate_password_hash
from ..objects.user import User
from ..objects.forms import SignUpForm, LoginForm
from ..dbmanager import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth/")

@bp.route("/signup/", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        flash('You Already Have an Account Here!', category='message')
        return redirect(url_for('profile.get_profile', email=current_user.email))
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
                return redirect(url_for('auth.signup'))
            
            hash = generate_password_hash(form.password.data)
            user = User(form.email.data, form.name.data, hash)

            test_user = get_db().get_user(user.email)
            if test_user:
                flash('A User With That Email Already Exists!', category='invalid')
                return redirect(url_for('auth.signup'))
            else:
                get_db().insert_user(user)
                flash("User Added Successfully", category='valid')
            return render_template("index.html") 
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
            return redirect(url_for('auth.signup'))
        
    elif request.method == 'GET':
        return render_template("signup.html", form=form)

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You Are Already Logged In!', category='message')
        return redirect(url_for('profile.get_profile', email=current_user.email))
    form = LoginForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            user = get_db().get_user(email)
            if user:
                password = form.password.data
                if check_password_hash(user.password, password):
                    login_user(user, remember=form.remember_me.data)
                    flash('Login Successful!', category='valid')
                    return redirect(url_for('index.index'))
                else:
                    flash('Email or Password Entered are Invalid!', category='invalid')
                    return redirect(url_for('auth.login'))
            else:
                flash("Email or Password Entered are Invalid!", category='invalid')
                return redirect(url_for('auth.login'))
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
            return redirect(url_for('index.index'))
    elif request.method == 'GET':
        return render_template('login.html', form=form)
    
@bp.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('Successfully Logged Out!', category='valid')
    return redirect(url_for('index.index'))

@bp.route('/avatar/<email>/avatar.png/')
@login_required
def get_avatar(email):
    if current_user.blocked and current_user.email != email:
        flash("You Have Been Blocked by an Admin, so Viewing this Page is Not Allowed!", category='invalid')
        return redirect(url_for('profile.get_profile', email=current_user.email))
    dir = os.path.join(current_app.config['IMAGE_PATH'], email)
    return send_from_directory(dir, 'avatar.png')