from flask import Blueprint, render_template, request

bp = Blueprint("competencies", __name__, url_prefix="/competencies/")

@bp.route("/", methods=['GET', 'POST'])
def show_competencies():
    return render_template('competencies.html')