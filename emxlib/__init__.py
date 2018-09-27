# **************************************************************************
# *
# * Authors:     J.M. De la Rosa Trevin (delarosatrevin@scilifelab.se)
# *
# * SciLifeLab, Stockholm University
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

import os
import pyworkflow.em
from pyworkflow.utils import Environ
from emxlib.constants import EMXLIB_HOME
from emxlib.utils import *


_logo = "emx_logo.png"
_references = ['Marabini2016']


class Plugin(pyworkflow.em.Plugin):
    _homeVar = EMXLIB_HOME
    _pathVars = []

    @classmethod
    def _defineVariables(cls):
        cls._defineEmVar(EMXLIB_HOME, 'emx_export-1.0.0')

    @classmethod
    def getEnviron(cls):
        """ Setup the environment variables needed to launch emx export. """
        environ = Environ(os.environ)

        environ.update({
            'PATH': Plugin.getHome(),
            'LD_LIBRARY_PATH': str.join(cls.getHome(), 'emxlib')
                               + ":" + cls.getHome(),
        }, position=Environ.BEGIN)

        return environ

    @classmethod
    def defineBinaries(cls, env):
        """ Define required binaries in the given Environment. """
        pass


pyworkflow.em.Domain.registerPlugin(__name__)