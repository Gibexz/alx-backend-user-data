#!/usr/bin/env python3
"""
module: auth.py
"""
from flask import request
from os import getenv
from typing import List, TypeVar


class Auth():
    """
    class to manage the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        not implemented yet
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path:
            if path[-1] == '/':
                path == path
            else:
                path = path + '/'
        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """
        not implemented yet
        """
        if request:
            if "Authorization" in request.headers:
                return request.headers["Authorization"]
            return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        not implemented yet
        """
        return None

    def session_cookie(self, request=None):
        """
        returns a cookie value from a request
        
        Please_NOTE::: cookie_value = session_id
        """
        if request is None:
            return None
        cookie_name = getenv('SESSION_NAME')
        cookie_value = request.cookies.get(cookie_name)
        return cookie_value
