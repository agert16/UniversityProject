from .db_utils import load_db, save_db

def create_university(name):
    db = load_db()
    university_id = f"university_id_{len(db['universities']) + 1}"
    new_university = {
        "id": university_id,
        "name": name,
        "rooms": [],
        "classes": [],
        "personnel": []
    }

    db['universities'].append(new_university)
    save_db(db)
    return university_id