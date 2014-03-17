#!/usr/bin/env python

from distutils.core import setup

setup(name='ship-in-a-bottle',
        version='0.1',
        description='Run multiple WSGI scripts and/or bottles at the same port.',
        author='Chloride Cull',
        author_email='chloride@devurandom.net',
        url='http://devurandom.net/python/',
        scripts=['ship-in-a-bottle.py'],
        requires=["bottle"],
        data_files=[('/etc', ['cfgs/ship-in-a-bottle.conf']),
                    ('/srv/bottles', ['cfgs/ships.conf', 'examples/hello.py'])],
        classifiers=["Development Status :: 4 - Beta",
                     "Environment :: Web Environment",
                     "Intended Audience :: System Administrators",
                     "Framework :: Bottle",
                     "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
                     "Programming Language :: Python :: 3"]
     )
