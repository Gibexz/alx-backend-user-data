#!/usr/bin/env python3
"""
module: session_exp_auth.py
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """
    add an expiration date to a Session ID.
    """
    def __init__(self):
        """
        Initializes a new SessionExpAuth instance
        """
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        session creator method
        """
        session_id = super().create_session(user_id=user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user id of the user associated with
        a given session id
        """
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if not session_dict:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        exp_time = created_at + timedelta(seconds=self.session_duration)

        if exp_time < datetime.now():
            return None

        return session_dict['user_id']
