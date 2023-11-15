#!/usr/bin/env python3
"""
Module: main.py
"""

import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """mmm mmm mmm"""
    url = f"{BASE_URL}/users"
    payload = {"email": email, "password": password}
    response = requests.post(url, payload)
    # print(response.status_code)
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """mmm mmm mmm"""
    url = f"{BASE_URL}/sessions"
    payload = {"email": email, "password": password}
    response = requests.post(url, payload)
    assert response.status_code == 401


def profile_unlogged() -> None:
    """ mmm mmm mmm """
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403


def log_in(email: str, password: str) -> str:
    """mmm mmm mmm"""
    url = f"{BASE_URL}/sessions"
    payload = {"email": email, "password": password}
    response = requests.post(url, payload)
    # print(response.status_code)
    assert response.status_code == 200
    # print(response.cookies.get("session_id"))
    # print (response.status_code)
    session_id = response.cookies.get("session_id")
    return session_id


def profile_logged(session_id: str) -> None:
    """mmm mmm mmm"""
    url = f"{BASE_URL}/profile"
    headers = {"Cookie": f"session_id={session_id}"}
    response = requests.get(url, headers=headers)
    # print (session_id)
    # print (response.status_code)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """mmm mmm mmm"""
    url = f"{BASE_URL}/sessions"
    headers = {"Cookies": f"session_id={session_id}"}
    response = requests.delete(url, headers=headers)
    # print (session_id)
    # print (response.status_code)
    assert response.status_code in (
        200, 302, 403), f"Unexpected status code: {response.status_code}"


def reset_password_token(email: str) -> str:
    """mmm mmm mmm"""
    url = f"{BASE_URL}/reset_password"
    payload = {"email": email}
    response = requests.post(url, data=payload)
    # print(response.json().get("reset_token", ""))
    assert response.status_code == 200
    return response.json().get("reset_token")


def update_password(
        email: str, reset_token: str, new_password: str) -> None:
    """mmm mmm mmm"""
    url = f"{BASE_URL}/reset_password"
    payload = {
                "email": email,
                "reset_token": reset_token,
                "new_password": new_password
            }
    # print(reset_token)
    response = requests.put(url, data=payload)
    # print(response.json().get("message"))
    assert response.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
