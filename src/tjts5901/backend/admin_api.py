import json
import logging

from flask import request, jsonify
from flask_restful import Resource, abort

import tjts5901.backend.models.users as users
from flask_jwt_extended import (jwt_required, get_jwt_identity)

logger = logging.getLogger(__name__)

class AdminAPI (Resource):
    """Admin rest call interface

    Args:
        Resource (_type_): _description_
    """
    
    @jwt_required()
    def get(self, email = None):
        user = users.User()

        #current_user = get_jwt_identity()
        if not email:
            logger.info("retriving all users!")
            query_result = user.get_all()
            user_from_db = [user_from_db for user_from_db in query_result]
            temp = json.dumps(user_from_db, default=str)
            return temp
        
        logger.info(f"Trying to retrive a user with id: {id}")
        try:
            query_result = user.get_user(email)
            temp = json.dumps(query_result, default=str)
            return temp
        except Exception as err:
            abort(404, message = err)
    
    @jwt_required()
    def post(self):
        #TODO: connection with db
        data = request.get_json()
        user = users.User(**data)
        user.add()
        addad_user = json.dumps(user.serialize(), default=str)
        return {'status' : addad_user}, 201