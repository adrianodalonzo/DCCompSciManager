from flask import Blueprint, jsonify, request, flash
from ..dbmanager import get_db
from objects.competency import Competency
bp = Blueprint('competencies_api', __name__, url_prefix='/api/competencies')

@bp.route('/', methods=['GET', 'POST'])
def competencies_api():
    return