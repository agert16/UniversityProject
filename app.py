from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from functools import wraps
from modules.db_utils import load_db
from modules.university import create_university
from modules.classroom import create_room, check_room_capacity
from modules.scheduler import schedule_class, is_room_available
from modules.personnel import add_personnel

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'cMCgr8C4fE'
jwt = JWTManager(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

users = {
    "admin": {"password": "adminpass", "roles": ["admin"]},
    "manager": {"password": "managerpass", "roles": ["manager"]},
    "public": {"password": "publicpass", "roles": ["public"]}
}

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = users.get(username, {})

    if user and user['password'] == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Bad username or password"}), 401
 
def role_required(allowed_roles=None):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorated(*args, **kwargs):
            if allowed_roles is None:
                # If allowed_roles is None, bypass role check (any authenticated user can access)
                return fn(*args, **kwargs)
            current_user = get_jwt_identity()
            user_roles = users.get(current_user, {}).get('roles', [])
            if any(role in allowed_roles for role in user_roles):
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Insufficient role permissions"), 403
        return decorated
    return wrapper  

@app.route('/create_uni', methods=['POST'])
@role_required(['admin'])
def add_university():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({"error": "University name is required"}), 400
    university_id = create_university(name)
    return jsonify({"message": "University created", "university_id": university_id}), 201   

@app.route('/add_room', methods=['POST'])
@role_required(['admin', 'manager'])
def add_room():
    data = request.json
    required_fields = ['university_id', 'name', 'room_type', 'capacity', 'accessibility_features']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing requried field"}), 400
    
    try:
        room_id = create_room(data['university_id'], data['name'], data['room_type'], data['capacity'], data['accessibility_features'])
        return jsonify({"message": "Room added", "room_id": room_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/schedule_class', methods=['POST'])
@role_required(['admin', 'manager', 'public'])
def scheduler():
    data = request.json
    required_fields = ['university_id', 'title', 'room_id', 'timeslot', 'instructor_id']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required field"}), 400
    
    university_id = data['university_id']
    room_id = data['room_id']
    timeslot = data['timeslot']
    expected_capacity = data['expected_capacity']

    try:
        if not is_room_available(university_id, room_id, timeslot):
            return jsonify({"error": "Room is not available at the desired timeslot"}), 400

        if not check_room_capacity(university_id, room_id, expected_capacity):
            return jsonify({"error": "Room does not have enough capacity"}), 400
        
        class_id = schedule_class(data['university_id'], data['title'], data['room_id'], data['timeslot'], data['instructor_id'])
        return jsonify({"message": "Class scheduled", "class_id": class_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/add_personnel', methods=['POST'])
@role_required(['admin', 'manager', 'public'])
def add_person():
    data = request.json
    required_fields = ['university_id', 'name', 'role']
    specializations = data.get('specializations', [])
    accessibility_needs = data.get('accessibilityNeeds', [])

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required field"}), 400

    try:
        personnel_id = add_personnel(data['university_id'], data['name'], data['role'], specializations, accessibility_needs)
        return jsonify({"message": "Personnel added", "personnel_id": personnel_id})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/universities', methods=['GET'])
@jwt_required(optional=True)
def get_universities():
    """Retrieve all universities."""
    data = load_db()
    return jsonify(data['universities'])

@app.route('/universities/<university_id>', methods=['GET'])
@jwt_required(optional=True)
def get_university_by_id(university_id):
    """Retrieve a specific university by ID."""
    data = load_db()
    university = next((uni for uni in data['universities'] if uni['id'] == university_id), None)
    if university:
        return jsonify(university)
    else:
        return jsonify({"message": "University not found"}), 404
    
@app.route('/universities/<university_id>/rooms', methods=['GET'])
@jwt_required(optional=True)
def get_rooms(university_id):
    """Retrieve all rooms for a specific university."""
    data = load_db()
    university = next((uni for uni in data['universities'] if uni['id'] == university_id), None)
    if university:
        return jsonify(university.get('rooms', []))
    else:
        return jsonify({"message": "University not found"}), 404 

@app.route('/universities/<university_id>/classes', methods=['GET'])
@jwt_required(optional=True)
def get_classes(university_id):
    """Retrieve all classes for a specific university."""
    data = load_db()
    university = next((uni for uni in data['universities'] if uni['id'] == university_id), None)
    if university:
        return jsonify(university.get('classes', []))
    else:
        return jsonify({"message": "University not found"}), 404
    
@app.route('/universities/<university_id>/personnel', methods=['GET'])
@jwt_required(optional=True)
def get_personnel(university_id):
    """Retrieve all personnel for a specific university."""
    data = load_db()
    university = next((uni for uni in data['universities'] if uni['id'] == university_id), None)
    if university:
        return jsonify(university.get('personnel', []))
    else:
        return jsonify({"message": "University not found"}), 404

@app.route('/universities/<university_id>/classes/<class_id>', methods=['GET'])
@jwt_required(optional=True)
def get_class_by_id(university_id, class_id):
    """Retrieve a specific class by ID within a university."""
    data = load_db()
    university = next((uni for uni in data['universities'] if uni['id'] == university_id), None)
    if university:
        specific_class = next((cls for cls in university.get('classes', []) if cls['id'] == class_id), None)
        if specific_class:
            return jsonify(specific_class)
        else:
            return jsonify({"message": "Class not found"}), 404
    else:
        return jsonify({"message": "University not found"}), 404

@app.route('/universities/<university_id>/rooms/<room_id>', methods=['GET'])
@jwt_required(optional=True)
def get_room_by_id(university_id, room_id):
    """Retrieve a specific room by ID within a university."""
    data = load_db()
    university = next((uni for uni in data['universities'] if uni['id'] == university_id), None)
    if university:
        specific_room = next((r for r in university.get('rooms', []) if r['id'] == room_id), None)
        if specific_room:
            return jsonify(specific_room)
        else:
            return jsonify({"message": "Room not found"}), 404
    else:
        return jsonify({"message": "University not found"}), 404

@app.route('/universities/<university_id>/personnel/<instructor_id>', methods=['GET'])
@jwt_required(optional=True)
def get_instructor_by_id(university_id, instructor_id):
    """Retrieve a specific instructor by ID within a university."""
    data = load_db()
    university = next((uni for uni in data['universities'] if uni['id'] == university_id), None)
    if university:
        specific_instructor = next((i for i in university.get('personnel', []) if i['id'] == instructor_id), None)
        if specific_instructor:
            return jsonify(specific_instructor)
        else:
            return jsonify({"message": "Instructor not found"}), 404
    else:
        return jsonify({"message": "University not found"}), 404         


