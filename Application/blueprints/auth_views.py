from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app, send_from_directory
from flask_login import login_required, login_user, logout_user
import os
from werkzeug.security import check_password_hash, generate_password_hash
from ..objects.user import User, SignUpForm, LoginForm
from ..dbmanager import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth/")

@bp.route("/signup/", methods=['GET', 'POST'])
def signup():
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
            # TODO MAYBE: Add code to check for what specific aspects of the form are invalid.
            flash("Form Is Invalid!", category='invalid')
            return redirect(url_for('auth.signup'))
        
    elif request.method == 'GET':
        return render_template("signup.html", form=form)

@bp.route('/login/', methods=['GET', 'POST'])
def login():
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
                    return render_template('index.html')
                else:
                    flash('Email or Password Entered are Invalid!', category='invalid')
                    return redirect(url_for('auth.login'))
            else:
                flash("Email or Password Entered are Invalid!", category='invalid')
                return redirect(url_for('auth.login'))
        else:
            flash('Form Invalid!', category='invalid')
            return redirect(url_for('auth.login'))
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
    dir = os.path.join(current_app.config['IMAGE_PATH'], email)
    return send_from_directory(dir, 'avatar.png')