from flask import Flask, jsonify, request, abort
from flask_cors import CORS

from models import *
from helper_functions import *
from auth import AuthError, requires_auth


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#      _                ___           __ _
#     /_\  _ __ _ __   / __|___ _ _  / _(_)__ _
#    / _ \| '_ \ '_ \ | (__/ _ \ ' \|  _| / _` |
#   /_/ \_\ .__/ .__/  \___\___/_||_|_| |_\__, |
#         |_|  |_|                        |___/

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(res):
        res.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization'
            )
        res.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, DELETE, PATCH'
            )

        return res


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#    ___          _
#   | _ \___ _  _| |_ ___ ___
#   |   / _ \ || |  _/ -_|_-<
#   |_|_\___/\_,_|\__\___/__/
#


#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
#    _______________    __         __
#   / ___/ __/_  __/  _/_/__ _____/ /____  _______
#  / (_ / _/  / /   _/_// _ `/ __/ __/ _ \/ __(_-<
#  \___/___/ /_/   /_/  \_,_/\__/\__/\___/_/ /___/

    '''
    @DONE endpoint GET /actors
        - roles that can access the endpoint:
            - Casting Assistant
            - Casting Director
            - Executive Producer
        - returns actors, paginated
        - order_by ID by default, order_by options: name, age
    '''

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        # Sorting by name and by age added, assuming
        # when hiring actors they might need a certain age range.
        # It orders by id if the arg is not known
        order_by = request.args.get('order_by', 'id')
        if order_by == 'name':
            db_actors = Actor.query.order_by(Actor.name).all()
        elif order_by == 'age':
            db_actors = Actor.query.order_by(Actor.age).all()
        else:
            db_actors = Actor.query.order_by(Actor.id).all()

        actors = paginate(request, db_actors)

        if len(actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': actors,
            'length': len(db_actors)
        })


#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
#    _______________    __               _
#   / ___/ __/_  __/  _/_/_ _  ___ _  __(_)__ ___
#  / (_ / _/  / /   _/_//  ' \/ _ \ |/ / / -_|_-<
#  \___/___/ /_/   /_/ /_/_/_/\___/___/_/\__/___/

    '''
    @DONE endpoint GET /movies
        - roles that can access the endpoint:
            - Casting Assistant
            - Casting Director
            - Executive Producer
        - returns list of movies, paginated
    '''

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        # Order can be by release_date, title or by default - ID
        order_by = request.args.get('order_by', 'id')
        if order_by == 'release_date':
            db_movies = Movie.query.order_by(Movie.release_date).all()
        if order_by == 'title':
            db_movies = Movie.query.order_by(Movie.title).all()
        else:
            db_movies = Movie.query.order_by(Movie.id).all()

        movies = paginate(request, db_movies)

        if len(movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': movies,
            'length': len(db_mo)
        })


#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
#     ___  ______   ______________     __         __
#    / _ \/ __/ /  / __/_  __/ __/   _/_/__ _____/ /____  _______
#   / // / _// /__/ _/  / / / _/   _/_// _ `/ __/ __/ _ \/ __(_-<
#  /____/___/____/___/ /_/ /___/  /_/  \_,_/\__/\__/\___/_/ /___/

    '''
    @DONE endpoint DELETE /actors
        - roles that can access the endpoint:
            - Casting Director
            - Executive Producer
        - returns the deleted_actor object
    '''

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        actor = Actor.query.filter_by(id=id).one_or_none()

        if actor is None:
            abort(404)

        try:
            deleted_actor = actor.format()
            actor.delete()

            return jsonify({
                'success': True,
                'deleted_actor': deleted_actor
            })

        except:
            abort(500)


#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
#     ___  ______   ______________     __               _
#    / _ \/ __/ /  / __/_  __/ __/   _/_/_ _  ___ _  __(_)__ ___
#   / // / _// /__/ _/  / / / _/   _/_//  ' \/ _ \ |/ / / -_|_-<
#  /____/___/____/___/ /_/ /___/  /_/ /_/_/_/\___/___/_/\__/___/

    '''
    @DONE endpoint DELETE /movies
        - roles that can access the endpoint:
            - Executive Producer
        - returns the movie that was deleted
    '''

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        movie = Movie.query.filter_by(id=id).one_or_none()

        if movie is None:
            abort(404)

        try:
            deleted_movie = movie.format()
            movie.delete()

            return jsonify({
                'success': True,
                'deleted_movie': deleted_movie
            })

        except:
            abort(500)


