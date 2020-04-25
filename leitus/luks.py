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

from leitus.deep import LuksDevice, DiskByUUID

INFO = """

LUKS encrypted drive:

\tuuid:\t\t{0}
\tmapping:\t'{1}'
\ttarget:\t\t'{2}'

"""


def a_luks_drive(uuid, name, target):
    return LuksDrive(uuid, name, target)


class LuksDrive:

    def __init__(self, uuid, name, target):
        self.uuid = uuid
        self.name = name
        self.target = target

    def perform(self):
        print("LUKS ", self.uuid, self.name, self.target)
        LuksDevice().on(DiskByUUID(self.uuid)).toggle(self.name, self.target)

    def info(self):
        return INFO.format(self.uuid, self.name, self.target)
