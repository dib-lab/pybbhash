import sys
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

EXTRA_COMPILE_ARGS=[]
if sys.platform == 'darwin':              # Mac OS X?
    EXTRA_COMPILE_ARGS.extend(['-arch', 'x86_64', '-mmacosx-version-min=10.7',
                               '-std=c++11', '-stdlib=libc++'])
 

setup(
   name='bbhash',
   version='0.1dev',
   description="A Python wrapper for the BBHash Minimal Perfect Hash Function",
   author="C. Titus Brown",
   author_email="titus@idyll.org",
   license="BSD 3-clause",
   url="http://github.com/dib-lab/pybbhash",
   ext_modules =
          [Extension('bbhash',
                     sources=['bbhash.pyx'],
                     depends=['BooPHF.h'],
                     language='c++',
                     extra_compile_args=EXTRA_COMPILE_ARGS)],
   cmdclass = {'build_ext': build_ext}
)
