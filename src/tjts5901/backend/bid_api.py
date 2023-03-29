import json
import logging

from flask import request
from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import (jwt_required, get_jwt_identity)

import tjts5901.backend.models.items as items
from tjts5901.backend.models.items import ItemNotFound

#For testing I was using reqbin better then postman!

BID_ENDPOINT : str = r"/bid/"
logger = logging.getLogger(__name__)

class Bid (Resource):
    """Auction item class used to represent resource, and create GET, POST calls

    Args:
        Resource (_type_): _description_
    """

    parser = reqparse.RequestParser()
    parser.add_argument('item_id', type=str, required=True, help="Item id is required!")
    parser.add_argument('bid_price', type=float, required=True, help="Bid price is requried!")

    @jwt_required()
    def post(self):
        """POST method for biding

        Returns:
            _type_: if user can bid status code will be 200, else 401 or 402
        """

        current_user = get_jwt_identity()
        data = Bid.parser.parse_args()
        temp = items.Item()
        item = temp.get_item(data['item_id'])

        if not item:
            abort(401, message = ItemNotFound)
        if data['bid_price'] <= item['highest_bid_price']:
            abort(402, message = "bid price must be higher then the current one")
        
        temp.set_bider(data['item_id'], data['bid_price'], current_user)

        return {'data' : "bid updated"}, 201