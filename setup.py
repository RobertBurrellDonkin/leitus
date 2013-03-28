#!/usr/bin/env python
#
# Copyright (c) Robert Burrell Donkin 2011
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
# Leitus is a suite of higher level functions for cryptographic drives.
#
# Robert Burrell Donkin, 2011
#
from distutils.core import setup

setup(name='leitus',
      description='Leitus is a suite of higher level functions for cryptographic drives.',
      version='0.6-SNAPSHOT',
      author='Robert Burrell Donkin',
      author_email='leitus@robertburrelldonkin.name',
      url='https://github.com/RobertBurrellDonkin/leitus',
      license='GNU GPL v2',
      scripts=['bin/leitus'],
      packages=['name', 'name.robertburrelldonkin', 'name.robertburrelldonkin.leitus'],
      )
