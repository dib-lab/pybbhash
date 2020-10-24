all:
	python setup.py build_ext -i

clean:
	rm -fr bbhash.cpp bbhash.cpython-36m-darwin.so build/ bbhash.egg-info

test: all
	py.test

upload:
	rm -fr dist
	python setup.py sdist
	twine upload dist/bbhash-*.tar.gz
