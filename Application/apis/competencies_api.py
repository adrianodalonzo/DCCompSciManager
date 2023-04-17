from flask import Blueprint, jsonify, request, flash
from ..dbmanager import get_db
from objects.competency import Competency
bp = Blueprint('competencies_api', __name__, url_prefix='/api/competencies')

@bp.route('/', methods=['GET', 'POST'])
def competencies_api():
    try:
        if request.method == 'POST':
            competencies_json = request.json
            if competencies_json:
                competency = Competency.from_json(competencies_json)
                get_db().add_competency(competency)
        elif request.method == 'GET':
            if request.args:
                id = request.args.get("id")
                competencies = get_db().get_competencies()
                competency = [competency for competency in competencies if competency.id == id]
                return jsonify(competency[0].__dict__)
        competencies = get_db().get_competencies()
        json = [competency.__dict__ for competency in competencies]
        return jsonify(json)
    except Exception:
        return ""