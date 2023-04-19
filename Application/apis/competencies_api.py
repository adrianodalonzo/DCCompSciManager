from flask import Blueprint, jsonify, request, flash
from ..dbmanager import get_db
from Application.objects.competency import Competency
from Application.objects.element import Element
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
                competencies = get_db().get_all_competencies()
                competency = [competency for competency in competencies if competency.id == id]
                return jsonify(competency[0].__dict__)
        competencies = get_db().get_all_competencies()
        json = [competency.__dict__ for competency in competencies]
        return jsonify(json)
    except Exception:
        return ""
    
@bp.route('/<competency_id>', methods=['GET', 'PUT'])
def competency_api(competency_id):
    try:
        if request.method == 'PUT':
            competencies_json = request.json
            if competencies_json:
                competency = Competency.from_json(competencies_json)
                get_db().add_competency(competency)
        elif request.method == 'GET':
            competency = get_db().get_competency(competency_id)
            return jsonify(competency.__dict__)
    except Exception:
        return ""
    
@bp.route('/<competency_id>/elements', methods=['GET', 'POST'])
def competency_elements_api(competency_id):
    try:
        if request.method == 'PUT':
            elements_json = request.json
            if elements_json:
                element = Element.from_json(elements_json)
                get_db().add_competency_element(element)
        elif request.method == 'GET':
            if request.args:
                name = request.args.get("name")
                element = get_db().get_element(name)
                return jsonify(element.__dict__)
            elements = get_db().get_competency_elements(competency_id)
            json = [element.__dict__ for element in elements]
        return jsonify(json)
    except Exception:
        return ""
    
##NEED TO IMPLEMENT GET ELEMENT BY ID    
@bp.route('/<competency_id>/elements/<int:element_id>', methods=['GET', 'PUT'])
def competency_element_api(element_id):
    try:
        if request.method == 'PUT':
            elements_json = request.json
            if elements_json:
                element = Element.from_json(elements_json)
                get_db().add_competency_element(element)
        elif request.method == 'GET':
            element = get_db().get_element(element_id)
            return jsonify(element.__dict__)
    except Exception:
        return ""