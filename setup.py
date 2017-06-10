#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Setup file for easy installation."""
from setuptools import setup
import glob
from openmoo2 import __version__

setup(
    name='openmoo2',
    description='Master of Orion II',
    long_description='open source clone of Microprose game "Master of Orion II: Battle at Antares"',
    url='http://openmoo2.org/',
    download_url='https://github.com/scarabeusiv/openmoo2',

    version=__version__,

    test_require=[
        "nose",
    ],

    author='Petr Mika',
    author_email='peterman@email.cz',

    maintainer='Tomáš Chvátal',
    maintainer_email='tomas.chvatal@gmail.com',

    license='License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
    platforms=['Linux'],
    keywords=['Strategy', 'Game'],

    packages=['openmoo2'],

    data_files=[('/usr/share/openmoo2/', glob.glob('data/*')), ],

    entry_points={
        'console_scripts': ['openmoo2 = openmoo2:main'],
    },
)
