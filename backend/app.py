from flask import Flask, jsonify
from flask_cors import CORS

from models import *

# --------------------------------------------------------------------------- #
# --------->                   Server Setup                        <--------- #
# --------------------------------------------------------------------------- #

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/test')
    def test():
        movies = Movie.query.all()
        actors = Actor.query.all()
        f_movies = [movie.format() for movie in movies]
        f_actors = [actor.format() for actor in actors]

        return jsonify({'movies': f_movies, 'actors': f_actors})

    return app


# --------------------------------------------------------------------------- #
# --------->                   Launching app                       <--------- #
# --------------------------------------------------------------------------- #

app = create_app()
if __name__ == '__main__':
    app.run()