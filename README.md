# University Project

## Server Configuration Instructions:
 
To start the server, run the following command in terminal in the directory of the project:

```bash
flask run
```

Once the server is running, you can now call the apis listed in the project with the valid format specified below.

## URI Prefix
To use the application after it is up and running, you must use the following URI prefix:
```
http://127.0.0.1:5000
```

This application will run on the local machine and use port 5000.

## API endpoints & format
### ```/login``` endpoint
This endpoint is used to login as a user.

It can be reached via POST request with the following JSON structure in the body as an example:

```
{
    "username": "admin",
    "password": "adminpass"
}
```
```
{
    "username": "manager",
    "password": "managerpass"
}
```
```
{
    "username": "public",
    "password": "publicpass"
}
```

This API will return an access token that is required for POSTing anything. There are 3 users specified: Admin, Manager, and Public. Their credentials are listed in the JSONs above. 

Only Admins can create universities and Admins and Managers can create new rooms. Public users can create everything else. 

An example of the response:

```
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMjczNzMzMSwianRpIjoiY2MzMDlkZWQtY2Q1Mi00Yjc3LThkNGQtMGM2NzFhMTQyODc1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzEyNzM3MzMxLCJjc3JmIjoiOTY5MzZjYjgtNTY2MS00MzM0LTg4ZDItOTI5ZTIxZTNhZmRhIiwiZXhwIjoxNzEyNzM4MjMxfQ.bcZ4fN5lfCtW_i5zBqm1KXZS8OIPcCynrbVyl2jXVtg"
}
```

### ```/create_uni``` endpoint
This endpoint is used to create a university.

It can be reached via POST request with the following header:
```
Authorization: Bearer <admin-access-token>
```
and with the following JSON structure in the body. Only name is required:
```
{
    "name": "Harvard University" 
}
```

## ```/add_room``` endpoint
This endpoint is used to add a room to a specific university.

It can be reached via POST request with the following header:
```
Authorization: Bearer <admin/manager-access-token>
```

and with the following JSON structure in the body:
```
{
    "university_id": "university_id_2",
    "name": "Lounge",
    "room_type": "Lounge",
    "capacity": "100",
    "accessibility_features": []
}
```
```university_id```, ```name```, ```room_type```, ```capacity```, and ```accessibility_features``` are all required inputs for this endpoint.

This API will return a JSON of the new ```room_id``` and a message of the room being added.

An example of the response:
```
{
    "message": "Room added",
    "room_id": "room_id_2"
}
```

## ```/schedule_class``` endpoint
This endpoint is used to schedule a class at a university with a specific instructor.

It can be reached via POST request with the following header:
```
Authorization: Bearer <admin/manager/public-access-token>
```

and with the following JSON structure in the body:
```
{
  "university_id": "university_id_1",
  "title": "Biology 102",
  "room_id": "room_id_2",
  "timeslot": "Monday 00:00-02:30",
  "instructor_id": "instructor_id_2",
  "expected_capacity": 50
}
```
```university_id```, ```title```, ```room_id```, ```timeslot```, ```instructor_id``` and ```expected_capacity``` are all required inputs for this endpoint.

This API will return a JSON of the new ```class_id``` and a message of the room being added if there are no scheduling or accessibility conflicts.

An example of the responses:
```
{
    "class_id": "class_id_7",
    "message": "Class scheduled"
}
```
```
{
    "error": "Room is not available at the desired timeslot"
}
```
```
{
    "error": "Room room_id_2 does not meet the instructor's accessibility needs"
}
```
```
{
    "error": "Room does not have enough capacity"
}
```

## ```/add_personnel``` endpoint
This endpoint is used to add university employees to a specific university.

It can be reached via POST request with the following header:
```
Authorization: Bearer <admin/manager/public-access-token>
```

