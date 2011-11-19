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
# Contains common diagnostics.
#
# Robert Burrell Donkin, 2011
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
                                 "Missing configuration: %(configuration)s not found in %(layout)s" % {"configuration": repr(configuration),
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


def fileNotFound(error_number):
    return (error_number == 2)
    
    

#
# Default logger for module
#
logger = logging.getLogger("leitus")