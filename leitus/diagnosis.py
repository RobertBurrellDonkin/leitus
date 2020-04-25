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
# Contains common diagnostics.
#

import logging


class DiagnosticError(Exception):
    def __init__(self, error, fix, message):
        self.diagnosticMessage = message
        self.causalError = error
        self.fix = fix
        logger.debug(error)
        Exception.__init__(self, message)

    def __str__(self):
        return self.diagnosticMessage

    def __repr__(self):
        return str(self)

    def recommendedFix(self):
        return self.fix


class ConfigurationNotFoundError(DiagnosticError):
    def __init__(self, configuration, layout, error):
        self.configuration = configuration
        self.layout = layout
        DiagnosticError.__init__(self,
                                 error,
                                 "Did you mistype %(name)s?" % {"name": repr(configuration)},
                                 "Missing configuration: %(configuration)s not found in %(layout)s" % {
                                     "configuration": repr(configuration),
                                     "layout": repr(layout)})


class ConfigurationPermissionError(DiagnosticError):
    def __init__(self, configuration, layout, error):
        self.configuration = configuration
        self.layout = layout
        DiagnosticError.__init__(self,
                                 error,
                                 "Did you mean to sudo?",
                                 "Could not read %(configuration)s in %(layout)s" % {
                                     "configuration": repr(configuration),
                                     "layout": repr(layout)})


class MissingDiscImageError(DiagnosticError):
    def __init__(self, layout, error, discImageNotFound):
        self.layout = layout
        self.error = error
        self.discImageNotFound = discImageNotFound
        DiagnosticError.__init__(self,
                                 error,
                                 "Did you mean to specify a drives directory on the command line?",
                                 "Disc image '%(discImage)s' not found. Drives in %(drives)s"
                                 % {"discImage": str(discImageNotFound), "drives": repr(layout.drives())})


class CouldNotUnlockEncryptedDrive(DiagnosticError):
    def __init__(self, layout, error, driveThatCouldNotBeUnlock):
        self.layout = layout
        self.error = error
        self.driveThatCouldNotBeUnlock = driveThatCouldNotBeUnlock
        DiagnosticError.__init__(self,
                                 error,
                                 "Did you type the right passphase?",
                                 "\n'%(discImage)s' couldn't be unlocked."
                                 % {"discImage": str(driveThatCouldNotBeUnlock)})


class UnsupportedRequirementError(DiagnosticError):
    def __init__(self, error):
        DiagnosticError.__init__(self,
                                 error,
                                 "Looks like your system is missing a vital requirement for Leitus.",
                                 error.explain())


class InUseError(DiagnosticError):
    def __init__(self, error):
        DiagnosticError.__init__(self,
                                 error,
                                 "",
                                 "%(resource)s is already in use."
                                 % {"resource": str(error.resource)})


def fileNotFound(error_number):
    return (error_number == 2)


#
# Default logger for module
#
logger = logging.getLogger("leitus")

__version__ = '1.0rc1.dev'
