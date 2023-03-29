import pytest
import json
import requests
from flask import Flask

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,)

def test_hello(client):
    with client.application.app_context():
        resp = client.get("/hello")
        assert resp.status_code == 200

def test_get_all_items(client):
    """Test getting all items

    Args:
        client (_type_): _description_
    """
    with client.application.app_context():
        #jwt = JWTManager(client.application)
        access_token= create_access_token(identity="jozko@test.com")
        bearer_str = r"Bearer " + access_token
        
        #headers["Authorization"] = "Bearer "
        
        headers = {
            "Authorization": bearer_str
        }

        response = client.get("/auction_item/", headers=headers)
        assert response.status_code == 200
        assert isinstance(json.loads(response.data), str)

def test_get_my_auctions(client):
    """Test getting specific user with email: jozko@test.com

    Args:
        client (_type_): _description_
    """
    with client.application.app_context():
        #jwt = JWTManager(client.application)
        access_token= create_access_token(identity="jozko@test.com")
        bearer_str = r"Bearer " + access_token
        
        #headers["Authorization"] = "Bearer "
        
        headers = {
            "Authorization": bearer_str
        }

        response = client.get("/auction_item/my", headers=headers)
        assert response.status_code == 200
        assert isinstance(json.loads(response.data), str)

def test_get_my_bids(client):
    """Test getting items taht user: jozko@test.com had bid on

    Args:
        client (_type_): _description_
    """
    with client.application.app_context():
        #jwt = JWTManager(client.application)
        access_token= create_access_token(identity="jozko@test.com")
        bearer_str = r"Bearer " + access_token
        
        #headers["Authorization"] = "Bearer "
        
        headers = {
            "Authorization": bearer_str
        }

        response = client.get("/auction_item/my_bids", headers=headers)
        assert response.status_code == 200
        assert isinstance(json.loads(response.data), str)

def test_get_all_users(client):
    """Test getting all users

    Args:
        client (_type_): _description_
    """
    with client.application.app_context():
        #jwt = JWTManager(client.application)
        access_token= create_access_token(identity="jozko@test.com")
        bearer_str = r"Bearer " + access_token
        
        #headers["Authorization"] = "Bearer "
        
        headers = {
            "Authorization": bearer_str
        }

        response = client.get("/users/", headers=headers)
        assert response.status_code == 200
        assert isinstance(json.loads(response.data), str)

@pytest.mark.skip(reason="Temporary skip for now")
def test_get_specific_user(client):
    """Test getting specific user with email: jozko@test.com

    Args:
        client (_type_): _description_
    """
    with client.application.app_context():
        #jwt = JWTManager(client.application)
        access_token= create_access_token(identity="jozko@test.com")
        bearer_str = r"Bearer " + access_token

        #headers["Authorization"] = "Bearer "
   
        headers = {
            "Authorization": bearer_str
        }

        response = client.get("/users/jozko@test.com", headers=headers)
        assert response.status_code == 200
        assert isinstance(json.loads(response.data), str)