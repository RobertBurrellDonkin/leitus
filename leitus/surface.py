#
# Copyright (c) Robert Burrell Donkin 2011-2013, 2020
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
# Leitus is a suite of higher level functions for cryptographic drives.
# The surface module contains a high level API.
#

from leitus import config
from leitus import deep
from leitus import diagnosis
from leitus import layout
from leitus.config import ConfigConstants


def standard():
    return session_home('neo').with_size(2000).for_user(
        'rdonkin').merge_profiles(['home', 'gnome', 'maven', 'java6']
                                  ).build()


def session_home(name):
    return Builder().named(name)


class Configure:
    def __init__(self, api=deep.Facade()):
        self.api = api

    def with_configuration(self, configuration, directory_layout=None):
        constants = ConfigConstants()
        if constants.UUID in configuration:
            return self.api.a_luks_drive(constants.uuid_for(configuration),
                                         constants.name_for(configuration),
                                         constants.target_for(configuration))
        elif constants.SOURCE in configuration:
            source_disc_image = constants.source_for(configuration)
            if directory_layout:
                source_disc_image = directory_layout.drivePath(source_disc_image)
            return self.api.an_image_drive(source_disc_image,
                                           constants.name_for(configuration),
                                           constants.target_for(configuration))
        else:
            user = constants.user_for(configuration)
            return self.api.a_session_home(constants.profiles_for(configuration),
                                           constants.name_for(configuration), constants.size_for(configuration),
                                           user, user.home())


class Builder:

    def __init__(self):
        self.configuration = {}
        self.constants = ConfigConstants()

    def merge_profiles(self, profiles):
        self.configuration[self.constants.PROFILES] = profiles
        return self

    def for_user(self, with_name):
        self.configuration[self.constants.USER] = with_name
        return self

    def with_size(self, megabytes):
        self.configuration[self.constants.SIZE] = megabytes
        return self

    def named(self, name):
        self.configuration[self.constants.NAME] = name
        return self

    def build(self):
        return with_configuration(self.configuration)


class Leitus:
    def __init__(self, conf_d, drives_d, profiles_d, api=deep.Facade()):
        self.layout = layout.StandardLayout(conf_d, drives_d, profiles_d)
        self.api = api

    def with_configuration(self, name):
        return Configure(self.api).with_configuration(config.load(name, self.layout.conf()), self.layout)

    def perform(self, name):
        try:
            if name:
                self.with_configuration(name).perform()
            else:
                standard().perform()
        except deep.DiscImageNotFoundError as error:
            raise diagnosis.MissingDiscImageError(self.layout, error, error.resource)

        except deep.PassphaseError as error:
            raise diagnosis.CouldNotUnlockEncryptedDrive(self.layout, error, error.resource)

        except deep.UnsupportedError as error:
            raise diagnosis.UnsupportedRequirementError(error)

        except deep.AlreadyInUseError as error:
            raise diagnosis.InUseError(error)

    def info(self, name):
        if name:
            return self.with_configuration(name).info()
        else:
            return "Here's the deal: a name for information"


__version__ = '1.0rc2.dev'