and with the following JSON structure in the body:
```
{
    "university_id": "university_id_2",
    "name": "Nadav Gertel",
    "role": "Computer Science Professor",
    "accessibilityNeeds": []
}
```
```university_id```, ```name```, and ```role``` are all required inputs for this endpoint. ```accessibilityNeeds``` and ```specializations``` are optional inputs.

This API will return a JSON of the new ```instructor_id``` and a message of the personnel being added to the university.

An example of the response:
```
{
    "message": "Personnel added",
    "personnel_id": "instructor_id_2"
}
```

## ```/universities``` endpoint
This endpoint is used to retrieve all universities and their information such as personnel, rooms, and classes.

It can be reached via GET request.

An example of the response:
```
{
        "classes": [
            {
                "id": "class_id_1",
                "instructor": "instructor_id_1",
                "room_id": "room_id_1",
                "timeslot": "Thursday 08:00-11:30",
                "title": "Biology 101"
            }
        ],
        "id": "university_id_2",
        "name": "Harvard University",
        "personnel": [
            {
                "accessibilityNeeds": [],
                "id": "instructor_id_1",
                "name": "Nadav Gertel",
                "role": "Computer Science Professor",
                "specializations": []
            }
        ],
        "rooms": [
            {
                "accessibilityFeatures": [],
                "capacity": "100",
                "id": "room_id_1",
                "name": "Bio Lab",
                "type": "Lab"
            }
        ]
    }
```

## ```/universities/<university_id>``` endpoint
This endpoint is used to retrieve a specified university given the ```university_id``` in the endpoint.

It can be reached via GET request.


## ```/universities/<university_id>/rooms``` endpoint
This endpoint is used to retrieve all the rooms from a specified university given the ```university_id``` in the endpoint.

It can be reached via GET request.

An example of the response:
```
{
    "rooms": [
        {
            "accessibilityFeatures": [],
            "capacity": "100",
            "id": "room_id_1",
            "name": "Bio Lab",
            "type": "Lab"
        }
    ]
}
```

## ```/universities/<university_id>/classes``` endpoint
This endpoint is used to retrieve all the classes from a specified university given the ```university_id``` in the endpoint.

It can be reached via GET request.

An example of the response:
```
{
    "classes": [
        {
            "id": "class_id_1",
            "instructor": "instructor_id_1",
            "room_id": "room_id_1",
            "timeslot": "Thursday 08:00-11:30",
            "title": "Biology 101"
        }
    ]
}
```

## ```/universities/<university_id>/personnel``` endpoint
This endpoint is used to retrieve all the personnel from a specified university given the ```university_id``` in the endpoint.

It can be reached via GET request.

An example of the response:
```
{
    "personnel": [
        {
            "accessibilityNeeds": [],
            "id": "instructor_id_1",
            "name": "Nadav Gertel",
            "role": "Computer Science Professor",
            "specializations": []
        }
    ],
}
```

## ```/universities/<university_id>/classes/<class_id>``` endpoint
This endpoint is used to retrieve a specific class from a specified university given the ```university_id``` and ```class_id``` in the endpoint.

It can be reached via GET request.

## ```/universities/<university_id>/rooms/<room_id>``` endpoint
This endpoint is used to retrieve a specific room from a specified university given the ```university_id``` and ```room_id``` in the endpoint.

It can be reached via GET request.

## ```/universities/<university_id>/personnel/<instructor_id>``` endpoint
This endpoint is used to retrieve a specific employee from a specified university given the ```university_id``` and ```instructor_id``` in the endpoint.

It can be reached via GET request.


## How to Run the Test Suite
To run the unit tests, navigate to the root of the ```UniversityProject``` folder.

You can then copy and paste these lines of code into terminal to run all unit tests:
```
export PYTHONPATH=$PYTHONPATH:$(pwd)
python3 -m unittest discover tests
```
You should see
```
Ran 12 tests in 0.00Xs
OK
```
in terminal indicating a successful run of all unit tests.