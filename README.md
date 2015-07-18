# PhotoBundle

**Note**: Very much a work in progress

A simple folder-based photo viewer for the web,
based on
- [PhotoFloat](http://git.zx2c4.com/PhotoFloat/about/)
- [PhotoSwipe](http://photoswipe.com/)

## Installation

- put album directory structure in `dist/albums`
- edit `gen-albums.py`

```bash
npm install
pip install iptcinfo
pip install jinja2

make
./gen-albums.py
```

Configure web browser to serve files from `dist/`.