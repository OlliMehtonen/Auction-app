import json
import logging

from flask import request
from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import (jwt_required, get_jwt_identity)

import tjts5901.backend.models.users as reg_user
import tjts5901.backend.login_api as log_in

#For testing I was using reqbin better then postman!

ITEM_ENDPOINT : str = r"/auction_item"
logger = logging.getLogger(__name__)

class Register(Resource):
    """Auction item class used to represent resource, and create GET, POST calls

    Args:
        Resource (_type_): _description_
    """
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help="Email is required!")
    parser.add_argument('password', type=str, required=True, help="Password is requried!")

    def get(self):
        """Register route for new users

        Returns:
            _type_: if user already exists 401, else 201, in case email or password is not provided 400
        """
        print(request.args)
        email = request.args.get('email')
        password = request.args.get('password')

        if not email or not password:
            abort(400, message="Both email and password are required!")
        if '@' not in email:
            abort(400, message="Invalid email address")
        hased_user = log_in.UserLogin(email, password)
        user = reg_user.User(hased_user.username, hased_user.password)
        if(user.add()):
            return {'message' : 'User registerd sucessfuly'}, 201
        return {'message' : 'email is already in use'}, 401 


    def post(self):
        
        data = Register.parser.parse_args()
        email = data['email']
        password = data['password']
        
        if '@' not in email:
            #abort(400, message="Invalid email address")
            return{"message" : "Invalid email"}, 400
        hased_user = log_in.UserLogin(email, password)
        user = reg_user.User(hased_user.username, hased_user.password)
        if(user.add()):
            return {'message' : 'User registerd sucessfuly'}, 201
        return {'message' : 'email is already in use'}, 401 