import os

from setuptools import setup, find_packages

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))

about = {}
with open(os.path.join(ROOT, "codecommit_slack", "__about__.py")) as f:
    exec (f.read(), about)

setup(
    name=about["__title__"],
    version=about["__version__"],
    author=about["__author__"],
    url=about["__uri__"],
    description=about["__summary__"],
    license=about["__license__"],
    packages=find_packages(exclude=["test*"]),
    install_requires=[
        'boto3',
        'requests'
    ],
    extra_requires={
        'tests': [
            'flake8',
            'pyflakes',
            'pytest',
            'pytest-mock'
        ]
    }
)
