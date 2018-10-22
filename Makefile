.PHONY: clear build test

clear:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	find . -name "*pycache*" | xargs rm -rf
	find paicli -name "*.pyc" | xargs rm -rf

build:
	python setup.py install
	python setup.py sdist bdist_wheel

test:
	python -m unittest -v paicli/tests/*.py

pypi:
	python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
