#
# Copyright (c) Robert Burrell Donkin 2012-2013, 2020
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
#
#
from leitus.crypt import LuksDevice

from leitus.loop import LoopDevice


def an_image_drive(uuid, name, target):
    return ImageDrive(uuid, name, target)


class ImageDrive:

    def __init__(self, source, name, target):
        self.source = source
        self.name = name
        self.target = target

    def perform(self):
        LuksDevice().on(LoopDevice(self.source).open()).toggle(self.name, self.target)

    def info(self):
        return "Image Drive\n  source: {0}\n  target: {1}\n\n".format(self.source, self.target)
