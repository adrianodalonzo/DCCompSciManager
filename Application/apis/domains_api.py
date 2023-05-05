from flask import Blueprint, jsonify, request, url_for, make_response, url_for
from ..dbmanager import get_db
from Application.objects.domain import Domain
import oracledb

bp = Blueprint('domains_api', __name__, url_prefix='/api/domains')

@bp.route('', methods=['GET', 'POST'])
def domains_api():
    try:
        if request.method == 'POST':
            try:
                domains_json = request.json
                if domains_json:
                    domain = Domain.from_json(domains_json)
                    get_db().add_domain(domain)
                    infoset = {'id': "Success", 'description': 'Successfully added domain.'}
                    response = make_response(jsonify(infoset), 201)
                    response.headers['Location'] = url_for('domains_api.domain_api', domain_id=get_db().get_last_domain_id())
                    return response
                    
            except Exception:
                error_infoset = {'id': 'Bad Request',
                        'description': 'Domain with this id already exists, please add a new domain.'}
                return make_response(jsonify(error_infoset), 400)
            
        elif request.method == 'GET':
            if request.args:
                id = int(request.args.get("id"))
                domain = get_db().get_domain(id)
                courses = get_db().get_courses_by_domain(domain.id)
                url = url_for('domains_api.domain_api', domain_id=domain.id)
                all_course_urls = []
                for course in courses:
                    all_course_urls.append(url_for('courses_api.course_api', course_id=course.id))
                return jsonify(domain.to_json(url, all_course_urls)), 200

            page_num = 1
            if request.args.get("page"):
                    page = request.args.get("page")
                    if page:
                        page_num = int(page)
                        
            domains, prev_page, next_page = get_db().get_all_domains(page_num=page_num, page_size=10)
            
            json = {'prev_page': prev_page, 
                    'next_page': next_page, 
                    'results':[domain.to_json(url_for('domains_api.domain_api', domain_id=domain.id), [url_for('courses_api.course_api', course_id=course.id) for course in get_db().get_courses_by_domain(domain.id)]) for domain in domains]}
            return jsonify(json), 200
    
    except oracledb.Error:
        error_infoset = {'id': 'Internal Service Error',
                        'description': 'There is problems in the database. Please try again later.'}
        return make_response(jsonify(error_infoset), 500)
    
    except Exception as e:
        error_infoset = {'id': 'Not Found',
                        'description': 'Url not found on this server.'}
        return make_response(jsonify(error_infoset), 404)
    
@bp.route('/<int:domain_id>', methods=['GET', 'PUT', 'DELETE'])
def domain_api(domain_id):
    try:
        if request.method == 'PUT':
            domains_json = request.json
            if domains_json:
                domain = Domain.from_json(domains_json)
                existing_domain = get_db().get_domain(domain_id)
                domain.id = existing_domain.id
                
                if existing_domain:
                    get_db().modify_domain(domain)
                    infoset = {'id': "Success", 'description': 'Successfully updated domain.'}
                    response = make_response(jsonify(infoset), 200)
                    response.headers['Location'] = url_for('domains_api.domain_api', domain_id=domain_id)
                    return response
                
                infoset = {'id': "Not Supported", 'description': 'Does not support adding a new domain  in this route.'}
                return make_response(jsonify(infoset), 404)
            
        elif request.method == 'GET':
            try:
                domain = get_db().get_domain(domain_id)
                courses = get_db().get_courses_by_domain(domain.id)
                url = url_for('domains_api.domain_api', domain_id=domain_id)
                all_course_urls = []
                for course in courses:
                    all_course_urls.append(url_for('courses_api.course_api', course_id=course.id))
                return jsonify(domain.to_json(url, all_course_urls)), 200
            
            except Exception:
                error_infoset = {'id': 'Bad Request',
                        'description': 'Domain not found, please insert a valid domain id.'}
                return make_response(jsonify(error_infoset), 400)
        
        elif request.method == 'DELETE':
            domain = get_db().get_domain(domain_id)
            get_db().delete_domain(domain.id)
            infoset = {'id': "Success", 'description': 'Successfully deleted domain'}
            return make_response(jsonify(infoset), 204)
        
    except oracledb.Error:
        error_infoset = {'id': 'Internal Service Error',
                        'description': 'There is problems in the database. Please try again later.'}
        return make_response(jsonify(error_infoset), 500)
    
    except Exception:
        error_infoset = {'id': 'Not Found',
                        'description': 'Url not found on this server.'}
        return make_response(jsonify(error_infoset), 404)
