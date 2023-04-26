from flask import Blueprint, jsonify, request, flash, make_response, url_for
from ..dbmanager import get_db
from Application.objects.course import Course
import oracledb
bp = Blueprint('courses_api', __name__, url_prefix='/api/courses')

@bp.route('/', methods=['GET', 'POST'])
def courses_api():
    try:
        if request.method == 'POST':
            courses_json = request.json
            if courses_json:
                course = Course.from_json(courses_json)
                get_db().add_course(course)
                infoset = {'id': "Success", 'description': 'Successfully added course.'}
                return make_response(jsonify(infoset), 201)
            
        elif request.method == 'GET':
            if request.args:
                id = request.args.get("id")
                courses = get_db().get_all_courses()
                course = [course for course in courses if course.id == id]
                url = url_for('courses_api.course_api', course_id=course.id)
                domain_url = url_for('domains_api.domain_api', domain_id=course.domain_id)
                return jsonify(course[0].to_json(url, domain_url))
        courses = get_db().get_all_courses()
        json = [course.to_json(url_for('courses_api.course_api', course_id=course.id), url_for('domains_api.domain_api', domain_id=course.domain_id)) for course in courses]
        return jsonify(json)
    except Exception:
        return ""
    
@bp.route('/<course_id>', methods=['GET', 'PUT', 'DELETE'])
def course_api(course_id):
    try:
        if request.method == 'PUT':
            courses_json = request.json
            if courses_json:
                course = Course.from_json(courses_json)
                existing_element = get_db().get_course(course.id)
                if existing_element:
                    get_db().modify_course(course)
                    infoset = {'id': "Success", 'description': 'Successfully updated course.'}
                    return make_response(jsonify(infoset), 200)
                get_db().add_course(course)
                infoset = {'id': "Success", 'description': 'Successfully added course.'}
                return make_response(jsonify(infoset), 201)
            
        elif request.method == 'GET':
            try:
                course = get_db().get_course(course_id)
                url = url_for('courses_api.course_api', course_id=course_id)
                domain_url = url_for('domains_api.domain_api', domain_id=course.domain_id)
                return jsonify(course.to_json(url, domain_url))
            except Exception:
                error_infoset = {'id': 'Bad Request',
                        'description': 'Element not found, please insert a valid element id.'}
                return make_response(jsonify(error_infoset), 400)
        
        elif request.method == 'DELETE':
            try:
                course = get_db().get_course(course_id)
                get_db().delete_course(course_id)
                infoset = {'id': "Success", 'description': 'Successfully deleted course'}
                return make_response(jsonify(infoset), 204)
            except Exception:
                error_infoset = {'id': 'Bad Request',
                        'description': 'Course not found, please insert a valid course id.'}
                return make_response(jsonify(error_infoset), 400)
    
    except oracledb.Error:
        error_infoset = {'id': 'Internal Service Error',
                        'description': 'There is problems in the database. Please try again later.'}
        return make_response(jsonify(error_infoset), 500)
    
    except Exception:
        error_infoset = {'id': 'Not Found',
                        'description': 'Url not found on this server.'}
        return make_response(jsonify(error_infoset), 404)