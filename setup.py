import sys

from os import path
from ssl import OPENSSL_VERSION
from codecs import open
from setuptools import setup, find_packages
from distutils.version import StrictVersion

from agilepay.constants import SDK_VERSION

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='agilepay',

    version=SDK_VERSION,

    description='The AgilePay python sdk',

    long_description=long_description,

    url='https://github.com/agile-pay/python-sdk',

    author='Alessandro Colaneri',

    author_email='colaneri.alessandro@gmail.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='agilepay.io, payment gateways aggreagator, api gateways aggreagator, payment processing, credit cards, transaction scheduling, stripe, braintree, sagepay, authorize.net, realex, worldpay, securionpay, cardstream, paypal',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'requests >= 0.8.8, < 0.10.1' if sys.version_info < (2, 6) else 'requests >= 0.8.8'
    ],
)