from Cython.Build import cythonize
from distutils.extension import Extension
from glob import iglob
from os.path import splitext


def _find_native_extensions():
    for filename in iglob('advent_of_code/**/*.pyx', recursive=True):
        package = splitext(filename)[0].replace('/', '.')
        yield Extension(package, [filename])


def build(setup_kwargs):
    extensions = tuple(_find_native_extensions())
    setup_kwargs['ext_modules'] = cythonize(extensions, build_dir='build')
