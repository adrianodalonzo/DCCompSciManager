from flask import Blueprint, jsonify, request, make_response, url_for
from ..dbmanager import get_db
from Application.objects.course import Course
import oracledb

bp = Blueprint('courses_api', __name__, url_prefix='/api/courses')

@bp.route('', methods=['GET', 'POST'])
def courses_api():
    try:
        if request.method == 'POST':
            try:
                courses_json = request.json
                if courses_json:
                    course = Course.from_json(courses_json)
                    get_db().add_course(course)
                    infoset = {'id': "Success", 'description': 'Successfully added course.'}
                    response = make_response(jsonify(infoset), 201)
                    response.headers['Location'] = url_for('courses_api.course_api', course_id=course.id)
                    return response
                
            except Exception:
                error_infoset = {'id': 'Bad Request',
                        'description': 'Course with this id already exists, please add a new course.'}
                return make_response(jsonify(error_infoset), 400)
            
        elif request.method == 'GET':
            if request.args.get("id"):
                id = request.args.get("id")
                course = get_db().get_course(id)
                url = url_for('courses_api.course_api', course_id=course.id)
                domain_url = url_for('domains_api.domain_api', domain_id=course.domain_id)
                return jsonify(course.to_json(url, domain_url)), 200
                if request.args.get("page"):
                    page = request.args.get("page")
                    if page:
                        page_num = int(page)
            
            courses, prev_page, next_page = get_db().get_all_courses(page_num=page_num, page_size=10)
            json = {'prev_page': prev_page, 
                    'next_page': next_page, 
                    'results':[course.to_json(url_for('courses_api.course_api', course_id=course.id), url_for('domains_api.domain_api', domain_id=course.domain_id)) for course in courses]}
            return jsonify(json), 200
    
    except oracledb.Error:
        error_infoset = {'id': 'Internal Service Error',
                        'description': 'There is problems in the database. Please try again later.'}
        return make_response(jsonify(error_infoset), 500)
    
    except Exception:
        error_infoset = {'id': 'Not Found',
                        'description': 'Url not found on this server.'}
        return make_response(jsonify(error_infoset), 404)
    
@bp.route('/<course_id>', methods=['GET', 'PUT', 'DELETE'])
def course_api(course_id):
    try:
        if request.method == 'PUT':
            courses_json = request.json
            if courses_json:
                course = Course.from_json(courses_json)
                existing_course = get_db().get_course(course.id)
                
                if existing_course:
                    get_db().modify_course(course)
                    infoset = {'id': "Success", 'description': 'Successfully updated course.'}
                    response = make_response(jsonify(infoset), 200)
                    response.headers['Location'] = url_for('courses_api.course_api', course_id=course.id)
                    return response
                
                get_db().add_course(course)
                infoset = {'id': "Success", 'description': 'Successfully added course.'}
                response = make_response(jsonify(infoset), 201)
                response.headers['Location'] = url_for('courses_api.course_api', course_id=course.id)
                return response
            
        elif request.method == 'GET':
            try:
                course = get_db().get_course(course_id)
                url = url_for('courses_api.course_api', course_id=course_id)
                domain_url = url_for('domains_api.domain_api', domain_id=course.domain_id)
                return jsonify(course.to_json(url, domain_url)), 200
            
            except Exception:
                error_infoset = {'id': 'Bad Request',
                        'description': 'Course not found, please insert a valid course id.'}
                return make_response(jsonify(error_infoset), 400)
        
        elif request.method == 'DELETE':
            course = get_db().get_course(course_id)
            get_db().delete_course(course.id)
            infoset = {'id': "Success", 'description': 'Successfully deleted course'}
            return make_response(jsonify(infoset), 204)
    
    except oracledb.Error:
        error_infoset = {'id': 'Internal Service Error',
                        'description': 'There is problems in the database. Please try again later.'}
        return make_response(jsonify(error_infoset), 500)
    
    except Exception:
        error_infoset = {'id': 'Not Found',
                        'description': 'Url not found on this server.'}
        return make_response(jsonify(error_infoset), 404)