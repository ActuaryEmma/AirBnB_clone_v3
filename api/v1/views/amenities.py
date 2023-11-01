#!/usr/bin/python3
"""this file has the amenety module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """ get list of all amenities """
    amenities = storage.all(Amenity).values()
    all_list = []
    for amenity in amenities:
        all_list.append(amenity.to_dict())
    return jsonify(all_list)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ get amenity by id"""
    amenities = storage.all(Amenity).values()
    if not amenities:
        abort(404)
    for amenity in amenities:
        if amenity.id == amenity_id:
            return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """ delete amenity by id"""
    amenities = storage.all(Amenity).values()
    if not amenities:
        abort(404)
    for amenity in amenities:
        if amenity.id == amenity_id:
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200


@app_views.route("/amenities/", methods=['POST'],
                 strict_slashes=False)
def create_obj_amenity():
    """ create new instance """
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    else:
        item_name = data.get("name")
        if not item_name:
            return make_response(jsonify({"error": "Missing name"}), 400)
        new_amenity = Amenity(**data)
        storage.new(new_amenity)
        storage.save()
        return (jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """update amenity"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
