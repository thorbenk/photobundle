#kate: tab-indents off; tab-width 4; replace-tabs on; indent-width 4;

#Python
import os
import json
from functools import wraps

#Flask
from flask import request, abort, redirect
from flask_login import current_user, UserMixin

#App
from app import app, login_manager, USERS, PERMISSIONS

class User(UserMixin):
    def __init__(self, id):
        self.id = id
    @property
    def name(self):
        return self.id

@login_manager.user_loader
def load_user(id):
    """
    Reload the user object from the user ID stored in the session.
    Return None if the ID is invalid
    """
    if id in USERS:
        return User(id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")

def checkUser(username, password):
    return username in USERS and USERS[username] == password

def hasPermissions(path):
    if not current_user.is_authenticated:
        return False;
    n = path.find("/")
    if n >= 0:
        path = path[0:n]
    album = path
    allowedForAlbum = PERMISSIONS.get(album, [])
    allowed = current_user.id in allowedForAlbum
    #print "* user", current_user.id, "is",
    #print "allowed" if allowed else "NOT allowed",
    #print "for album '%s'" % album
    return allowed

def login_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if current_user and current_user.is_authenticated:
            return fn(*args, **kwargs)
        return app.login_manager.unauthorized()
    return decorated_view
