# :movie_camera: Casting Agency :movie_camera:

## About
The project is split into two sections:
- Backend (API)
- Frontend (React App)

Each section is deployed on different platform:
- API: [https://jaka-casting-agency.herokuapp.com/](https://jaka-casting-agency.herokuapp.com/)
- React App [https://jakapresecnik.github.io/casting_agency/](https://jakapresecnik.github.io/casting_agency/)

If you don't have the permissions, the only screen you can enter is 'Home'. If you log in, both 'actors' and 'movies' will return 'unauthorized', so if you want to test the frontend send me an email to jaka.presecnik@gmail.com and I'll try to give you the permissions as fast as possible, so you won't spend much more time on the review.

###  Tech stack used:
- Python
- Flask
- Postgresql
- React
- SCSS

## Getting started
### Pre-requisites
In order to work with the project locally, you need to have:
- Python 3.7
- Postgresql
- Node.js
- Node Package Manager(NPM)

### Backend Setup 
For detailed instructions how to run the backend and information on API enter `backend` folder.

#### Quick setup
Open the terminal window and run: 
```
py -3.7 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
source setup.sh
export DB_USER=postgres
export DB_PASSWORD=postgres
python app.py
```
There might be other variations of your system. Please try following readme in the backend folder if stuck.

### Frontend setup
Open another terminal and all that is needed to run is: 
```
npm i
npm start
```
The focus on the subject was backend so I will leave readme here blank.

## API Reference
The API is only able to work if the roles are defined. These are the roles:
* Casting Assistant (can view actors and movies only)
* Casting director (can also delete an actor from the database and modify actors and movies)
* Executive Producer (can also add or delete a movie from the database)

the permissions on auth0 are: 
- get:movie
- get:actors
- delete:movies
- delete:actors
- post:movies
- post:actors
- patch:movies
- patch:actors

How the permissions are implemeted in the api follow readme in the backend folder. Also follow backend readme for examples.
[Readme in backend folder](./backend/README.md)

## Authors
Both API and React app done entirely by Jaka Presecnik.