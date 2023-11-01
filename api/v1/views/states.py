#!/usr/bin/python3
"""Create a new view for State objects that handles all default RESTFul API"""
from models.state import State
from flask import Flask, jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage


@app_views.route("/states", strict_slashes=False)
def get_states():
    """return list of all states"""
    states = storage.all("State").values()
    state_list = []
    for state in states:
        state_list.append(state.to_dict())
    return jsonify(state_list)


@app_views.route("/states/<state_id>", strict_slashes=False)
def get_states_id(state_id):
    """return one state based on the id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """delete a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def post_state():
    """create a state"""
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    else:
        item_name = data.get("name")
        if not item_name:
            return make_response(jsonify({"error": "Missing name"}), 400)
        new_state = State(**data)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """ update method """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()

    return jsonify(obj.to_dict())
