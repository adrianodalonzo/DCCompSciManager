from flask import Blueprint, jsonify, request, flash
from ..dbmanager import get_db
from objects.course import Course
bp = Blueprint('courses_api', __name__, url_prefix='/api/courses')

@bp.route('/', methods=['GET', 'POST'])
def courses_api():
    return