#!/usr/bin/env python3
"""
module: app.py: basic Flask c
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/")
def home():
    """home route for the app"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
