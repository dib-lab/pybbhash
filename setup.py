import sys
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

EXTRA_COMPILE_ARGS=['-std=c++11']
if sys.platform == 'darwin':              # Mac OS X?
    EXTRA_COMPILE_ARGS.extend(['-arch', 'x86_64', '-mmacosx-version-min=10.7',
                               '-stdlib=libc++'])
 

setup(
   name='bbhash',
   version='0.3',
   description="A Python wrapper for the BBHash Minimal Perfect Hash Function",
   author="C. Titus Brown",
   author_email="titus@idyll.org",
   license="BSD 3-clause",
   url="http://github.com/dib-lab/pybbhash",
   setup_requires=["Cython>=0.29.21", "setuptools>=50.3.2", "numpy"],
   install_requires=['Cython>=0.29.21', "setuptools>=50.3.2", "numpy"],
   ext_modules =
          [Extension('bbhash',
                     sources=['bbhash.pyx'],
                     depends=['BooPHF.h'],
                     language='c++',
                     extra_compile_args=EXTRA_COMPILE_ARGS),
          Extension('bbhash_table',
                     sources=['bbhash_table.pyx'],
                     language='c++',
                     extra_compile_args=EXTRA_COMPILE_ARGS)],
   headers=['BooPHF.h'],
   cmdclass = {'build_ext': build_ext}
)
