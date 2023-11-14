#!/usr/bin/env python3
"""
module: app.py: basic Flask c
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, make_response, redirect


AUTH = Auth()
app = Flask(__name__)


@app.route("/")
def home():
    """home route for the app"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"], strict_slashes=False)
def users():
    """
    a route to register new users
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except Exception as e:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login():
    """
    session login after aunthentication
    """
    email = request.form.get("email")
    password = request.form.get("password")

    # try:
    if AUTH.valid_login(email=email, password=password):
        newSessionID = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", newSessionID)
        return response
    else:
        abort(401)
    # except Exception:
    #     abort(401)


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout():
    """destroy the session and redirect the user to GET th home "/" route"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        response = redirect("/")
        response.set_cookie(session_id, '', expires=0) # 0: expires in 0 seconds
        return response
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
