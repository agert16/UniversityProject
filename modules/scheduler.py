from .db_utils import load_db, save_db
from datetime import datetime, timedelta
import re

def schedule_class(university_id, title, room_id, timeslot, instructor_id, accessibility_needs = []):
    db = load_db()
    university = next((u for u in db['universities'] if u['id'] == university_id), None)
    if not university:
        raise ValueError("University not found")
    
    room = next((r for r in university['rooms'] if r['id'] == room_id), None)
    if not room:
        raise ValueError("Room not found in this university")
    
    instructor = next((p for p in university['personnel'] if p['id'] == instructor_id), None)
    if not instructor:
        raise ValueError("Instructor not found")
    
    if not is_room_accessible_for_personnel(room, instructor):
        raise ValueError(f"Room {room_id} does not meet the instructor's accessibility needs")
    
    new_class = {
        "id": f"class_id_{len(university['classes']) + 1}",
        "title": title,
        "room_id": room_id,
        "timeslot": timeslot,
        "instructor": instructor_id
    }
    university['classes'].append(new_class)
    save_db(db)
    return new_class['id']

def is_room_available(university_id, room_id, new_timeslot):
    db = load_db()
    university = next((u for u in db['universities'] if u['id'] == university_id), None)
    if not university:
        raise ValueError("University not found")
    
    for scheduled_class in university['classes']:
        if scheduled_class['room_id'] == room_id and timeslots_overlap(scheduled_class['timeslot'], new_timeslot):
            return False
    return True
    
def parse_timeslot(timeslot):
    """Parses a timeslot string into a tuple of datetime objects representing the start and end times."""
    if not is_valid_timeslot_format(timeslot):
        raise ValueError("Invalid timeslot format. Please use the format 'Day HH:MM-HH:MM'.")
    
    day, times = timeslot.split()
    start_time_str, end_time_str = times.split('-')
    start_time = datetime.strptime(start_time_str, "%H:%M")
    end_time = datetime.strptime(end_time_str, "%H:%M")

    if end_time <= start_time:
        end_time += timedelta(days=1)
    return day, start_time.time(), end_time.time()    

def is_valid_timeslot_format(timeslot):
    """Checks if the timeslot matches the expected format of 'Day HH:MM-HH:MM'."""
    pattern = r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) (\d{2}):(\d{2})-(\d{2}):(\d{2})$'
    return re.match(pattern, timeslot) is not None

def timeslots_overlap(timeslot1, timeslot2):
    """Checks if two timeslots overlap."""
    day1, start1, end1 = parse_timeslot(timeslot1)
    day2, start2, end2 = parse_timeslot(timeslot2)

    if day1 != day2:
        return False
    
    return not (end1 <= start2 or end2 <= start1)

def is_room_accessible_for_personnel(room, personnel):
    return all(need in room['accessibilityFeatures'] for need in personnel['accessibilityNeeds'])

    