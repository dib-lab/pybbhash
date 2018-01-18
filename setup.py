from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(ext_modules = [Extension('bbhash', sources=['bbhash.pyx', 'bbhash-wrap.cc'], language='c++',
     extra_compile_args=['-std=c++11', '-stdlib=libc++'])],
     cmdclass = {'build_ext': build_ext}
)
