#!/usr/bin/env python

import json
import sys
import os
from jinja2 import Template

#------------------------------------------------------------------------------

ALBUMS_ABS = "dist/albums"
CACHE_ABS  = "dist/cache"

ALBUMS_REL = "albums"
CACHE_REL = "cache"

def albumJsonFile (albumPath):
   return CACHE_ABS + "/" + albumPath + "/_" + os.path.basename(albumPath) + ".json"

#------------------------------------------------------------------------------

def readAlbum(jsonFilename, sort=None):
    with open(jsonFilename, 'r') as f:
        d = json.load(f)
    photos = d["photos"]
    if sort == 'filename':
        photos = sorted(photos, key=lambda image: image["name"])
    return photos

def writeAlbum(albumFilenames, outFilename, title, desc=None, sort=None, zipFile=None):
    assert isinstance(albumFilenames, list)
    
    template = Template(open('template/gallery.t.html', 'r').read())
   
    albumPhotos = []
    for albumPath in albumFilenames:
        albumFileJson = albumJsonFile (albumPath)
        for x in readAlbum(albumFileJson, sort=sort): 
            albumPhotos.append((albumFileJson, albumPath, x))
            
    print "there are %d photos in %s" % (len(albumPhotos), outFilename)
    
    album_title = title
    album_subtitle = "%d Fotos" % len(albumPhotos)
    
    images = []
    
    for i, (albumFileJson, albumPath, image) in enumerate(albumPhotos):
        print "[%04d/%04d] %s" % (i, len(albumPhotos), outFilename)
        sizes = image["thumbnailSizes"]
        
        assert " " not in image["name"]
        #originalImageFilename = originalImageFilename.replace(" ", "%20")
        
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
        
    out = template.render(page_title = album_title, album_title=album_title, album_subtitle=album_subtitle, images=images)
    with open(outFilename, 'w') as f:
        f.write(out)
                    
if __name__ == "__main__":
    
    writeAlbum(["testalbum", "testalbum/album2"], "dist/testalbum.html", "Test Album")

    
