# PhotoBundle

**Note**: Very much a work in progress

A simple folder-based photo viewer for the web,
based on
- [PhotoFloat](http://git.zx2c4.com/PhotoFloat/about/)
- [PhotoSwipe](http://photoswipe.com/)

## Installation

```bash
git clone https://github.com/thorbenk/photobundle.git
cd photobundle
git submodule init
git submodule update

npm install
pip install -r requirements.txt

make grunt
```
Configure web browser to serve files from `dist/`.

## Creating albums

First put or symlink your photos as a directory structure beneath `dist/albums`.

Next, run `make thumbs` to generate thumbnails for all photos.

To create a HTML gallery pages, create a JSON file `pages.json`

```json
[
    { 
        "dirs":  ["testalbum", "testalbum/album2"],
        "out":   "testalbum.html",
        "title": "Test album"
    }
]
```

- Each entry in that list will create a single html gallery page
  (filename `out`).
- A gallery page can pull in photos from multiple 
  directories as specified in `dirs` (photos are **not** added recursively
  to the gallery page by default).
- The `title` is the page title and heading of the generated gallery page

Then, run `./gen-albums pages.json`