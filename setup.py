# -*- coding: utf-8 -*-
from Cython.Build import cythonize
from setuptools import setup
from setuptools import Extension
from setuptools.dist import Distribution
from distutils.command.build_ext import build_ext
import os

packages = ["aiodeu"]

package_data = {"": ["*"]}

extras_require = {
    "aws": ["boto3>=1.26.20,<2.0.0"],
    "faust": [
        "faust-streaming[cython,fast]>=0.10.4,<0.11.0",
        "python-schema-registry-client>=2.4.1,<3.0.0",
    ],
}

entry_points = {"console_scripts": ["aiodeu = aiodeu.console:main"]}

setup_kwargs = {
    "name": "aiodeu",
    "version": "0.1.30",
    "description": "aio data engineering utils",
    "long_description": "None",
    "author": "Josh Rowe",
    "author_email": "s-block@users.noreply.github.com",
    "maintainer": "Josh Rowe",
    "maintainer_email": "s-block@users.noreply.github.com",
    "url": "https://github.com/s-block/aiodeu",
    "packages": packages,
    "package_data": package_data,
    "extras_require": extras_require,
    "entry_points": entry_points,
    "python_requires": ">=3.8.1,<4.0",
}


try:
    from Cython.Build import cythonize
    extensions = ["aiodeu/cetl.pyx"]
    # gcc arguments hack: enable optimizations
    os.environ["CFLAGS"] = "-O3"
    # Build
    setup_kwargs.update(
        {
            "ext_modules": cythonize(
                extensions,
                language_level=3,
                compiler_directives={"linetrace": True},
            ),
            "cmdclass": {"build_ext": build_ext},
        }
    )
except ImportError:
    pass

setup(**setup_kwargs)
