all:
	python setup.py build_ext -i

clean:
	rm -fr bbhash.cpp bbhash.cpython-36m-darwin.so build/ bbhash.egg-info

test:
	python -m pytest tests.py

upload:
	rm -fr dist
	python setup.py sdist
	twine upload dist/bbhash-*.tar.gz
