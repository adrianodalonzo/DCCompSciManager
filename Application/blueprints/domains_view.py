from flask import Blueprint, render_template, request

bp = Blueprint("domains", __name__, url_prefix="/domains/")

@bp.route("/", methods=['GET', 'POST'])
def show_domains():
    return render_template('domains.html')