#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
#     ___  ____  __________    __         __
#    / _ \/ __ \/ __/_  __/  _/_/__ _____/ /____  _______
#   / ___/ /_/ /\ \  / /   _/_// _ `/ __/ __/ _ \/ __(_-<
#  /_/   \____/___/ /_/   /_/  \_,_/\__/\__/\___/_/ /___/

    '''
    @DONE endpoint POST /actors
        - roles that can access the endpoint:
            - Casting Director
            - Executive Producer
        - returns the actor that was created
        - if the actor already in the library it returns 409 error
          I know that there might be more actors with the same name but it
          is less likely they would work in the same agency, in that case
          we can set another test for age.
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actor(payload):
        body = request.get_json()
        if not body:
            abort(422)

        actor_name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        if actor_name is None or age is None or gender is None:
            abort(400)

        # We get the names of actors and save it as an array
        # If the actor is already in the library it returns 409 error
        actors = Actor.query.with_entities(Actor.name).all()
        actors_array = [name for (name, ) in actors]

        if actor_name in actors_array:
            abort(409)

        try:
            actor = Actor(
                name=actor_name,
                age=age,
                gender=gender
                )
            actor.insert()

            return ({
                'success': True,
                'new_actor': actor.format()
            })
        except:
            abort(500)


#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
#     ___  ____  __________    __               _
#    / _ \/ __ \/ __/_  __/  _/_/_ _  ___ _  __(_)__ ___
#   / ___/ /_/ /\ \  / /   _/_//  ' \/ _ \ |/ / / -_|_-<
#  /_/   \____/___/ /_/   /_/ /_/_/_/\___/___/_/\__/___/

    '''
    @DONE endpoint POST /movies
        - roles that can access the endpoint:
            - Executive Producer
        - returns the movie that was created
    '''

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movie(payload):
        body = request.get_json()
        if not body:
            abort(422)

        movie_title = body.get('title', None)
        release_date = body.get('release_date', None)

        if movie_title is None or release_date is None:
            abort(400)

        try:
            movie = Movie(
                title=movie_title,
                release_date=release_date
            )
            movie.insert()

            return jsonify({
                'success': True,
                'new_movie': movie.format()
            })
        except:
            abort(500)


#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
#     ___  ___ _____________ __    __         __
#    / _ \/ _ /_  __/ ___/ // /  _/_/__ _____/ /____  _______
#   / ___/ __ |/ / / /__/ _  / _/_// _ `/ __/ __/ _ \/ __(_-<
#  /_/  /_/ |_/_/  \___/_//_/ /_/  \_,_/\__/\__/\___/_/ /___/

    '''
    @TODO endpoint PATCH /actors
        - roles that can access the endpoint:
            - Casting Director
            - Executive Producer
        - returns the actor that was modifies
    '''

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actor(payload, id):
        body = request.get_json()

        if not body:
            abort(422)

        actor = Actor.query.filter_by(id=id).one_or_none()

        if actor is None:
            abort(404)

        upd_name = body.get('name', None)
        upd_age = body.get('age', None)
        upd_gender = body.get('gender', None)

        if upd_name is None and upd_age is None and upd_gender is None:
            abort(400)

        actor_exist = Actor.query.filter(Actor.name == upd_name).count()
        if actor_exist:
            abort(409)

        try:
            if upd_name:
                actor.name = upd_name
            if upd_age:
                actor.age = upd_age
            if upd_gender:
                actor.gender = upd_gender

            actor.update()

            return jsonify({
                'success': True,
                'updated_actor': actor.format()
            })
        except:
            abort(500)


#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
#     ___  ___ _____________ __    __               _
#    / _ \/ _ /_  __/ ___/ // /  _/_/_ _  ___ _  __(_)__ ___
#   / ___/ __ |/ / / /__/ _  / _/_//  ' \/ _ \ |/ / / -_|_-<
#  /_/  /_/ |_/_/  \___/_//_/ /_/ /_/_/_/\___/___/_/\__/___/

    '''
    @TODO endpoint PATCH /movies
        - roles that can access the endpoint:
            - Casting Director
            - Executive Producer
        - returns the movie that was modified
    '''
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movie(payload, id):
        body = request.get_json()

        if not body:
            abort(422)

        upd_title = body.get('title', None)
        upd_release_date = body.get('release_date', None)

        if upd_title is None and upd_release_date is None:
            abort(400)

        movie = Movie.query.filter_by(id=id).one_or_none()

        if movie is None:
            abort(404)

        try:
            if upd_title:
                movie.title = upd_title
            if upd_release_date:
                movie.release_date = upd_release_date

            movie.update()

            return jsonify({
                'success': True,
                'updated_movie': movie.format()
            })
        except:
            abort(500)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#    ___                   _  _              _ _ _
#   | __|_ _ _ _ ___ _ _  | || |__ _ _ _  __| | (_)_ _  __ _
#   | _|| '_| '_/ _ \ '_| | __ / _` | ' \/ _` | | | ' \/ _` |
#   |___|_| |_| \___/_|   |_||_\__,_|_||_\__,_|_|_|_||_\__, |
#                                                      |___/
    '''
    Errors: 400, 404, 405, 409, 422, 500
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method Not Allowed'
        }), 405

    @app.errorhandler(409)
    def conflict(error):
        return jsonify({
            'success': False,
            'error': 409,
            'message': 'Conflict. Already Exists'
        }), 409

    @app.errorhandler(422)
    def unprocassable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    @app.errorhandler(AuthError)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#      _               _                      _
#     /_\  _ __ _ __  | |   __ _ _  _ _ _  __| |_
#    / _ \| '_ \ '_ \ | |__/ _` | || | ' \/ _| ' \
#   /_/ \_\ .__/ .__/ |____\__,_|\_,_|_||_\__|_||_|
#         |_|  |_|

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
