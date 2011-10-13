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

class ConfigurationNotFoundError(Exception):
    def __init__(self, configuration, layout, error):
        self.configuration = configuration
        self.layout = layout
        logger.debug(error)
        Exception.__init__(self, str(self))
        
    def __str__(self):
        return "Missing configuration: %(configuration)s not found in %(layout)s" % {"configuration": repr(self.configuration),
                                                "layout": repr(self.layout)}
    
    def __repr__(self):
        return str(self)
    
    def recommendedFix(self):
        return "Did you mistype %(name)s?" % {"name": repr(self.configuration)} 

def fileNotFound(error_number):
    return (error_number == 2)
    
    
    
    

#
# Default logger for module
#
logger = logging.getLogger("leitus")