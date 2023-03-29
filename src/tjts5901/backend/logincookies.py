from flask import session, redirect, url_for
from functools import wraps

def logged_in(f):
    """
    Check login info from session cookie. Use as decorator
    """

    @wraps(f)
    def decor(*args, **kwargs):
        if not 'logged_in' in session:
            return redirect('/login_page')
        return f(*args, **kwargs)
    return decor

def admin_logged_in(f):
    """
    Check admin login info from session cookie. Use as decorator
    """
    @wraps(f)
    def koristeltu(*args, **kwargs):
        if not 'admin_login' in session:
            return redirect(url_for("adminLogin"))
        return f(*args, **kwargs)
    return koristeltu

def login_with_user(username):
    session['logged_in'] = username

def admin_with_user(username):
    session['admin_login'] = username

def get_user_id():
    return session.get('logged_in', None)

def get_admin_id():
    return session.get('admin_login', None)

def logout_all():
    session.clear()
    
