from app import app
from flask import jsonify

@app.errorhandler(404)
def endpoint_not_found(error):
    return jsonify({"message": "Endpoint not found"}), 404