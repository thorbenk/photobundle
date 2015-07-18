grunt:
	node_modules/grunt-cli/bin/grunt

albums:
	PhotoFloat/scanner/main.py dist/albums dist/cache
	./gen-albums.py

