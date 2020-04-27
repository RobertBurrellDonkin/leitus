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
import pwd
import stat


class User:
    NAME_FIELD = 0
    PASSWD_FIELD = 1
    UID_FIELD = 2
    GID_FIELD = 3
    COMMENT_FIELD = 4
    HOME_DIRECTORY_FIELD = 5
    SHELL_FIELD = 6

    def __init__(self, name):
        self.name = name

    def uid(self):
        return self.info()[self.UID_FIELD]

    def gid(self):
        return self.info()[self.GID_FIELD]

    def home(self):
        return self.info()[self.HOME_DIRECTORY_FIELD]

    def info(self):
        return pwd.getpwnam(self.name)

    def own(self, target):
        """
        Establishes this user as owner of target.
        Applied recursively when target is a directory.
        """
        uid = self.uid()
        gid = self.gid()
        os.chown(target, uid, gid)
        for root, dirs, files in os.walk(target):
            for file in files:
                os.chown(os.path.join(root, file), uid, gid)
        os.chmod(target, stat.S_IRWXU)

    def __repr__(self):
        return "User named '{0}'".format(self.name)
