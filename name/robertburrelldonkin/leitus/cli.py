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
# An interface for the command line.
#
# Robert Burrell Donkin, 2011
#

from name.robertburrelldonkin.leitus import diagnosis
from name.robertburrelldonkin.leitus.surface import Leitus

#
#
# Scripting foo

import sys
import os.path
import argparse

def leitus(conf_data, var_data):
    CommandLineInterface(os.path.join(conf_data, 'leitus'),
                         os.path.join(var_data, 'drives.d'),
                         os.path.join(var_data, 'profiles.d')).leitus()

class CommandLineInterface():
    
    # Successful exit
    OKAY=0
    # Exit with failure caused by missing configuration
    FAILURE_MISSING_CONFIGURATION=1
    # Exit with failure when user cancels
    FAILURE_USER_CANCEL=2
    
    def __init__(self, conf_d, drives_d, profiles_d):
        self.conf_d = conf_d
        self.drives_d = drives_d
        self.profiles_d = profiles_d

    def leitus(self):
        try:
            parser = argparse.ArgumentParser(description="Leitus %(version)s does the legwork so users can relax and enjoy cryptographic drives."
                                             % {"version":__version__})
            parser.add_argument('name', help='the configuration exercised', nargs='?', default=None)
            parser.add_argument('-c', '--conf', help='configuration directory', nargs='?', default=self.conf_d)
            parser.add_argument('-p', '--profiles', help='profiles directory', nargs='?', default=self.profiles_d)
            parser.add_argument('-d', '--drives', help='drives directory', nargs='?', default=self.drives_d)
            args = parser.parse_args()
            
            Leitus(conf_d=args.conf, drives_d=args.drives, profiles_d=args.profiles).perform(args.name)
            return self.OKAY
        
        except diagnosis.ConfigurationNotFoundError, error:
            return self.noteFailure(self.FAILURE_MISSING_CONFIGURATION, error, error.recommendedFix())
            
        except KeyboardInterrupt:
            sys.stderr.write("\nLeitus cancelled.\n\nSome manual tidy up might be a good idea.\n")
            return self.FAILURE_USER_CANCEL
    
    def noteFailure(self, exit_code, error, recommendations=None):
        sys.stderr.write("%(message)s\nLeitus failed.\n" % {"message": repr(error)})
        if recommendations:
            sys.stderr.write("\n")
            sys.stderr.write(recommendations)
            sys.stderr.write("\n")
        return exit_code
    
__version__="0.4-SNAPSHOT"