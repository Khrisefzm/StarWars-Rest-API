"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Vehicles, Planets, Favorites

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people')
def get_people():
    people = People.query.all()
    return jsonify([person.serialize() for person in people]), 200

#in case the api require to create new people:
@app.route('/people', methods=['POST'])
def create_person():
    data = request.json
    new_person = People(
            name=data.get("name"),
            height=data.get("height"),
            mass=data.get("mass"),
            hair_color=data.get("hair_color"),
            skin_color=data.get("skin_color"),
            eyes_color=data.get("eyes_color"),
            birth_year=data.get("birth_year"),
            gender=data.get("gender"),
        )
    db.session.add(new_person)
    db.session.commit()
    return jsonify(new_person.serialize()), 200

@app.route('/people/<int:person_id>')
def get_single_person(person_id):
    person = People.query.get(person_id)
    return jsonify(person.serialize()), 200

@app.route('/vehicles')
def get_vehicles():
    vehicles = Vehicles.query.all()
    return jsonify([vehicle.serialize() for vehicle in vehicles]), 200

@app.route('/vehicles/<int:vehicle_id>')
def get_single_vehicle(vehicle_id):
    vehicle = Vehicles.query.get(vehicle_id)
    return jsonify(vehicle.serialize()), 200

@app.route('/planets')
def get_planets():
    planets = Planets.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets/<int:planet_id>')
def get_single_planet(planet_id):
    planet = Planets.query.get(planet_id)
    return jsonify(planet.serialize()), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/users/<int:user_id>')
def get_single_user(user_id):
    user = User.query.get(user_id)
    return jsonify(user.serialize()), 200

@app.route('/users/<int:user_id>/favorites')
def get_favorites():
    favorites = Favorites.query.all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200

@app.route('/users/<int:user_id>/favorites/people/<int:person_id>', methods=['POST', 'DELETE'])
def post_or_delete_favorite_person(person_id):
    if request.method == 'POST':
        favorite = Favorites(people_id=person_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify(favorite.serialize()), 200
    else:
        favorite = Favorites.query.get(person_id)
        if favorite is None:
            raise APIException('User not found', status_code=404)
        db.session.delete(favorite)
        db.session.commit()
        return jsonify(favorite.serialize()), 200

@app.route('/users/<int:user_id>/favorites/vehicles/<int:vehicle_id>', methods=['POST', 'DELETE'])
def post_or_delete_favorite_vehicle(vehicle_id):
    if request.method == 'POST':
        favorite = Favorites(vehicles_id=vehicle_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify(favorite.serialize()), 200
    else:
        favorite = Favorites.query.get(vehicle_id)
        if favorite is None:
            raise APIException('User not found', status_code=404)
        db.session.delete(favorite)
        db.session.commit()
        return jsonify(favorite.serialize()), 200

@app.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['POST', 'DELETE'])
def post_or_delete_favorite_planet(planet_id):
    if request.method == 'POST':
        favorite = Favorites(planets_id=planet_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify(favorite.serialize()), 200
    else:
        favorite = Favorites.query.get(planet_id)
        if favorite is None:
            raise APIException('User not found', status_code=404)
        db.session.delete(favorite)
        db.session.commit()
        return jsonify(favorite.serialize()), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
