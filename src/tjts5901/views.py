"""
Basic views for Application
===========================
"""
import logging

from flask import Blueprint, render_template, send_from_directory, redirect, session

from flask_jwt_extended import (
   jwt_required,
   get_jwt_identity)

#login info handling decorators
from tjts5901.backend.logincookies import logged_in, admin_logged_in, get_user_id, get_admin_id
from tjts5901.backend.models.items import Item, ItemNotFound

#Get item data from db
import tjts5901.backend.item_api as items

logger = logging.getLogger(__name__)

# Main blueprint.
bp = Blueprint('views', __name__)

# Blueprint for documentation.
docs_bp = Blueprint('docs', __name__)


@bp.route("/")
@logged_in
def main_page() -> str:
    """
    Index page.

    """

    # Render template file. Template file is using Jinja2 syntax,
    # and can be passed an arbitrary number
    # of arguments to be used in the template. The template file is located in
    # the templates directory.
    html = render_template("index.html.j2", title="TJTS5901 Example.")
    return html

@bp.route("/auction/<item_id>")
@logged_in
def bidding(item_id) -> str:
    """
    Page for making bids and seeing the auction status and deleting it if rights suffice.
    item_id is the id of item viewed.
    """

    #Get requested auction data
    a = backend_get(item_id)
    print("Item found", a)
    if a == None:
        #redirect if item not found
        return redirect('/')
    else:
        #owner and admin and others see different parts of the item auction template.
        is_owner = get_user_id() == a['owned_by']
        is_admin = get_admin_id() != None
        return render_template("auction.html", auc = a , is_owner=is_owner, is_admin = is_admin)


@bp.route("/termsetcond")
def terms():
    """
    View function to see terms and conditions of the service.
    Maybe more precise terms would be useful
    """
    return "Don't misuse this service or do anything illegal"

def backend_get(item_id = None):
    """ Analogue of GET method for backend use only.

    Args:
        id (str, optional): id for specif item, if it is not provided it will return all items. Defaults to None.

    Returns:
        list or dict: representation of item objects type depends on if item_id is provided or not.
    """
    item = Item()
    if not item_id:
        logger.info("retriving all items! (backend only)")
        query_result = item.get_all()
        item_from_db = [item_from_db for item_from_db in query_result]
        return item_from_db
        
    logger.info(f"Trying to retrive a item with id: {id} (backend only)" )
    try:
        return item.get_item(item_id)
    except ItemNotFound as err:
        return err
