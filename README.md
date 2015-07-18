# PhotoBundle

**Note**: Very much a work in progress

A simple folder-based photo viewer for the web,
based on
- [PhotoFloat](http://git.zx2c4.com/PhotoFloat/about/)
- [PhotoSwipe](http://photoswipe.com/)

## Installation

```bash
git clone https://github.com/thorbenk/photobundle.git
git submodule init
git submodule update

npm install
pip install iptcinfo
pip install jinja2

make grunt
```
Configure web browser to serve files from `dist/`.

## Creating albums

- put album directory structure in `dist/albums`
- edit `gen-albums.py`
- run `make albums`
