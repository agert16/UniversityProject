import json

def load_db():
    with open('db/data.json', 'r') as db:
        return json.load(db)

def save_db(data):
    with open('db/data.json', 'w') as db:
        json.dump(data, db, indent=4) 