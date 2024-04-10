from .db_utils import load_db, save_db

def add_personnel(university_id, name, role, specializations=None, accessibilityNeeds=None):
    db = load_db()
    university = next((u for u in db['universities'] if u['id'] == university_id), None)
    if not university:
        raise ValueError("University not found")
    
    personnel_id = f"instructor_id_{len(university['personnel']) + 1}"
    new_personnel = {
        "id": personnel_id,
        "name": name,
        "role": role,
        "specializations": specializations if specializations else [],
        "accessibilityNeeds": accessibilityNeeds if accessibilityNeeds else []
    }
    university['personnel'].append(new_personnel)
    save_db(db)
    return personnel_id