import os
import pymongo
import logging

from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()
CONNECTION_STRING = os.environ.get("COSMOS_CONNECTION_STRING")


class User:
    """Class for representing all users, it has DB connection as well
    """

    def __init__(self, email : str = "", password : str = ""):
        self.email = email
        self.password = password
        self.admin : bool = False #We have to prevent argument injection

        self.client = pymongo.MongoClient(CONNECTION_STRING)
        db = self.client[r"team13-database"]
        self.users = db[r"Users"]
        for prop, value in vars(self.client.options).items():
            print("Property: {}: Value: {} ".format(prop, value))

    def add(self) -> bool:
        """Will try to add user to the databse with hashed password

        Returns:
            bool: if user was added succesfully True else False
        """
        if(self.email == ""):
            return False
        if not self.users.find_one({"email" : self.email}):
            user = {"email" : self.email, "password" : self.password, "admin" : self.admin}
            self.users.insert_one(user)
            logger.info("Adding user")
            return True
        logger.info("Email already exists")
        return False

    def get_all(self):
        """Will return all users present in DB

        Returns:
            _type_: _description_
        """
        all_users = self.users.find().sort("email")
        return all_users

    def get_one(self):
        first_user = self.users.find_one()
        print(first_user)
        return first_user

    def get_user(self, email):
        """Will return desired user per email

        Args:
            email (_type_): email of user to return

        Returns:
            _type_: _description_
        """
        #print(f"id is: {id} type: {type(id)}")
        user = self.users.find_one({"email" : email})
        #print(f"found item = {item}")
        formated_user = dict(_id = user["_id"], email = user["email"])
        return formated_user

    def get_user_for_login(self, email):
        """Special method that will return raw user data for loging purposes

        Args:
            email (_type_): _description_

        Returns:
            _type_: _description_
        """
        #print(f"id is: {id} type: {type(id)}")
        user = self.users.find_one({"email" : email})
        #print(f"found item = {item}")
        return user

    def is_admin(self, email) -> bool:
        user = self.users.find_one({"email" : email})
        return user["admin"]

    def delete_user(self, user_email) -> bool:
        """Delets user with given username.

        Args:
            id (_type_): id of the item
            user (_type_): current user

        Returns:
            bool: if exists and was deleted return true, else false
        """
        user = self.users.find_one({"email" : user_email})
        if not user:
            return False

        self.users.delete_one({"email" : user_email})
        return True

    def serialize(self):
        #information hiding
        serialized : dict = {"email" : self.email}
        return serialized

    def __del__(self):
        self.client.close()