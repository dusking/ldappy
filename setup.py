import os
import codecs
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


setup(
    name='ldappy',
    version="0.1.3",
    url='https://github.com/dusking/ldapy',
    author='Omer Duskin',
    author_email='dusking@gmail.com',
    license='LICENSE',
    platforms='All',
    description='Query LDAP server without LDAP knowledge',
    long_description=read('README.rst'),
    packages=['ldappy'],
    install_requires=[
        "pyldap==2.4.25.1",
    ],
    classifiers=[
        'Programming Language :: Python',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
