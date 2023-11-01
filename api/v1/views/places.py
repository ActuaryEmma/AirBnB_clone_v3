#!/usr/bin/python3
"""
This file has the Place module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State


@app_views.route("cities/<city_id>/places",  methods=['GET'],
                 strict_slashes=False)
def list_places(city_id):
    """Retrive places associated with a specific city"""
    city = storage.get(City, city_id)
    print(city)
    if not city:
        abort(404)
    places_list = []
    for place in city.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>",  methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ get place by id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """ delete place by id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_obj_place(city_id):
    """ create new instance """
    city = storage.get(City, city_id)
    print(city)
    data = request.get_json()
    print(data)
    if not city:
        abort(404)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif 'user_id' not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    elif 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    else:
        user = storage.get(User, data['user_id'])
        if not user:
            abort(404)
        new_place = Place(**data)
        new_place.city_id = city.id
        new_place.save()
        return (jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ update by id """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
