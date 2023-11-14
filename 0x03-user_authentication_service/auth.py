#!/usr/bin/env python3
"""
module: auth.py
"""
import bcrypt
from db import DB
from typing import TypeVar
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(rawPassword: str) -> str:
    """
    takes in a password string arguments and returns bytes.
    """
    hasedPass = bcrypt.hashpw(rawPassword.encode('utf-8'), bcrypt.gensalt())

    return hasedPass


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ initialization method for the class """
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """Registers a new user"""
        try:
            if self._db.find_user_by(email=email) is not None:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            pass

        hashPassword = _hash_password(password)
        newuser = self._db.add_user(email, hashPassword)
        return newuser
