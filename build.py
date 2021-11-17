from distutils.extension import Extension
from glob import iglob
from os.path import splitext

from Cython.Build import cythonize
from setuptools_rust import Binding, RustExtension


def _find_native_extensions():
    for filename in iglob("advent_of_code/**/*.pyx", recursive=True):
        package = splitext(filename)[0].replace("/", ".")
        yield Extension(package, [filename])


def build(setup_kwargs):
    native_extensions = tuple(_find_native_extensions())
    setup_kwargs["ext_modules"] = cythonize(native_extensions, build_dir="build")

    setup_kwargs["rust_extensions"] = [
        RustExtension(target="aoc_rust", path="rust/Cargo.toml", binding=Binding.PyO3, native=True, debug=False)
    ]
