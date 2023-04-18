from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from ..objects.user import ResetPasswordForm
from ..dbmanager import get_db
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('profile', __name__, url_prefix='/profile/')

@bp.route('/')
@login_required
def profile():
    return render_template('profile.html')

@bp.route('/<email>/')
@login_required
def get_profile(email):
    if not isinstance(email, str):
        return TypeError("Email MUST be a string!")
    if current_user.email == email:
        return redirect(url_for('profile.profile'))
    user = get_db().get_user(email)
    if user:
        return render_template('specific_profile.html', user=user)
    flash("A User With That Email Doesn't Exist!", category='invalid')
    return redirect(url_for('index.index'))

@bp.route('/reset-password/', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            old_password = form.old_password.data
            if check_password_hash(current_user.password, old_password):
                new_password = form.new_password.data
                retyped_new_password = form.retype_new_password.data
                if new_password == retyped_new_password:
                    if new_password == old_password:
                        flash("If You Want to Reset your Password, Your Old and New Passwords Must be Different!", category='message')
                        return redirect(url_for('profile.reset_password'))
                    hashed_password = generate_password_hash(new_password)
                    get_db().update_user_password(current_user.email, hashed_password)
                    flash('Password Successfully Resetted!', category='valid')
                    return render_template('profile.html')
                else:
                    flash("The New Password and Retyped New Password Must Both Match!", category='invalid')
                    return redirect(url_for('profile.reset_password'))
            else:
                flash("The Password You Entered Doesn't Match Your Old Password!", category='invalid')
                return redirect(url_for('profile.reset_password'))
        else:
            flash('Form Is Invalid!', category='invalid')
    elif request.method == 'GET':
        return render_template('reset_password.html', form=form)