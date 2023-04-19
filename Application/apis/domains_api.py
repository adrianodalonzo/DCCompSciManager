from flask import Blueprint, jsonify, request, flash
from ..dbmanager import get_db
from Application.objects.domain import Domain
bp = Blueprint('domains_api', __name__, url_prefix='/api/domains')

@bp.route('/', methods=['GET', 'POST'])
def domains_api():
    try:
        if request.method == 'POST':
            domains_json = request.json
            if domains_json:
                domain = Domain.from_json(domains_json)
                get_db().add_domain(domain)
        elif request.method == 'GET':
            if request.args:
                id = int(request.args.get("id"))
                domains = get_db().get_all_domains()
                domain = [domain for domain in domains if domain.id == id]
                return jsonify(domain[0].__dict__)
        domains = get_db().get_all_domains()
        json = [domain.__dict__ for domain in domains]
        return jsonify(json)
    except Exception:
        return ""
    
@bp.route('/<int:domain_id>', methods=['GET', 'PUT'])
def domain_api(domain_id):
    try:
        if request.method == 'POST':
            domains_json = request.json
            if domains_json:
                domain = Domain.from_json(domains_json)
                get_db().add_domain(domain)
        elif request.method == 'GET':
            domain = get_db().get_domain(domain_id)
            return jsonify(domain.__dict__)
    except Exception:
        return "" 