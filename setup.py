from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
   name='bbhash',
   version='0.1dev',
   description="A Python wrapper for the BBHash Minimal Perfect Hash Function",
   author="C. Titus Brown",
   author_email="titus@idyll.org",
   license="BSD 3-clause",
   url="http://github.com/dib-lab/pybbhash",
   ext_modules =
          [Extension('bbhash', sources=['bbhash.pyx', 'bbhash-wrap.cc'],
                     language='c++',
                     extra_compile_args=['-std=c++11', '-stdlib=libc++'])],
   cmdclass = {'build_ext': build_ext}
)
