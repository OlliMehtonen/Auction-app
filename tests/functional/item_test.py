import pytest
import json
from flask import Flask
from flask_restful import Api
from tjts5901.backend.models.items import Item


def test_new_user():
    item = Item('flask_test', 'testing', 'in flask', '123test', 7.7, "pytest@test.com")
    assert item.name == 'flask_test'
    assert item.category == 'testing'
    assert item.subcategory == 'in flask'
    assert item.description == '123test'
    assert item.owned_by == "pytest@test.com"
    assert item.starting_price == 7.7
    assert item.highest_bid_price == 0.0
    assert item.highest_bidder == ''
    assert item.is_expired is False

def test_serialize():
    item = Item()
    assert isinstance(item.serialize(), dict)
'''
def test_db_add():
    item = Item('flask_test', 'testing', 'in flask', '123test', 7.7, "pytest@test.com")
    item.add()
    assert item.owned_by == "pytest@test.com"
    
def test_get_user_item():
    item = Item()
    user_item = item.get_user_items("pytest@test.com")
    item_from_db = [item_from_db for item_from_db in user_item]
    first_item = item_from_db[0]
    assert isinstance(item_from_db, list)
    assert first_item['name'] == 'flask_test'
    assert first_item['category'] == 'testing'
    assert first_item['subcategory'] == 'in flask'
    assert first_item['description'] == '123test'
    assert first_item['starting_price'] == 7.7
    assert first_item['owned_by'] == 'pytest@test.com'

def test_bid():
    item = Item()
    user_item = item.get_user_items("pytest@test.com")
    item_from_db = [item_from_db for item_from_db in user_item]
    first_item = item_from_db[0]
    item.set_bider(first_item["_id"], 10, "pytest@test.com")
    assert isinstance(item_from_db, list)

def test_my_bids():
    item = Item()
    user_item = json.loads(item.get_my_bids("pytest@test.com"))
    first_item = user_item['ongoing'][0]
    assert isinstance(user_item, dict)
    assert first_item['highest_bidder'] == "pytest@test.com"
    assert first_item['highest_bid_price'] == 10.0

def test_db_delete():
    item = Item()
    user_item = item.get_user_items("pytest@test.com")
    item_from_db = [item_from_db for item_from_db in user_item]
    first_item = item_from_db[0]
    delete = item.delete_item(id=first_item['_id'], user_mail="pytest@test.com")
    assert delete is True
'''