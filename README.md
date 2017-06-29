# PhotoBundle

A simple folder-based photo viewer for the web,
based on
- [PhotoFloat](http://git.zx2c4.com/PhotoFloat/about/)
- [PhotoSwipe](http://photoswipe.com/)

![screenshot](https://raw.githubusercontent.com/thorbenk/photobundle/master/github/screenshot.png)

## Installation

On Ubuntu 17.04, you'll need to install:
```bash
sudo apt install npm grunt uwsgi uwsgi-plugin-python nginx
```

```bas
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
Here is a simple development environment working on Ubuntu 17.04:

```bash
cd photobandle
source .venv/bin/activate

sed -e "s|PHOTOBUNDLE_PATH|$PWD|g" app/nginx.sample > /tmp/nginx.conf && sudo cp /tmp/nginx.conf /etc/nginx/sites-available/localhost.photobundle
sudo ln -s /etc/nginx/sites-available/localhost.photobundle /etc/nginx/sites-enabled
sudo service nginx restart

sed -e "s|PHOTOBUNDLE_PATH|$PWD|g" app/app.cfg.sample > app/app.cfg
sed -e "s|PHOTOBUNDLE_PATH|$PWD|g" app/app.ini.sample > app/app.ini
cp app/users.json.sample app/users.json
vim app/albums.json # see below

uwsgi app/app.ini
```

Finally, go to http://localhost:8080

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

