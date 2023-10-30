#!/usr/bin/python3
"""Create a new view for State objects that handles all default RESTFul API"""
from models.state import State
from flask import Flask, jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from api.v1.app import not_found_error

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
    states = storage.all("State").values()
    for state in states:
        if state.id == state_id:
            return jsonify(state.to_dict())
    return not_found_error("error")


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["DELETE"])
def delete_state(state_id):
    """delete a state"""
    states = storage.all("State").values()
    for state in states:
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
    return not_found_error("error")


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
        response = {"name": item_name}
        return jsonify(response), 201



@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)

def update_state(state_id):
    """ update method """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(State, state_id)
    if obj is None:
        return not_found_error("error")
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()

    return jsonify(obj.to_dict())
