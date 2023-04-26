from flask import Blueprint, jsonify, request, flash, make_response
from ..dbmanager import get_db
from Application.objects.competency import Competency
from Application.objects.element import Element
import oracledb
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
    
@bp.route('/<competency_id>', methods=['GET', 'PUT', 'DELETE'])
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
        
        elif request.method == 'DELETE':
            pass
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
                infoset = {'id': "Success", 'description': 'Successfully updated element'}
                return make_response(infoset, 201)
            
        elif request.method == 'GET':
            try:
                if request.args:
                    id = request.args.get("id")
                    element = get_db().get_element(id)
                    return jsonify(element.to_json())
                elements = get_db().get_competency_elements(competency_id)
                json = [element.__dict__ for element in elements]
                return jsonify(json)
            except Exception:
                    error_infoset = {'id': 'Not Found',
                            'description': 'Url not found on this server.'}
                    return make_response(jsonify(error_infoset), 404)
    
    except oracledb.Error:
        error_infoset = {'id': 'Internal Service Error',
                        'description': 'There is problems in the database. Please try again later.'}
        return make_response(error_infoset, 500)
    
    except Exception:
        error_infoset = {'id': 'Internal Service Error',
                        'description': 'There is problems in the database. Please try again later.'}
        return make_response(jsonify(error_infoset), 500)
    
@bp.route('/<competency_id>/elements/<int:element_id>', methods=['GET', 'PUT', 'DELETE'])
def competency_element_api(competency_id, element_id):
    try:   
        if request.method == 'PUT':
            elements_json = request.json
            if elements_json:
                element = Element.from_json(elements_json)
                existing_element = get_db().get_element(element.id)
                if existing_element:
                    get_db().modify_competency_element(element)
                    infoset = {'id': "Success", 'description': 'Successfully updated element'}
                    return make_response(jsonify(infoset), 200)
                get_db().add_competency_element(element)
                infoset = {'id': "Success", 'description': 'Successfully added element'}
                return make_response(jsonify(infoset), 201)
            
        elif request.method == 'GET':
            try:
                element = get_db().get_competency_element(competency_id, element_id)
                return jsonify(element.to_json()), 200
            except Exception:
                error_infoset = {'id': 'Bad Request',
                        'description': 'Element not found, please insert a valid element id.'}
                return make_response(jsonify(error_infoset), 400)
        
        elif request.method == 'DELETE':
            try:
                element = get_db().get_competency_element(competency_id, element_id)
                get_db().delete_competency_element(element)
                infoset = {'id': "Success", 'description': 'Successfully deleted element'}
                return make_response(jsonify(infoset), 204)
            except Exception:
                error_infoset = {'id': 'Bad Request',
                        'description': 'Element not found, please insert a valid element id.'}
                return make_response(jsonify(error_infoset), 400)
        
    except oracledb.Error:
        error_infoset = {'id': 'Internal Service Error',
                        'description': 'There is problems in the database. Please try again later.'}
        return make_response(error_infoset, 500)
    
    except Exception:
        error_infoset = {'id': 'Not Found',
                        'description': 'Url not found on this server.'}
        return make_response(jsonify(error_infoset), 404)