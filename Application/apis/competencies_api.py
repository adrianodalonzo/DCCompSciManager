from flask import Blueprint, jsonify, request, make_response, url_for
from ..dbmanager import get_db
from Application.objects.competency import Competency
from Application.objects.element import Element
import oracledb
bp = Blueprint('competencies_api', __name__, url_prefix='/api/competencies')

@bp.route('', methods=['GET', 'POST'])
def competencies_api():
    try:
        if request.method == 'POST':
            competencies_json = request.json
            
            if competencies_json:
                competency = Competency.from_json(competencies_json)
                get_db().add_competency(competency)
                infoset = {'id': "Success", 'description': 'Successfully added competency.'}
                response = make_response(jsonify(infoset), 201)
                response.headers['Location'] = url_for('competencies_api.competency_api', competency_id=competency.id)
                return response
            
        elif request.method == 'GET':
            if request.args.get("id"):
                id = request.args.get("id")
                competency = get_db().get_competency(id)
                elements = get_db().get_competency_elements(competency.id)
                url = url_for('competencies_api.competency_api', competency_id=competency.id)
                all_elements_urls = []
                for element in elements:
                    all_elements_urls.append(url_for('competencies_api.competency_element_api', competency_id=competency.id, element_id=element.id))
                return jsonify(competency.to_json(url, all_elements_urls)), 200
            
            page_num = 1
            if request.args.get("page"):
                    page = request.args.get("page")
                    if page:
                        page_num = int(page)
                        
            competencies, prev_page, next_page = get_db().get_all_competencies(page_num=page_num, page_size=10)
            
            json = {'prev_page': prev_page, 
                    'next_page': next_page, 
                    'results':[competency.to_json(url_for('competencies_api.competency_api', competency_id=competency.id), [url_for('competencies_api.competency_element_api', competency_id=competency.id, element_id=element.id) for element in get_db().get_competency_elements(competency.id)]) for competency in competencies]}
            return jsonify(json), 200

    except oracledb.Error:
        error_infoset = {'id': 'Internal Service Error',
                        'description': 'There is problems in the database. Please try again later.'}
        return make_response(jsonify(error_infoset), 500)
    
    except Exception:
        error_infoset = {'id': 'Not Found',
                        'description': 'Url not found on this server.'}
        return make_response(jsonify(error_infoset), 404)
    
@bp.route('/<competency_id>', methods=['GET', 'PUT', 'DELETE'])
def competency_api(competency_id):
    try:
        if request.method == 'PUT':
            competencies_json = request.json
            if competencies_json:
                competency = Competency.from_json(competencies_json)
                existing_competency = get_db().get_competency(competency.id)
                
                if existing_competency:
                    get_db().modify_competency(competency)
                    infoset = {'id': "Success", 'description': 'Successfully updated competency.'}
                    response = make_response(jsonify(infoset), 200)
                    response.headers['Location'] = url_for('competencies_api.competency_api', competency_id=competency.id)
                    return response
                
                get_db().add_competency(competency)
                infoset = {'id': "Success", 'description': 'Successfully added competency'}
                response = make_response(jsonify(infoset), 201)
                response.headers['Location'] = url_for('competencies_api.competency_api', competency_id=competency.id)
                return response

        elif request.method == 'GET':
            try:
                competency = get_db().get_competency(competency_id)
                elements = get_db().get_competency_elements(competency.id)
                url = url_for('competencies_api.competency_api', competency_id=competency.id)
                all_elements_urls = []
                for element in elements:
                    all_elements_urls.append(url_for('competencies_api.competency_element_api', competency_id=competency.id, element_id=element.id))
                return jsonify(competency.to_json(url, all_elements_urls))
            
            except Exception:
                error_infoset = {'id': 'Bad Request',
                        'description': 'Element not found, please insert a valid element id.'}
                return make_response(jsonify(error_infoset), 400)
        
        elif request.method == 'DELETE':
            try:
                competency = get_db().get_competency(competency_id)
                get_db().delete_competency(competency.id)
                infoset = {'id': "Success", 'description': 'Successfully deleted competency.'}
                return make_response(jsonify(infoset), 204)
            
            except Exception:
                error_infoset = {'id': 'Bad Request',
                        'description': 'Competency not found, please insert a valid competency id.'}
                return make_response(jsonify(error_infoset), 400)
    
    except oracledb.Error:
        error_infoset = {'id': 'Internal Service Error',
                        'description': 'There is problems in the database. Please try again later.'}
        return make_response(jsonify(error_infoset), 500)
    
    except Exception:
        error_infoset = {'id': 'Not Found',
                        'description': 'Url not found on this server.'}
        return make_response(jsonify(error_infoset), 404)
    
@bp.route('/<competency_id>/elements', methods=['GET', 'POST'])
def competency_elements_api(competency_id):
    try:
        if request.method == 'POST':
            elements_json = request.json
            
            if elements_json:
                element = Element.from_json(elements_json)
                get_db().add_competency_element(element)
                infoset = {'id': "Success", 'description': 'Successfully added element'}
                response = make_response(jsonify(infoset), 201)
                response.headers['Location'] = url_for('competencies_api.competency_element_api', competency_id=competency_id, element_id=get_db().get_last_element_id())
                return response
                
        elif request.method == 'GET':
            if request.args:
                id = int(request.args.get("id"))
                element = get_db().get_element(id)
                return jsonify(element.to_json(url_for('competencies_api.competency_element_api', competency_id=competency_id, element_id=element.id))), 200
            
            elements = get_db().get_competency_elements(competency_id)
            json = [element.to_json(url_for('competencies_api.competency_element_api', competency_id=competency_id, element_id=element.id)) for element in elements]
            return jsonify(json), 200
    
    except oracledb.Error:
        error_infoset = {'id': 'Internal Service Error',
                        'description': 'There is problems in the database. Please try again later.'}
        return make_response(jsonify(error_infoset), 500)
    
    except Exception as e:
        error_infoset = {'id': 'Not Found',
                        'description': 'Url not found on this server.'}
        return make_response(jsonify(error_infoset), 404)
    
@bp.route('/<competency_id>/elements/<int:element_id>', methods=['GET', 'PUT', 'DELETE'])
def competency_element_api(competency_id, element_id):
    try:   
        if request.method == 'PUT':
            elements_json = request.json
            if elements_json:
                element = Element.from_json(elements_json)
                existing_element = get_db().get_element(element_id)
                existing_element.id = element_id
                
                if existing_element:
                    get_db().modify_competency_element(existing_element)
                    infoset = {'id': "Success", 'description': 'Successfully updated element'}
                    response = make_response(jsonify(infoset), 200)
                    response.headers['Location'] = url_for('competencies_api.competency_element_api', competency_id=competency_id, element_id=element_id)
                    return response
                
                infoset = {'id': "Not Supported", 'description': 'Does not support adding a new element in this route.'}
                return make_response(jsonify(infoset), 404)
            
        elif request.method == 'GET':
            try:
                element = get_db().get_competency_element(competency_id, element_id)
                return jsonify(element.to_json(url_for('competencies_api.competency_element_api', competency_id=competency_id, element_id=element.id))), 200
            
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
        return make_response(jsonify(error_infoset), 500)
    
    except Exception:
        error_infoset = {'id': 'Not Found',
                        'description': 'Url not found on this server.'}
        return make_response(jsonify(error_infoset), 404)