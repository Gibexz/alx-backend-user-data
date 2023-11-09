#!/usr/bin/env python3
"""
module: session_auth.py
"""
from api.v1.auth.auth import Auth
from api.v1.views import app_views
from models.user import User
from flask import request, jsonify, abort
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def user_session_view():
    """
    handles all routes for the Session authentication
    - returns JSON representation of a User object
    """
    email = request.form.get('email')
    if not email or email == "":
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password or password == "":
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404

    if users[0].is_valid_password(password):
        from api.v1.app import auth
        session_ID = auth.create_session(users[0].id)
        user_dict = users[0].to_json()
        session_cookie_name = getenv('SESSION_NAME')
        response = jsonify(user_dict)
        response.set_cookie(session_cookie_name, session_ID)
        return response
    return jsonify({"error": "wrong password"}), 401


@app_views.route(
        '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def user_session_logout():
    """
    logs_out/deletes a session
    """
    from api.v1.app import auth
    logout = auth.destroy_session(request)
    if not logout:
        abort(404)
    return jsonify({}), 200
