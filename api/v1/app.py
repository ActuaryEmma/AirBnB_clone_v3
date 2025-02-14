#!/usr/bin/python3
"""
declare method storage.close
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
import os


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def destroy(obj):
    """destroy an obj"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """return 404"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
