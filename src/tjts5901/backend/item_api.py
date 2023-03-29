import json
import logging

from flask import request
from bson import ObjectId
from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import (jwt_required, get_jwt_identity)

import tjts5901.backend.models.items as items
from tjts5901.backend.models.items import ItemNotFound

#For testing I was using reqbin better then postman!

ITEM_ENDPOINT : str = r"/auction_item"
logger = logging.getLogger(__name__)

class AuctionItem (Resource):
    """Auction item class used to represent resource, and create GET, POST calls

    Args:
        Resource (_type_): _description_
    """
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="Name is required!")
    parser.add_argument('category', type=str, required=True, help="Category is requried!")
    parser.add_argument('subcategory', type=str, required=True, help="Sub category is requried!")
    parser.add_argument('description', type=str, required=True, help="Description is requried!")
    parser.add_argument('starting_price', type=float, required=True, help="Expected sell price is requried!")

    @jwt_required(locations=['headers'])
    def get(self, id = None):
        """GET method that accepts various parameters, id, my, my_bids or None

        Args:
            id (str, optional): id for specif item, if it is not provided it will return all items. Defaults to None.

        Returns:
            json: json representation of item objects
        """
        #current_user = get_jwt_identity()
        item = items.Item()
        if not id:
            logger.info("retriving all items!")
            query_result = item.get_all()
            item_from_db = [item_from_db for item_from_db in query_result]
            temp = json.dumps(item_from_db, default=str)
            return temp
        
        if (id == "my"):
            logger.info("Fetching all items realted to the current user")
            current_user = get_jwt_identity()
            query_result = item.get_user_items(current_user)
            item_from_db = [item_from_db for item_from_db in query_result]
            temp = json.dumps(item_from_db, default=str)
            return temp

        if (id == "my_bids"):
            logger.info("Fetching items user has bid on")
            current_user = get_jwt_identity()
            return item.get_my_bids(current_user)

        if not ObjectId.is_valid(id):
            return {"message" : f"{id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"}, 400

        logger.info(f"Trying to retrive a item with id: {id}")
        try:
            query_result = item.get_item(id)
            if not query_result:
                return {"message" : "No such item with given id exists!"}, 400
            temp = json.dumps(query_result, default=str)
            return temp
        except ItemNotFound as err:
            abort(404, message = err)

    @jwt_required()
    def post(self):
        """Endpoint to post item if any of the Data are not provided it will result in failure

        Returns:
            _type_: _description_
        """
        
        current_user = get_jwt_identity()
        data = AuctionItem.parser.parse_args()
        name = data['name']
        categ = data['category']
        sub_cat = data['subcategory']
        description = data['description']
        starting_price = data['starting_price']
        if(starting_price < 0):
            return {"message" : "Starting price must be 0 or more!"}, 400
        item = items.Item(name, categ, sub_cat, description, starting_price, current_user)
        item.add()
        #json.dump
        #added_item = jsonify(item.serialize())
        added_item = json.dumps(item.serialize(), default=str)
        return {'data' : added_item}, 201
    
    @jwt_required()
    def delete(self, id = None):
        """Endpoint to delete auction item, only deletes the item that user owns or exists

        Args:
            id (_type_, optional): id of an item. Defaults to None.

        Returns:
            _type_: _description_
        """
        item = items.Item()
        current_user = get_jwt_identity()
        if not ObjectId.is_valid(id):
            return {"message" : f"{id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"}, 400
        if not id:
            return {"message" : "Item with given id doesn't exist"}, 400
        delete_item = item.delete_item(id, current_user)
        if not delete_item:
            return {"message" : "You don't own this item"}, 400
        return {"message" : "item succesfully deleted"}, 200
