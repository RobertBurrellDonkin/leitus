#!/usr/bin/env python
#
# Copyright (c) Robert Burrell Donkin 2011, 2020
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#
from setuptools import setup

from leitus import cli

setup(name='leitus',
      description='Leitus is a suite of higher level functions for cryptographic drives.',
      long_description='A suite of higher level tasks for cryptographic drive management',
      version=cli.__version__,
      author='Robert Burrell Donkin',
      author_email='leitus@robertburrelldonkin.name',
      url='https://github.com/RobertBurrellDonkin/leitus',
      license='GNU GPL v2',
      scripts=['scripts/leitus'],
      packages=['leitus'],
      classifiers=[
          'Programming Language :: Python :: 3.7"'
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Operating System :: POSIX',
          'Intended Audience :: System Administrators',
          'Development Status :: 4 - Beta',
          'Environment :: Console',
      ]
      )
