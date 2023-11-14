#!/usr/bin/env python3
"""
module: auth.py
"""
import bcrypt
from db import DB
from typing import TypeVar
from sqlalchemy.orm.exc import NoResultFound
from user import User
from uuid import uuid4


def _hash_password(rawPassword: str) -> bytes:
    """
    takes in a password string arguments and returns bytes.
    """
    hasedPass = bcrypt.hashpw(rawPassword.encode('utf-8'), bcrypt.gensalt())

    return hasedPass


def _generate_uuid() -> str:
    """uuid string generator"""
    return (uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ initialization method for the class """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user"""
        try:
            if self._db.find_user_by(email=email) is not None:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            pass

        hashPassword = _hash_password(password)
        newuser = self._db.add_user(email, hashPassword)
        return newuser

    def valid_login(self, email: str, password: str) -> bool:
        """ validates a user login details """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                if bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password):
                    return True
                else:
                    return False
        except Exception as e:
            return False

    def create_session(self, email: str) -> str:
        """session generator method"""
        try:
            user = self._db.find_user_by(email=email)
            # print (str(user))
            sessionID = str(_generate_uuid())
            # try using update_user form _db below if this fails.
            # self._db.update_user(user.id, session_id=sessionID)
            user.session_id = sessionID
            self._db._session.commit()
            return (sessionID)

        except Exception as e:
            return None
