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

virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

make grunt
```

All front-end code is copied to the `dist/` directory.

### Configuring the flask app

A lightweight flask application for authenticating users can be found in the
`app/` directory. Users and the available albums (with permissions per user)
are configured using JSON files.

To configure the app, adapt the files
- `app/app.cfg`
- `app/app.ini`
- `app/users.json`
- `app/albums.json`

Then, configure nginx according to `app/nginx.sample`.

Finally, run the app:
```bash
uwsgi app/app.ini
```

## Creating albums and thumbnails

First put or symlink your photos as a directory structure beneath `dist/albums`.

Next, run `make thumbs` to generate thumbnails for all photos.

In `app/albums.json`, you must configure a list of galleries as follows:
- Each entry in that list will be visilbe to the users as a single html gallery
  page (filename `out`).
- A gallery page can pull in photos from multiple 
  directories as specified in `dirs` (photos are **not** added recursively
  to the gallery page by default).
- The `title` is the page title and heading of the generated gallery page

