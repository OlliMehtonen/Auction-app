"""
Flask Application
=================

This is the default entrypoint for our application.
Flask tutorial: https://flask.palletsprojects.com/en/2.2.x/tutorial/

"""

import logging
from os import environ
import os
import sentry_sdk
from typing import Dict, Literal, Optional

from flask_babel import _
from .i18n import init_babel


from dotenv import load_dotenv
from flask import (
    Flask,
    jsonify,
    Response,
    request,
    render_template,
    redirect,
    make_response,
    url_for,
    session

)

from sentry_sdk.integrations.flask import FlaskIntegration
from flask_restful import Resource, Api, reqparse, abort
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity)


#login info handling decorators
from tjts5901.backend.logincookies import logged_in, admin_logged_in, login_with_user, admin_with_user, logout_all

#item api class
import tjts5901.backend.item_api as items
import tjts5901.backend.admin_api as admin_api
import tjts5901.backend.login_api as log_in
import tjts5901.backend.bid_api as bid
import tjts5901.backend.register_api as register_api

import tjts5901.backend.models.users as reg_user

from .utils import get_version
#from .db import init_db
from . import views  # pylint: disable=import-outside-toplevel

logger = logging.getLogger(__name__)

# Register blueprints


def create_app(config: Optional[Dict] = None) -> Flask:
    """
    Application factory for creating a new Flask instance.

    :param name: The name of the application.
    """


    flask_app = Flask(__name__, instance_relative_config=True, static_folder='./frontend')
    

    #Change of static folder location above

    flask_app.config.from_mapping(
        SECRET_KEY='dev',
        BRAND=_("13th auction app"),
    )
    flask_app.register_blueprint(views.bp, url_prefix='')

    # load the instance config, if it exists, when not testing
    if config is None:
        flask_app.config.from_pyfile('config.py', silent=True)
    else:
        flask_app.config.from_mapping(config)


    # Initialize logging early, so that we can log the rest of the initialization.
    from .logging import init_logging  # pylint: disable=import-outside-toplevel
    init_logging(flask_app)

    # ensure the instance folder exists
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass
    
    # Initialize the Flask-Babel extension.
    init_babel(flask_app)

    # Initialize the database connection.
    #init_db(flask_app)

    #@flask_app.route('/debug-sentry')
    #def trigger_error():
    #    division_by_zero = 1 / 0

    # a simple page that says hello
    @flask_app.route('/hello')
    def hello():
        return _('Hello, World!')

    #from . import auth
    #flask_app.register_blueprint(auth.bp)

    #from . import items
    #flask_app.register_blueprint(items.bp)
    #flask_app.add_url_rule('/', endpoint='index')

    #Ensure the flask jwt token location has cookies

    return flask_app


# Load environment variables from .env file, if present. See the `dotenv` file for a
# template and how to use it.
load_dotenv()

sentry_sdk.init(
    dsn="https://2eaf6ba1a9ef42d89c9d5e660d3c5f19@o1104883.ingest.sentry.io/4504668957900800",
    integrations=[
        FlaskIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

# Create the Flask application.
flask_app = create_app()
# Addad time till token expires from 10 min to 2 hours
flask_app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 7200
# create flast restapi
api = Api(flask_app)
#create JSON web token bearer
jwt = JWTManager(flask_app)




# added auction item resource
api.add_resource(items.AuctionItem, "/auction_item/", "/auction_item/<id>")
api.add_resource(admin_api.AdminAPI, "/users/", "/users/<email>")
api.add_resource(bid.Bid, "/bid")
api.add_resource(register_api.Register, "/register")

@flask_app.route('/debug-sentry')
def trigger_error():
    try:
        division_by_zero = 1 / 0
    except Exception as er:
        return {"Error" : er}, 400


@flask_app.route("/server-info")
def server_info() -> Response:
    """
    A simple endpoint for checking the status of the server.

    This is useful for monitoring the server, and for checking that the server is
    running correctly.
    """

    # Test for database connection
    database_ping = False
    try:
        from .db import db  # pylint: disable=import-outside-toplevel
        database_ping = db.connection.admin.command('ping').get("ok", False) #and True
    except Exception as exc:  # pylint: disable=broad-except
        logger.warning("Error querying mongodb server: %r", exc,
                       exc_info=True,
                       extra=flask_app.config.get_namespace("MONGODB"))

    # Check for sentry
    sentry_available = False
    try:
        from sentry_sdk import Hub
        sentry_available = True if Hub.current.client else False
    except ImportError:
        logger.warning("Sentry package is not installed")
    except TypeError:
        logger.info("Sentry is not integrated")

    response = {
        "database_connectable": database_ping,
        'sentry_available': sentry_available,
        "version": get_version(),
        "build_date": environ.get("BUILD_DATE", None)
    }

    # Response with pong if ping is provided.
    ping = request.args.get("ping", None)
    if ping is not None:
        response["pong"] = f"{ping}"

    return jsonify(response)

@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    """Login route for users

    Returns:
        _type_: 401 in case email or password is not matching, else 200
    """
    # Get the username and password from the request
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        save_as_cookie = request.form.get('to_cookie', True)
    elif request.method == 'GET':
        email = request.args.get('email')
        password = request.args.get('password')
        save_as_cookie = False

    # Authenticate the user
    user = log_in.UserLogin.authenticate(email, password)
    if not user:
        return {'message': 'Invalid email or password'}, 401
    
    #Save data to session
    if save_as_cookie:
        login_with_user(user['email'])
    # Generate a JWT access token
    access_token = create_access_token(identity=user["email"])
    return {'access_token': access_token}, 200


@flask_app.route('/adminlogin', methods=['POST'])
def admin_login():
    """Admin login route for users

    Returns:
        _type_: 401 in case email or password is not matching, else 200
    """
    # Get the username and password from the request
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

    #if not email or not password:
    #    abort(400, message="Both email and password are required!")

    # Authenticate the user

    user = log_in.UserLogin.authenticate(email, password)
    if not user or not password:
        return {'message': 'Invalid email or password'}, 401
    
    #Save data to session
    admin_with_user(user['email'])
    # Generate a JWT access token
    access_token = create_access_token(identity=user["email"])
    return {'access_token': access_token}, 200

@flask_app.route('/protected')
@jwt_required()
def protected():
    """Just a test route

    Returns:
        str: formatted output
    """
    # Access the identity of the current user from the JWT
    current_user = get_jwt_identity()
    return {'message': 'Hello, {}!'.format(current_user)}


@flask_app.route('/login_page', methods=['GET'])
def login_page():
    """View for logging in

    Returns:
        Login page in case of authentication failure and redirect to main page if authenticated.
    """
    return render_template('login.html', login_fail=False)

@flask_app.route('/reg')
def reg_page():
    """
    View for registering new users.
    """
    return render_template('auth/register.html')

@flask_app.route('/alpage')
def admin_login_page():
    return render_template('alogin.html', login_fail=False)

@flask_app.route('/logout')
def logout():
    logout_all()
    return redirect(url_for('login_page'))






