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

import os
import os.path
from tempfile import NamedTemporaryFile

from leitus.deep import CryptDeviceWithRandomKey, LoopDevice, ExtFileSystem


def a_session_home(profiles, name, size_in_megabytes, user, target):
    return SessionHome(profiles, name, size_in_megabytes, user, target)


INFO = """

Session drive:

\tsize:\t\t{0}M
\tmapping:\t'{1}'
\ttarget:\t\t'{2}'
\tuser:\t\t{3}
\tprofiles:\t"""


class SessionHome:
    def __init__(self, profiles, name, size_in_megabytes, user, target):
        self.profiles = profiles
        self.name = name
        self.user = user
        self.size_in_megabytes = size_in_megabytes
        self.target = target
        self.filename = NamedTemporaryFile(prefix='leitus-drive-' + name + '-', suffix=".img").name

    def commission(self):
        CryptDeviceWithRandomKey().on(
            LoopDevice(self.filename).create(self.size_in_megabytes).open()).map_to(
            self.name).with_format(ExtFileSystem()).mount_on(self.target).merge(self.profiles).own_by(self.user)

    def decommission(self):
        CryptDeviceWithRandomKey().on(
            LoopDevice(self.filename)).unmap_from(self.name, self.target)

    def perform(self):
        if os.path.exists(self.filename):
            self.decommission()
        else:
            self.commission()

    def info(self):
        info = INFO.format(self.size_in_megabytes, self.name, self.target, self.user)
        is_first_time = True
        for profile in self.profiles:
            if is_first_time:
                is_first_time = False
            else:
                info += ','
            info += repr(profile)
        info += "\n\n"
        return info
