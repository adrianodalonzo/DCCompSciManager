from flask import Blueprint, render_template, request
from werkzeug.security import check_password_hash, generate_password_hash
from objects.user import User, UserForm

bp = Blueprint("signup", __name__, url_prefix="/signup/")

@bp.route("/", methods=['GET', 'POST'])
def signup():
    form = UserForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            hash = generate_password_hash(form.password.data)
            user = User(form.email.data, form.name.data, hash, form.avatarlink.data)
            # get_db().insert_user(user)
            # flash("User Added")
    
    return render_template("signup.html", form=form)