from flask import Blueprint, jsonify, request, flash, make_response, url_for
from ..dbmanager import get_db
from Application.objects.course import Course
bp = Blueprint('courses_api', __name__, url_prefix='/api/courses')

@bp.route('/', methods=['GET', 'POST'])
def courses_api():
    try:
        if request.method == 'POST':
            courses_json = request.json
            if courses_json:
                course = Course.from_json(courses_json)
                get_db().add_course(course)
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
                get_db().add_course(course)
                response = make_response({}, 201)
                return response
        elif request.method == 'GET':
            course = get_db().get_course(course_id)
            url = url_for('courses_api.course_api', course_id=course_id)
            domain_url = url_for('domains_api.domain_api', domain_id=course.domain_id)
            return jsonify(course.to_json(url, domain_url))
    except Exception:
        return ""