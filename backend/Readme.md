# Casting Agency API
To access the API one needs to have correct credentials.
The methods one is allowed to send depends on the perimissions that were given to him. API does the following with permission nedded in round brackets:
- Get a list of movies (get:movies)
- Get a list of actors (get:actors)
- Delete an actor (delete:actors)
- Delete a movie (delete:movies)
- Post an actor (post:actors)
- Post a movie (post:movies)
- Update an actor (patch:actors)
- Update a movie (patch:movies)

## Pre-requisites
### 1. Python 3.7
Follow instructions to install verion 3.7 [python docs](https://docs.python.org/3.7/using/unix.html#getting-and-installing-the-latest-version-of-python)

### 2. **Virtual Enviornment** 
We recommend working within a virtual environment whenever using Python for projects. 

Enter this commands in terminal to install and start Virtual Enviroment:
One of the dependencies doesn't work on python version 3.8 and above, so make sure you use 3.7.
```
py -3.7 -m venv venv
venv\Scripts\activate 
```
**or**
```
python3.7 -m venv venv
source venv\Scripts\activate 
```

### 3. **PIP Dependencies**
Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and run:
```
pip install -r requirements.txt
```
**or**
```
pip3 install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.

### 4. Database
Database should be instantiated the first time you start the app automatically. Same with test_app.py. It will be empty so the first get request will return 404. You need to post first before get request will work.
You do need postgres installed on your computer. To install it follow this [link](https://www.postgresql.org/download/).

## Running the server
From `/backend` directory first ensure you are working in the virtual enviroment you've created, then set enviroment variables:
```
set DB_USER=<YOUR DATABASE USERNAME>
set DB_PASSWORD=<PASSWORD FOR YOUR DATABASE USER>
source setup.sh
```
or
```
$env:DB_USER = <YOUR DATABASE USERNAME>
$env:DB_PASSWORD = <PASSWORD FOR YOUR DATABASE USER>
source setup.sh
```
or
```
export DB_USER=<YOUR DATABASE USERNAME>
export DB_PASSWORD=<PASSWORD FOR YOUR DATABASE USER>
source setup.sh
```

Then run the srerver with:
```
python app.py
```
## Testing
### Python test
TESTS FOR ALL PERMISSIONS ARE MADE IN POSTMAN
**`casting_agency.postman_collection.json`**
To run the tests make sure you are in the virtual enviroment, and you have the enviroment variables set up then run:
```
python test_app.py
```
There is a token in the test_app.py used as a variable, so the tests work.
The first test should be succesfull others will fail.
In order to run multiple tests, after each test run:
```
dropdb casting_agency_test
```
If you use a different username than default:
```
dropdb -U <USER> casting_agency_test
```

### Postman test
Import `casting_agency.postman_collection.json` and run it. The token should be valid for 7 days, so it should work.

## API Reference
### Getting started
Base URL:
- The app can be run locally on the default: `http://127.0.0.1:5000/`
- The app is hosted on: `https://jaka-casting-agency.herokuapp.com/`

### Error Handling
Errors are returned as JSON objects in this format:
```
{
      "success": False, 
      "error": 400,
      "message": "Bad request"
}
```
The API can several errors when the request fails:
* 400: 
    * Bad request
    * Unable to parse authentication token
    * Unable to find the appropriate key
    * Permission not included in JWT
* 401: 
    * Authorization malformed
    * Token expired
    * Incorrect claims. Check audience and issuer
    * Authorization header is expected
    * Token not found
    * Authorization header must start with "Bearer"
* 403: Permission not found
* 404: Not found
* 405: Method Not Allowed
* 409: Already exists
* 422: Unprocessable
* 500: Internal Server Error

### Endpoints
#### GET /movies
The permission needed to access the endpoint: `get:movies`
Returns a list of movie objects paginated by 3 items in the list, containing id, release_date and title
##### Sample return
```
{
    "length": 6,
    "movies": [
        {
            "id": 27,
            "release_date": "Tue, 15 Jun 2021 00:00:00 GMT",
            "title": "Sample Movie"
        },
        {
            "id": 28,
            "release_date": "Thu, 17 Jun 2021 00:00:00 GMT",
            "title": "Another Sample Movie"
        },
        {
            "id": 31,
            "release_date": "Thu, 17 Jun 2021 00:00:00 GMT",
            "title": "Another Sample"
        }
    ],
    "success": true
}
```

#### GET /actors
The permisson needed for this endpoint. `get:actors`
Returns a list of actor objects paginated by 3 per page, containing age, gender, id and name.
##### Sample return
```
{
    "actors": [
        {
            "age": 40,
            "gender": "female",
            "id": 5,
            "name": "Sample Name"
        },
        {
            "age": 20,
            "gender": "male",
            "id": 7,
            "name": "Sample Actor"
        },
        {
            "age": 1,
            "gender": "postman",
            "id": 8,
            "name": "Mr. Postman Test"
        }
    ],
    "length": 4,
    "success": true
}
```

#### DELETE /movie/{int:id}
The permission needed for this endpoint: `delete:movies`
It deletes the movie with the provided id. It returns the deleted movie.
##### Sample return
```
{
    "deleted_movie": {
        "id": 27,
        "release_date": "Tue, 15 Jun 2021 00:00:00 GMT",
        "title": "Simple Movie"
    },
    "success": true
}
```

#### DELETE /actor/{int:id}
The permission needed for this endpoint: `delete:actors`
It deletes the actor with the provided id. It returns the deleted actor.
##### Sample return
```
{
    "deleted_actor": {
        "age": 40,
        "gender": "male",
        "id": 5,
        "name": "Sample actor"
    },
    "success": true
}
```

#### POST /movies
The permission needed: `post:movies`.
It recieves a JSON object containing the title of the movie and the release date.
##### Sample request
```
{
    "title": "Postman Testing",
    "release_date": "2021-06-16"
}
```
And it returns this new movie object when successfull.
##### Sample return
```
{
    "new_movie": {
        "id": 35,
        "release_date": "Wed, 16 Jun 2021 00:00:00 GMT",
        "title": "Postman Testing"
    },
    "success": true
}
```

#### POST /actors
The permission needed: `post:actors`.
It recieves a JSON object containing name age and gender of the actor.
##### Sample request
```
{
    "name": "Mr. Testing Postman.",
    "age": 1,
    "gender": "postman"
}
```
And it returns the newly created actor object.
##### Sample return
```
{
    "new_actor": {
        "age": 1,
        "gender": "postman",
        "id": 10,
        "name": "Mr. Testing Postman."
    },
    "success": true
}
```

#### PATCH /movies/{int:id}
The permission needed: `patch:movies`.
It recieves a JSON object containing whatever field needs to changed and it process it by the provided id.
##### Sample request
```
{
    "title": "Patched Title"
}
```
It returns the updated movie.
##### Sample return
```
{
    "success": true,
    "updated_movie": {
        "id": 28,
        "release_date": "Thu, 17 Jun 2021 00:00:00 GMT",
        "title": "Patched Title"
    }
}
```

#### PATCH /actors/{int:id}
The permission needed: `patch:actors`.
It recieves a JSON object containing whatever field needs to changed and it process it by the provided id.
##### Sample request
```
{
    "name": "Mr. Patched Postman"
}
```
It returns the updated actor object.
##### Sample return
```
{
    "success": true,
    "updated_actor": {
        "age": 1,
        "gender": "postman",
        "id": 8,
        "name": "Mr. Patched Postman"
    }
}
```