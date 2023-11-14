#!/usr/bin/env python3
"""DB module : using sqlite with alchemy
"""
from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> TypeVar('user'):
        """
        method to create / add a new user
        """
        newUser = User(email=email, hashed_password=hashed_password)
        self._session.add(newUser)
        self._session.commit()

        return newUser

    def find_user_by(self, **kwargs):
        """
        method to find a user given som abitrary information as arguments
        """
        try:
            users = self._session.query(User).filter_by(**kwargs).all()
            if not users:
                raise NoResultFound
            return users[0]
        except InvalidRequestError as badRequest:
            raise badRequest

    def update_user(self, user_id: int, **kwargs: dict) -> None:
        """
        update a user based on its id
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, val in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, val)
            self._session.commit()

        except NoResultFound:
            pass
        except InvalidRequestError:
            pass
