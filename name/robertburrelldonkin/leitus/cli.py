#
# Copyright (c) Robert Burrell Donkin 2011
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
# Leitus is a suite of higher level functions for cryptographic drives.
# An interface for the command line.
#
# Robert Burrell Donkin, 2011
#

from name.robertburrelldonkin.leitus.surface import Leitus

#
#
# Scripting foo

import os.path
import argparse

def leitus(conf_data, var_data):
    CommandLineInterface(os.path.join(conf_data, 'leitus'),
                         os.path.join(var_data, 'drives.d'),
                         os.path.join(var_data, 'profiles.d')).leitus()

class CommandLineInterface():
    
    def __init__(self, conf_d, drives_d, profiles_d):
        self.conf_d = conf_d
        self.drives_d = drives_d
        self.profiles_d = profiles_d

    def leitus(self):
        parser = argparse.ArgumentParser(description="Leitus does the legwork so users can relax and enjoy cryptographic drives.")
        parser.add_argument('name', help='the configuration exercised', nargs='?', default=None)
        parser.add_argument('-c', '--conf', help='configuration directory', nargs='?', default=self.conf_d)
        parser.add_argument('-p', '--profiles', help='profiles directory', nargs='?', default=self.profiles_d)
        parser.add_argument('-d', '--drives', help='drives directory', nargs='?', default=self.drives_d)
        args = parser.parse_args()
        
        Leitus(conf_d=args.conf, drives_d=args.drives, profiles_d=args.profiles).perform(args.name)
