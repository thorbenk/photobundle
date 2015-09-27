#kate: tab-indents off; tab-width 4; replace-tabs on; indent-width 4;

#Python
import os.path
import json
from collections import defaultdict
import codecs

#Flask
from flask import Flask
from flask_login import LoginManager

USERS = dict()
PERMISSIONS = defaultdict(set)
PWD = os.path.dirname(os.path.abspath(__file__))

def readPermissions():
    global PERMISSIONS, PWD
    with codecs.open(os.path.join(PWD, "albums.json"), "r", "UTF-8") as f:
        albums = json.loads(f.read())
        for album in albums:
            auth = album.get("auth", [])
            dirs = album.get("dirs", [])
            for directory in dirs:
                for user in auth:
                    PERMISSIONS[directory].add(user)

def readUsers():
    global USERS, PWD
    with open(os.path.join(PWD, "users.json"), "r") as f:
        users = json.loads(f.read())
        for user, passwd in users.iteritems():
            USERS[user] = passwd

readPermissions()
readUsers()

app = Flask(__name__)
app.config.from_pyfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.cfg"))
login_manager = LoginManager()

import login
login_manager.init_app(app)
login_manager.login_view="login"
import endpoints




