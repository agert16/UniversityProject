from .db_utils import load_db, save_db

def create_room(university_id, name, room_type, capacity, accessibility_features):
    db = load_db()
    university = next((u for u in db['universities'] if u['id'] == university_id), None)
    if not university:
        raise ValueError("University not found")
    
    room_id = f"room_id_{len(university['rooms']) + 1}"
    new_room = {
        "id": room_id,
        "type": room_type,
        "name": name,
        "capacity": capacity,
        "accessibilityFeatures": accessibility_features
    }

    university['rooms'].append(new_room)
    save_db(db)
    return room_id

def check_room_capacity(university_id, room_id, expected_capacity):
    db = load_db()
    university = next((u for u in db['universities'] if u['id'] == university_id), None)
    if not university:
        raise ValueError("University not found")
    
    room = next((r for r in university['rooms'] if r['id'] == room_id), None)
    if not room:
        raise ValueError("Room not found")
    return int(room['capacity']) >= expected_capacity
