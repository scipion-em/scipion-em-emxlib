# **************************************************************************
# *
# * Authors:     Roberto Marabini (roberto@cnb.csic.es) [1]
# *              J.M. De la Rosa Trevin (delarosatrevin@scilifelab.se) [2]
# *
# * [1] SciLifeLab, Stockholm University
# * [2] Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
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

import pyworkflow.gui.text as text
from pyworkflow.em.viewers import DataView
from pyworkflow.viewer import Viewer, DESKTOP_TKINTER, WEB_DJANGO

from emxlib.protocols import ProtEmxExport


class EMXViewer(Viewer):
    """ Class to visualize Relion protocols """
    _environments = [DESKTOP_TKINTER, WEB_DJANGO]
    _targets = [ProtEmxExport]
    _label = 'viewer emx'
    
    def __init__(self, **args):
        Viewer.__init__(self, **args)

    def visualize(self, obj, **args):
        data = self.protocol._getPath('emxData/data.mrc')
        DataView(data).show()

        # open EMX file in web browser
        fn = self.protocol._getPath('emxData/data.emx')
        text._open_cmd(fn, self.getTkRoot())
