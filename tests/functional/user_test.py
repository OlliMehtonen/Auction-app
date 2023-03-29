import pytest
import json
from flask import Flask
from flask_restful import Api
from tjts5901.backend.models.users import User


def test_new_user():
    user = User('tester@test.com', 'test123')
    assert user.email == 'tester@test.com'
    assert user.password == 'test123'
    assert user.admin is False

def test_db_add():
    user = User('pytest0@test.com', 'test123')
    user.add()
    assert user.email == "pytest0@test.com"
    
def test_get_all_users():
    user = User()
    users = user.get_all()
    users_from_db = [item_from_db for item_from_db in users]
    assert isinstance(users_from_db, list)

def test_is_admin():
    user = User()
    assert user.is_admin("pytest0@test.com") is False

def test_get_user():
    user = User()
    recived_user = user.get_user("pytest0@test.com")
    assert isinstance(recived_user, dict)
    assert recived_user['email'] == "pytest0@test.com"

def test_user_delete():
    user = User()
    user_deleted = user.delete_user("pytest0@test.com")
    assert user_deleted is True