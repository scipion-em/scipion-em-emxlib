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

import pyworkflow.em

_logo = "emx_logo.jpg"
_references = ['Marabini2016']


class Plugin(pyworkflow.em.Plugin):
    _homeVar = 'TEST'
    _pathVars = ['TEST']
    _supportedVersions = ['1.0']

    @classmethod
    def _defineVariables(cls):
        cls._defineEmVar('TEST', '.')


pyworkflow.em.Domain.registerPlugin(__name__)
