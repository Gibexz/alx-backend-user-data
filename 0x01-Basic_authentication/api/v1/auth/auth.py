#!/usr/bin/env python3
"""
module: auth.py
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """
    class to manage the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        not implemented yet
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        not implemented yet
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        not implemented yet
        """
        return None
