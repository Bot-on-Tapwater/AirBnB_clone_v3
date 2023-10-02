#!/usr/bin/python3

"""this is a script that serves a flask app"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

# instance of Flask
app = Flask(__name__)

app.register_blueprint(app_views)

cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def cleanup_app_context(arg):
    """Remove SQLAlchemy  Session"""
    # print("removing session")
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """404 Not found"""
    data = {
        "error": "Not found"
    }

    return jsonify(data), 404


@app.errorhandler(400)
def bad_request(e):
    """400 Bad request"""
    custom_message = str(e.description if e.description else "Bad Request")
    return jsonify(custom_message), 400


if __name__ == '__main__':
    # assign host and post values
    host = "0.0.0.0"
    port = 5000

    if "HBNB_API_HOST" in os.environ:
        host = os.environ.get("HBNB_API_HOST")
    if "HBNB_API_PORT" in os.environ:
        port = int(os.environ.get("HBNB_API_PORT"))
    # run flask app
    app.run(host=host, port=port, threaded=True)
