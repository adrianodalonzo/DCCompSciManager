from flask import Blueprint, jsonify, request, url_for, make_response, url_for
from ..dbmanager import get_db
from Application.objects.domain import Domain
import oracledb

bp = Blueprint('domains_api', __name__, url_prefix='/api/domains')

@bp.route('/', methods=['GET', 'POST'])
def domains_api():
    try:
        if request.method == 'POST':
            try:
                domains_json = request.json
                if domains_json:
                    domain = Domain.from_json(domains_json)
                    get_db().add_domain(domain)
                    infoset = {'id': "Success", 'description': 'Successfully added domain.'}
                    return make_response(jsonify(infoset), 201)
                    
            except Exception:
                error_infoset = {'id': 'Bad Request',
                        'description': 'Domain with this id already exists, please add a new domain.'}
                return make_response(jsonify(error_infoset), 400)
            
        elif request.method == 'GET':
            if request.args:
                id = int(request.args.get("id"))
                domain = get_db.get_domain(id)
                courses = get_db().get_courses_by_domain(domain.id)
                url = url_for('domains_api.domain_api', domain_id=domain.domain.id)
                all_course_urls = []
                for course in courses:
                    all_course_urls.append(url_for('courses_api.course_api', course_id=course.id))
                return jsonify(domain.to_json(url, all_course_urls)), 200

        domains = get_db().get_all_domains()
        json = []
        for domain in domains:
            url = url_for('domains_api.domain_api', domain_id=domain.id)
            courses = get_db().get_courses_by_domain(domain.id)
            all_courses_url = []
            for course in courses:
                course_url = url_for('courses_api.course_api', course_id=course.id)
                all_courses_url.append(course_url)
            json.append(domain.to_json(url, all_courses_url))
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
                existing_domain = get_db().get_domain(domain.id)
                if existing_domain:
                    get_db().modify_domain(domain)
                    infoset = {'id': "Success", 'description': 'Successfully updated domain.'}
                    return make_response(jsonify(infoset), 200)
                get_db().add_domain(domain)
                infoset = {'id': "Success", 'description': 'Successfully added domain.'}
                return make_response(jsonify(infoset), 201)
            
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
            get_db().delete_course(domain.id)
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