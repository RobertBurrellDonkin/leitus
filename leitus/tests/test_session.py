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
#
#
# Leitus is a suite of higher level functions for cryptographic drives.
# The contents tests the surface module.
#
# Robert Burrell Donkin, 2011
#

from leitus import session


def test_info():
    profiles = ["a profile", "another profile"]
    name = "some name"
    size_in_megabytes = 12345
    user = "some_user"
    target = "some/target"
    subject = session.SessionHome(profiles, name, size_in_megabytes, user, target)

    assert subject.info() == ("\n\nSession drive:\n\n\tsize:\t\t12345M\n\tmapping:\t" +
                              "'some name'\n\ttarget:\t\t'some/target'\n\tuser:\t\tsome_user\n\tprofiles:\t" +
                              "'a profile','another profile'\n\n")
