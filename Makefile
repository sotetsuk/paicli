.PHONY: clear build test

clear:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	find . -name "*pycache*" | xargs rm -rf
	find paicli -name "*.pyc" | xargs rm

build:
	python setup.py install

test:
	python -m unittest -v paicli/tests/*.py
