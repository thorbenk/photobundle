#kate: space-indents on; tab-width 4; replace-tabs on; indent-width 4;

#Python
from collections import defaultdict
import os
import json
from random import shuffle
from mimetypes import guess_type

#Flask
from flask import Response, abort, json, request, jsonify, redirect, render_template
from flask_login import login_user, logout_user, current_user

#App
from app import app, PWD
from app.login import login_required, load_user, User, hasPermissions, checkUser

CACHE_PATH = app.config["CACHE_PATH"]
ALBUM_PATH = app.config["ALBUM_PATH"]
CACHE_ACCEL = app.config["CACHE_ACCEL"]
ALBUM_ACCEL = app.config["ALBUM_ACCEL"]

ALBUMS_REL = "/albums"
CACHE_REL = "/cache"

class AlbumEntry:
    def __init__(self, pagename, title, directories):
        self.pagename = pagename
        self.title = title
        self.directories = directories

def readAlbums():
    albumList = []
    with open(os.path.join(PWD, "albums.json"), "r") as f:
        albums = json.load(f)
        for album in albums:
            pagename = album.get("out", None)
            title = album.get("title", None)
            directories = album.get("dirs", None)
            if not pagename or not title or not directories:
                continue
            if not all([hasPermissions(x) for x in directories]):
                continue
            albumList.append(AlbumEntry(pagename, title, directories))
    return albumList

def albumJsonFile (albumPath):
   return os.path.join(CACHE_PATH, albumPath, "_"+os.path.basename(albumPath)+".json")

def readAlbum(jsonFilename, sort=None):
    with open(jsonFilename, 'r') as f:
        d = json.load(f)
    photos = d["photos"]
    if sort == 'filename':
        photos = sorted(photos, key=lambda image: image["name"])
    return photos

def accel_redirect(internal, real, relative_name):
    real_path = os.path.join(real, relative_name)
    internal_path = os.path.join(internal, relative_name)
    if not os.path.isfile(real_path):
        abort(404)
    mimetype = None
    types = guess_type(real_path)
    if len(types) != 0:
        mimetype = types[0]
    response = Response(mimetype=mimetype)
    response.headers.add("X-Accel-Redirect", internal_path)
    
    # FIXME: cache control and permissions after logout?
    
    response.cache_control.public = True
    if mimetype == "application/json":
        response.cache_control.max_age = 3600
    else:
        response.cache_control.max_age = 29030400
    
    return response

#------------------------------------------------------------------------------

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user and current_user.is_authenticated:
        return redirect("/")
   
    if request.method == 'POST':
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        if not checkUser(username, password):
            # login failed
            return redirect("/login")
        
        user = load_user(username)
        if not user:
            return redirect("/login")
        
        login_user(user)
    
        return redirect("/")
    return render_template("login.html")

@app.route("/a/<path:path>")
@login_required
def albumPage(path):
    sort = None # TODO
   
    title = None
    directories = None
    # find title, directories entry for the given "path"
    # (that is, an albums name "xyz.html", which might consist of
    # a number of 'real' directories full of photos
    with open(os.path.join(PWD, "albums.json"), "r") as f:
        albums = json.load(f)
        for album in albums:
            pagename = album.get("out", None)
            title = album.get("title", None)
            directories = album.get("dirs", None)
            if pagename == path:
                break
    
    if not directories:
        abort(404)
    
    albumPhotos = []
    for albumPath in directories:
        albumFileJson = albumJsonFile (albumPath)
        for x in readAlbum(albumFileJson, sort=sort): 
            albumPhotos.append((albumFileJson, albumPath, x))
            
    album_title = title
    album_subtitle = "%d Fotos" % len(albumPhotos)
    
    images = []
    
    for i, (albumFileJson, albumPath, image) in enumerate(albumPhotos):
        sizes = image["thumbnailSizes"]
        assert " " not in image["name"]
        
        fullPathPrefix  = ALBUMS_REL + "/" + albumPath + "/"
        cachePathPrefix =  CACHE_REL + "/" + albumPath + "/"
        
        cacheFname = cachePathPrefix+image["name"]

        bigSize = sizes[-1]
        medSize = sizes[-2]
        thumbSize = sizes[1]
        bigSizeStr = "%dx%d" % (bigSize[0], bigSize[1])
        medSizeStr = "%dx%d" % (medSize[0], medSize[1])
        thumbSizeStr = "%dx%d" % (thumbSize[0], thumbSize[1])
        
        entry = {}
        entry["thumb_width"] = thumbSize[0]
        entry["thumb_height"] = thumbSize[1]
        
        entry["cache_big_url"] = cacheFname+"_"+bigSizeStr+".jpg"
        entry["cache_big_width"] = bigSize[0]
        entry["cache_big_height"] = bigSize[1]
        
        entry["cache_med_url"] = cacheFname+"_"+medSizeStr+".jpg"
        entry["cache_med_width"] = medSize[0]
        entry["cache_med_height"] = medSize[1]
        
        entry["cache_thumb_width"] = thumbSize[0]
        entry["cache_thumb_height"] = thumbSize[1]
        entry["cache_thumb_url"] = cacheFname+"_"+thumbSizeStr+".jpg"
        
        entry["orig_url"] = fullPathPrefix + image["name"]
        
        images.append(entry)
        
    return render_template("gallery.html", page_title = album_title, album_title=album_title, album_subtitle=album_subtitle, images=images)

@app.route("/")
@login_required
def index():
    return render_template("index.html", albums=readAlbums())

@app.route("/albums/<path:path>")
def albums(path):
    if not hasPermissions(path):
        abort(403)
    return accel_redirect(CACHE_ACCEL, CACHE_PATH, path)

@app.route("/cache/<path:path>")
def cache(path):
    if not hasPermissions(path):
        abort(403)
    return accel_redirect(CACHE_ACCEL, CACHE_PATH, path)
