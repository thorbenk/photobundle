all:
	node_modules/grunt-cli/bin/grunt
	PhotoFloat/scanner/main.py dist/albums dist/cache
