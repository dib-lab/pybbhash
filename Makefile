.PHONY: dist wheel test

all:
	pip install -e .

clean:
	rm -fr bbhash.cpp bbhash.cpython-36m-darwin.so build/ bbhash.egg-info

test: all
	py.test

upload: dist
	twine upload dist/bbhash-*.tar.gz

dist:
	rm -fr dist
	python -m build -s

wheel:
	rm -fr dist
	python -m build
