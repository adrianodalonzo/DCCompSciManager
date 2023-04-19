from flask import Blueprint, jsonify, request, flash
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
                courses = get_db().get_courses()
                course = [course for course in courses if course.id == id]
                return jsonify(course[0].__dict__)
        courses = get_db().get_courses()
        json = [course.__dict__ for course in courses]
        return jsonify(json)
    except Exception:
        return ""
    
@bp.route('/<course_id>', methods=['GET', 'PUT'])
def course_api(course_id):
    try:
        if request.method == 'POST':
            courses_json = request.json
            if courses_json:
                course = Course.from_json(courses_json)
                get_db().add_course(course)
        elif request.method == 'GET':
            course = get_db().get_course(course_id)
            return jsonify(course.__dict__)
    except Exception:
        return ""