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
# Leitus is a suite of higher level functions for cryptographic drives.
# An interface for the command line.
#

import argparse
import os.path
import sys

from leitus import diagnosis
from leitus.surface import Leitus

__version__ = '1.3.dev2'

#
#
# Scripting foo
INFO = """Leitus %(version)s

  Add the drive name to the command line, and I'll describe its configuration.

  For example 'leitus --info cool'

""" % {
    "version": __version__}


def leitus(conf_data, var_data):
    CommandLineInterface(os.path.join(conf_data, 'leitus'),
                         os.path.join(var_data, 'drives.d'),
                         os.path.join(var_data, 'profiles.d')).leitus()


def execute(args):
    if args.list:
        sys.stdout.write("Active drives:\n")
        for drive in app_from(args).list():
            sys.stdout.write("\t{}\n".format(drive))
        sys.stdout.write("\n")
    else:
        if args.name:
            app = app_from(args)
            if args.info:
                sys.stdout.write(app.info(args.name))
            else:
                app.perform(args.name)
        else:
            if args.info:
                write_info()
            else:
                write_version()


def app_from(args):
    return Leitus(conf_d=args.conf, drives_d=args.drives, profiles_d=args.profiles)


def write_version():
    sys.stdout.write(
        "Leitus %(version)s\n - Did you want something in particular?\n" % {"version": __version__})


def write_info():
    sys.stdout.write(INFO)


class CommandLineInterface:
    # Successful exit
    OKAY = 0
    # Exit with failure caused by missing configuration
    FAILURE_MISSING_CONFIGURATION = 1
    # Exit with failure when user cancels
    FAILURE_USER_CANCEL = 2
    # Exit with failure when disc image to be mapped is missing
    FAILURE_MISSING_DISC_IMAGE = 3
    # Exit with failure when encrypted drive cannot be unlocked
    FAILURE_CANNOT_UNLOCK_ENCRYPTED_DRIVE = 4
    # Exit with failure when some system requirement isn't met
    FAILURE_MISSING_REQUIREMENT = 5

    def __init__(self, conf_d, drives_d, profiles_d):
        self.conf_d = conf_d
        self.drives_d = drives_d
        self.profiles_d = profiles_d

    def leitus(self):
        try:
            args = self.parse_args()
            execute(args)
            return self.OKAY

        except diagnosis.ConfigurationPermissionError as error:
            return self.note_failure(self.FAILURE_MISSING_CONFIGURATION, error, error.recommended_fix())

        except diagnosis.ConfigurationNotFoundError as error:
            return self.note_failure(self.FAILURE_MISSING_CONFIGURATION, error, error.recommended_fix())

        except diagnosis.MissingDiscImageError as error:
            return self.note_failure(self.FAILURE_MISSING_DISC_IMAGE, error, error.recommended_fix())

        except diagnosis.CouldNotUnlockEncryptedDrive as error:
            return self.note_failure(self.FAILURE_CANNOT_UNLOCK_ENCRYPTED_DRIVE, error, error.recommended_fix())

        except diagnosis.UnsupportedRequirementError as error:
            return self.note_failure(self.FAILURE_MISSING_REQUIREMENT, error, error.recommended_fix())

        except diagnosis.InUseError as error:
            return self.note_failure(self.FAILURE_MISSING_REQUIREMENT, error, error.recommended_fix())

        except KeyboardInterrupt:
            sys.stderr.write("\nLeitus cancelled.\n\nSome manual tidy up might be a good idea.\n")
            return self.FAILURE_USER_CANCEL

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description="Leitus %(version)s does the legwork so users can relax and enjoy cryptographic drives."
                        % {"version": __version__})
        parser.add_argument('name', help='the configuration exercised', nargs='?', default=None)
        parser.add_argument('-c', '--conf',
                            help='configuration directory (defaults to %(conf.d)s)' % {"conf.d": self.conf_d},
                            nargs='?', default=self.conf_d)
        parser.add_argument('-p', '--profiles',
                            help='profiles directory (defaults to %(profiles.d)s)' % {
                                "profiles.d": self.profiles_d},
                            nargs='?', default=self.profiles_d)
        parser.add_argument('-d', '--drives',
                            help='drives directory (defaults to %(drives.d)s)' % {"drives.d": self.drives_d},
                            nargs='?', default=self.drives_d)
        parser.add_argument('-i', '--info',
                            help='describes the configuration',
                            action='store_true')
        parser.add_argument('-l', '--list',
                            help='lists all active drives',
                            action='store_true')
        args = parser.parse_args()
        return args

    @staticmethod
    def note_failure(exit_code, error, recommendations=None):
        sys.stderr.write("%(message)s\nLeitus failed.\n" % {"message": repr(error)})
        if recommendations:
            sys.stderr.write("\n")
            sys.stderr.write(recommendations)
            sys.stderr.write("\n")
        return exit_code
