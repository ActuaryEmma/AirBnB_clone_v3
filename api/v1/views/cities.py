#!/usr/bin/python3
"""Create a new view for State objects that handles all default RESTFul API"""
from models.city import City
from models.state import State
from flask import Flask, jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def get_cities(state_id):
    """return list of all cities"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_list = []
    for city in state.cities:
        city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """ get city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ delete city by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """create a city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    else:
        item_name = data.get("name")
        if not item_name:
            return make_response(jsonify({"error": "Missing name"}), 400)
        new_city = City(**data)
        new_city.state_id = state.id
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def update_city(city_id):
    """update name of the city"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['state_id', 'id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()

    return jsonify(obj.to_dict())
