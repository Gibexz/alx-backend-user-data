#!/usr/bin/env python3
"""
module basic_auth.py
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """
    Basic Authentication implementation
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        returns the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        returns the decoded value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_header_bytes = base64.b64decode(
                base64_authorization_header)
            return decoded_header_bytes.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
         returns the user email and
         password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" in decoded_base64_authorization_header:
            email, password = decoded_base64_authorization_header.split(":", 1)
            return email, password
        else:
            return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        returns the User instance based on his email and password
        """
        if not (user_email and isinstance(user_email, str) and
                user_pwd and isinstance(user_pwd, str)):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads Auth and retrieves the User instance for a request
        i.e. gets the instance of the current user
        """
        try:
            auth_header = self.authorization_header(request)
            encoding = self.extract_base64_authorization_header(auth_header)
            decoding = self.decode_base64_authorization_header(encoding)
            email, password = self.extract_user_credentials(decoding)
            user = self.user_object_from_credentials(email, password)
            return user
        except Exception:
            return None
