import bcrypt

from flask_restful import Resource

import tjts5901.backend.models.users as users

class UserLogin(Resource):
    def __init__(self, username, password : str):
        #username will be email
        self.username = username
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    @classmethod
    def authenticate(cls, email : str, password : str):
        """Method for authenticating user based on comapriosn of hased passwords

        Args:
            email (str): email of the user
            password (str): plain text password

        Returns:
            User: if user was succesfuly authenticated object representing him is returned
        """
        # Check if the username and password match an existing user
        # Return the user object if found, else return None
        user = users.User(email, password).get_user_for_login(email)
        if not user:
            return None
        user_psw : str = user["password"]
        if user and bcrypt.checkpw((password.encode('utf-8')), user_psw):
            return user
        return None