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

from leitus.luks import LuksDrive


def test_info():
    uuid = "AAAA-BBBB"
    name = "some name"
    target = "some/target"
    subject = LuksDrive(uuid, name, target)

    assert subject.info() == ("\n\nLUKS encrypted drive:\n\n\tuuid:\t\tAAAA-BBBB\n\tmapping:\t" +
                              "'some name'\n\ttarget:\t\t'some/target'\n\n")
