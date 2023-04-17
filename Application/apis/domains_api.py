from flask import Blueprint, jsonify, request, flash
from ..dbmanager import get_db
from objects.domain import Domain
bp = Blueprint('address_api', __name__, url_prefix='/api/domains')

@bp.route('/', methods=['GET', 'POST'])
def domains_api():
    return