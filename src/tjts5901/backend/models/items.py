import os
import logging
import pymongo
import json
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
CONNECTION_STRING = os.environ.get("COSMOS_CONNECTION_STRING")
logger = logging.getLogger(__name__)

class Item:
    """Class for representing the Auctioning item
    """
    def __init__(self, name : str = "", category : str = "", subcategory : str = "", description : str = "", starting_price : float = 0.0, owned_by : str = ""):
        self.name = name
        self.category = category
        self.subcategory = subcategory
        self.description = description
        self.starting_price = starting_price
        self.owned_by = owned_by
        self.highest_bid_price : float = 0.0
        self.highest_bidder : str = ""
        self.created_at = datetime.now()
        self.is_expired = False

        self.client = pymongo.MongoClient(CONNECTION_STRING)

        for prop, value in vars(self.client.options).items():
            print("Property: {}: Value: {} ".format(prop, value))

        db = self.client[r"team13-database"]
        self.users = db[r"Users"]
        self.items = db[r"Items"]

    def add(self):
        """method to add new item into a auction
        """
        #TODO: add checking and probably item history
        item = {"name" : self.name, "category" : self.category, "subcategory" : self.subcategory,
        "description" : self.description, "starting_price" : self.starting_price,
        "highest_bid_price" : self.highest_bid_price, "highest_bidder" : self.highest_bidder,
         "created_at" : self.created_at, "owned_by" : self.owned_by, "is_expired" : self.is_expired}
        self.items.insert_one(item)

    def get_one(self):
        """Test method to het first item that is in DB

        Returns:
            Item: First item form DB
        """
        first_item = self.items.find_one()
        return first_item
        
    def get_all(self):
        """Method to get all items form db

        Returns:
            List: List of dicts, representing items
        """
        self.update_expired_items()
        all_items = self.items.find({"is_expired" : {"$ne" : True}}).sort("name")
        return all_items

    def get_item(self, id):
        """method to get concrete item based on its id

        Args:
            id (str): id of and item

        Returns:
            dict: item represneted as dict
        """
        #print(f"id is: {id} type: {type(id)}")
        item = None
        try:
            item = self.items.find_one({"_id" : ObjectId(id)})
        except Exception as er:
            logging.error(er)
        #print(f"found item = {item}")
        return item

    def get_user_items(self, user_email : str):
        """Retrives all items owned by given user

        Args:
            user_email (str): email of current user

        Returns:
            list: empty list if user doesn't own any items
        """
        self.update_expired_items()
        all_items = self.items.find({"owned_by" : user_email}).sort("name") #, "is_expired" : {'$eq' : False}
        return all_items

    def get_my_bids(self, user_email : str):
        """Method will retrive all items user has bid on in two lists ongoing and finished

        Args:
            user_email (str): email of the current user

        Returns:
            dict: dictionary of lists of finished and ongoing items
        """
        self.update_expired_items()
        all_items = self.items.find({"highest_bidder" : user_email})
        ongoing : list = []
        expired : list = []
        for item in all_items:
            if item["is_expired"]:
                expired.append(item)
            else:
                ongoing.append(item)
        my_bids : dict = {"ongoing" : ongoing, "finished" : expired}
        #item_from_db = [item_from_db for item_from_db in query_result]
        temp = json.dumps(my_bids, default=str)
        return temp

    def update_expired_items(self):
        """Will check if any items are to be closed and if so it will mark them as expired
        """
        all_items = self.items.find({"is_expired" : {"$ne" : True}}).sort("name")
        item_from_db = [item_from_db for item_from_db in all_items]
        end_date = datetime.now()
        for item in item_from_db:
            creeated_at = item['created_at']
            end_date = creeated_at + timedelta(hours=24)
            #checks if auction is already going for 24 hours
            if end_date <= datetime.now():
                query_id = {"_id" : item['_id']}
                update_values = {"$set" : {"is_expired" : True}}
                self.items.update_one(query_id, update_values)
                self.send_mail()
                #print(f"\ndate is more then 24! query_id {query_id}")
        logger.info("Expiration times updated")

    def send_mail(self):
        pass

    def delete_item(self, id, user_mail) -> bool:
        """Delets item with given id, only if the user is admin or item is owned ny user.

        Args:
            id (_type_): id of the item
            user (_type_): current user

        Returns:
            bool: if user has privileges to delete item true, else false
        """
        user= self.users.find_one({"email" : user_mail})
        user_is_admin = user['admin']
        #print(f"\n user {user_is_admin}\n")
        if user_is_admin is True:
            logger.info("Admin is deleting item")
            self.items.delete_one({"_id" : ObjectId(id)})
            return True

        item = self.items.find_one({"_id" : ObjectId(id), "owned_by" : user['email']})
        if not item:
            return False
        self.items.delete_one({"_id" : ObjectId(id)})
        logger.info("Item deleted")
        return True

    def set_bider(self, item_id, new_bid ,new_highest_bider : str):
        """Will set new bidder for item

        Args:
            item_id (str): id of desired item
            new_bid (float): amount of bid
            new_highest_bider (str): current user that placed the bid
        """
        query = {"_id" : ObjectId(item_id)}
        new_val = {"$set" : {"highest_bidder" : new_highest_bider, "highest_bid_price" : new_bid}}
        self.items.update_one(query, new_val)

    def serialize(self):
        serialized : dict = {"name" : self.name, "category" : self.category, "subcategory" : self.subcategory,
        "description" : self.description, "starting_price" : self.starting_price, 
        "highest_bid_price" : self.highest_bid_price, "highest_bidder" : self.highest_bidder,
        "created_at" : self.created_at, "owned_by" : self.owned_by, "is_expired" : self.is_expired}
        return serialized

    def __del__(self):
        self.client.close()

class ItemNotFound(Exception):
    """Exception occurs when there is no item with given id in DB

    Args:
        Exception (_type_): _description_
    """
    
    def __init__(self):
        self.err_msg : str = r"Item with given id does not exist"

    def __str__(self):
        return self.err_msg