from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext
import pybind11

ext_modules = [
    Pybind11Extension(
        "caen_cpp",
        ["src/cpp/pybind11_module.cpp", "src/cpp/CBinaryIn.cpp"],
        language = "c++",
        include_dirs = ["./src/cpp/", pybind11.get_include()],
        cxx_std = 11,
    )
]

setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)