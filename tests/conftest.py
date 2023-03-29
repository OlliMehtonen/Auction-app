"""Module for testing."""
from typing import Any
from flask import Flask
from os import environ
import pytest
from tjts5901 import create_app
from flask_restful import Resource, Api, reqparse, abort
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity)

import tjts5901.backend.item_api as items
import tjts5901.backend.admin_api as admin_api
import tjts5901.backend.login_api as log_in
import tjts5901.backend.bid_api as bid

def pytest_addoption(parser: pytest.Parser):
    """
    Callback to add command-line options for pytest.

    Add option to define environment url to test.

    Usage example from agruments::
        $ pytest --environment-url "https://example.com"

    Note: GitLab CI automatically sets environment variable `CI_ENVIRONMENT_URL`
    to the address of environment to test.

    Usage example from environment variable::
        $ CI_ENVIRONMENT_URL="https://example.com" pytest

    Note: If you want to test locally, you can define environment variable in
    .env file.
    """

    parser.addoption("--environment-url",
                     dest="CI_ENVIRONMENT_URL",
                     help="Deployment webaddress",
                     default=environ.get("CI_ENVIRONMENT_URL"))


@pytest.fixture
def app() -> Flask:
    """
    Application fixture.

    Every test that requires `app` as parameter can use this fixture.

    Example:
    >>> def test_mytest(app: Flask):
    >>>     ...
    """
    flask_app = create_app({
        'TESTING': True,
        'DEBUG': False,

        # We need to set SERVER_NAME and PREFERRED_URL_SCHEME for testing.
        'SERVER_NAME': 'localhost.localdomain',
        'PREFERRED_URL_SCHEME': 'http',
    })

    # If you have done ties4080 course and have used Flask-WTF, you might
    # have noticed that CSRF protection is enabled by default. This is
    # problematic for testing, because we don't have a browser to generate
    # CSRF tokens. We can disable CSRF protection for testing, but we need
    # to make sure that we don't have CSRF protection enabled in production.

    # _app.config['WTF_CSRF_ENABLED'] = False
    # _app.config['WTF_CSRF_METHODS'] = []
    # _app.config['WTF_CSRF_CHECK_DEFAULT'] = False

    api = Api(flask_app)
    #create JSON web token bearer
    jwt = JWTManager(flask_app)

    # added auction item resource
    api.add_resource(items.AuctionItem, "/auction_item/", "/auction_item/<id>")
    api.add_resource(admin_api.AdminAPI, "/users/", "/users/<email>")
    api.add_resource(bid.Bid, "/bid")
    flask_app.testing = True
    yield flask_app

@pytest.fixture
def client(app) -> Any:
    return app.test_client()

#coverage run -m pytest