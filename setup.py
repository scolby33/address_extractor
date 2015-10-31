"""Setup module for the address_extractor package"""

import setuptools
import codecs # To use a consistent encoding
import os
import re

#################################################################

PACKAGES = setuptools.find_packages(where='src')
META_PATH = os.path.join('src', 'address_extractor', '__init__.py')
KEYWORDS = ['addresses', 'mailing']
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Topic :: Office/Business'
]
INSTALL_REQUIRES = ['usaddress']
EXTRAS_REQUIRE = {}
CONSOLE_ENTRY_POINTS = ['address_extractor=address_extractor.__main__:main']

#################################################################

HERE = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    """Build an absolute path from *parts* and return the contents of the resulting file. Assume UTF-8 encoding."""
    with codecs.open(os.path.join(HERE, *parts), 'rb', 'utf-8') as f:
        return f.read()

META_FILE = read(META_PATH)

def find_meta(meta):
    """Extract __*meta*__ from META_FILE"""
    meta_match = re.search(
        r'^__{meta}__ = ["\']([^"\']*)["\']'.format(meta=meta),
        META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError('Unable to find __{meta}__ string'.format(meta=meta))

def get_long_description():
    """Get the long_description from the README.md file. Assume UTF-8 encoding."""
    with codecs.open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

if __name__ == '__main__':
    setuptools.setup(
        name = find_meta('title'),
        version = find_meta('version'),
        description = find_meta('description'),
        long_description = get_long_description(),
        url = find_meta('url'),
        author = find_meta('author'),
        author_email = find_meta('email'),
        maintainer = find_meta('author'),
        license = find_meta('license'),
        classifiers = CLASSIFIERS,
        keywords = KEYWORDS,
        packages = PACKAGES,
        package_dir = {'': 'src'},
        install_requires = INSTALL_REQUIRES,
        extras_require = EXTRAS_REQUIRE,
        entry_points = {
            'console_scripts': CONSOLE_ENTRY_POINTS
        }
    )
