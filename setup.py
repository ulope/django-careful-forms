import codecs
import re
from os import path
from setuptools import setup


def read(*parts):
    file_path = path.join(path.dirname(__file__), *parts)
    return codecs.open(file_path).read()


def find_version(*parts):
    version_file = read(*parts)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='django-careful-forms',
    version=find_version('careful_forms', '__init__.py'),
    description="Security minded forms extension for django",
    long_description=read('README.rst'),
    author='Ulrich Petri',
    author_email='mail@ulo.pe',
    license='MIT',
    url='https://github.com/ulope/django-careful-forms',
    packages=[
        'careful_forms',
        'careful_forms.tests',
    ],
    install_requires=[
        'django-appconf>=0.5',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
    ],
)
