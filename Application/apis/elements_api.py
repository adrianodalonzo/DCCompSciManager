from flask import Blueprint, jsonify, request, flash
from ..dbmanager import get_db
from Application.objects.element import Element
bp = Blueprint('elements_api', __name__, url_prefix='/api/elements')

@bp.route('/', methods=['GET', 'POST'])
def elements_api():
    try:
        if request.method == 'POST':
            elements_json = request.json
            if elements_json:
                element = element.from_json(elements_json)
                get_db().add_element(element)
        elif request.method == 'GET':
            if request.args:
                id = int(request.args.get("id"))
                elements = get_db().get_all_elements()
                element = [element for element in elements if element.id == id]
                return jsonify(element[0].__dict__)
        elements = get_db().get_all_elements()
        json = [element.__dict__ for element in elements]
        return jsonify(json)
    except Exception:
        return ""
    
@bp.route('/<int:element_id>', methods=['GET', 'POST'])
def element_api(element_id):
    try:
        if request.method == 'POST':
            elements_json = request.json
            if elements_json:
                element = element.from_json(elements_json)
                get_db().add_element(element)
        elif request.method == 'GET':
            element = get_db().get_element(element_id)
            return jsonify(element.__dict__)
    except Exception:
        return ""