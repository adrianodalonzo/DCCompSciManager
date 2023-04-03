from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from objects.user import User, SignUpForm, LoginForm
from ..dbmanager import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth/")

@bp.route("/signup/", methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            hash = generate_password_hash(form.password.data)
            user = User(form.email.data, form.name.data, hash, form.avatarlink.data)
            # get_db().insert_user(user)
            # flash("User Added")
    
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
                else:
                    flash('Invalid Password!', category='invalid')
                    return redirect(url_for('auth.login'))
            else:
                flash("Couldn't Find User!", category='invalid')
                return redirect(url_for('auth.login'))
        else:
            flash('Invalid Form!', category='invalid')
            return redirect(url_for('auth.login'))
    elif request.method == 'GET':
        return render_template('login.html', form=form)
    
@bp.route('/logout/')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')