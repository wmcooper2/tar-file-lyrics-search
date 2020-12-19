from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("search.py")
)


# run `python3 setup.py build_ext --inplace`

## if this error...
# (venv) cooper@Coopers-MacBook-Air tarFileLyricSearch % python3 setup.py build_ext --inplace
# running build_ext
# copying build/lib.macosx-10.9-x86_64-3.9/customEnglish/tarFileLyricSearch/search.cpython-39-darwin.so -> customEnglish/tarFileLyricSearch
# error: could not create 'customEnglish/tarFileLyricSearch/search.cpython-39-darwin.so': No such file or directory
## deleting __init__.py solved the problem
