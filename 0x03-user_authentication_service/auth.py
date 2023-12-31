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
from typing import Union, Optional


def _hash_password(rawPassword: str) -> bytes:
    """
    takes in a password string arguments and returns bytes.
    """
    hasedPass = bcrypt.hashpw(rawPassword.encode('utf-8'), bcrypt.gensalt())

    return hasedPass


def _generate_uuid() -> str:
    """uuid string generator"""
    return (str(uuid4()))


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

            sessionID = str(_generate_uuid())
            # you can also use update_user form _db below as shown below.
            # self._db.update_user(user.id, session_id=sessionID)
            user.session_id = sessionID
            self._db._session.commit()
            return (sessionID)

        except Exception as e:
            return None

    def get_user_from_session_id(self, session_id: str) -> User or None:
        """
        returns a User corresponding to the given session_id, or None
        """
        # if session_id is not None and session_id.strip():
        #     user = self._db.find_user_by(session_id=session_id)
        #     if user:
        #         return user
        #     return None
        # return None

        # same as  above
        if session_id is None:
            return None

        return self._db.find_user_by(session_id=session_id)

    def destroy_session(self, user_id: str) -> None:
        """
        destroys a session
        """
        if user_id:
            self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        generates a new password reset tooken for the user
        """
        user = self._db.find_user_by(email=email)
        if user:
            new_reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=new_reset_token)
            return new_reset_token

        else:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        updates a password using reset
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            new_hashedPassword = _hash_password(password)
            self._db.update_user(user.id,
                                 hashed_password=new_hashedPassword,
                                 reset_token=None)
            # you must not return None

        except Exception:
            raise ValueError
