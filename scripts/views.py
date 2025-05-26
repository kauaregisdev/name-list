from scripts.main import *
from scripts.models import *
from flask import abort, request, jsonify

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request', 'message': str(error)}), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Unauthorized', 'message': str(error)}), 401

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found', 'message': str(error)}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error', 'message': str(error)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username == USERNAME and password == PASSWORD:
        token = generate_token(username)
        return jsonify({'Authorization': 'Bearer '+token})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/name', methods=['POST'])
@requires_jwt
def create_name():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Data must not be null'}), 400
    name = data.get('name')
    if not name.strip():
        return jsonify({'error': 'Name cannot be void'}), 400
    for char in name:
        if char.isdigit():
            return jsonify({'error': 'Names cannot have numbers in it'}), 400
    gender = data.get('gender')
    if gender not in ['b', 'B', 'g', 'G']:
        return jsonify({'error': 'Insert valid gender characters'}), 400
    gender = 'Boy' if gender in ['b', 'B'] else 'Girl'
    new_name = Name(
        name=name,
        gender=gender
    )
    db.session.add(new_name)
    db.session.commit()
    return jsonify({
        'id': new_name.id,
        'name': new_name.name,
        'gender': new_name.gender
    }), 201

@app.route('/name', methods=['GET'])
@requires_jwt
def read_names():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    pagination = Name.query.paginate(page=page, per_page=per_page, error_out=False)
    tasks = [{
        'id': task.id,
        'name': task.name,
        'gender': task.gender
    } for task in pagination.items]
    return jsonify({
        'tasks': tasks,
        'total': pagination.total,
        'page': pagination.page,
        'pages': pagination.pages,
        'per_page': pagination.per_page
    }), 200

@app.route('/name/<int:name_id>', methods=['PUT'])
@requires_jwt
def update_name(name_id):
    name = db.session.get(Name, name_id)
    if not name:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Data not provided'}), 400
    if 'name' in data:
        if not data['name'].strip():
            return jsonify({'error': 'Name cannot be void'}), 400
        for char in data['name']:
            if char.isdigit():
                return jsonify({'error': 'Names cannot have numbers in it'}), 400
    if 'gender' in data and data['gender'] not in ['b', 'B', 'g', 'G']:
        return jsonify({'error': 'Insert valid gender characters'}), 400
    name.name = data.get('name', name.name)
    name.gender = 'b' if name.gender == 'Boy' else 'g'
    name.gender = data.get('gender', name.gender)
    name.gender = 'Boy' if name.gender in ['b', 'B'] else 'Girl'
    db.session.commit()
    return jsonify({
        'id': name.id,
        'name': name.name,
        'gender': name.gender
    }), 200

@app.route('/name/<int:name_id>', methods=['DELETE'])
@requires_jwt
def delete_name(name_id):
    name = db.session.get(Name, name_id)
    if not name:
        abort(404)
    db.session.delete(name)
    db.session.commit()
    return ('', 204)