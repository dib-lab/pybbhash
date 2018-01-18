all:
	python setup.py build_ext -i

clean:
	rm -fr bbhash.cpp bbhash.cpython-36m-darwin.so build/ bbhash.egg-info

