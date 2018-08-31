# **************************************************************************
# *
# * Authors:     J.M. De la Rosa Trevin (delarosatrevin@scilifelab.se) [1]
# *              Roberto Marabini (roberto@cnb.csic.es) [2]
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

import os

import pyworkflow.protocol.params as params
from pyworkflow.em.protocol import EMProtocol, RELATION_CTF
from pyworkflow.utils.path import join, exists

from emxlib.constants import *
from emxlib.convert import exportData



class ProtEmxExport(EMProtocol):
    """
    Export micrographs, coordinates or particles to EMX format.

    EMX is a joint initiative for data exchange format between different
    EM software packages.
    """
    _label = 'emx export'

    _exportTypes = ['Micrographs',
                    'Coordinates',
                    'Particles',
                    'Averages']

    def __init__(self, **kwargs):
        EMProtocol.__init__(self, **kwargs)

        # We need to trace the changes of 'inputType' to
        # dynamically modify the property of pointerClass
        # of the 'inputSets' parameter
        def onChangeInputType():
            inputText = self.getEnumText('inputType')
            pointerClass = 'SetOf' + inputText
            self.getParam('inputSet').setPointerClass(pointerClass)

        self.inputType.trace(onChangeInputType)

        # --------------------------- DEFINE param functions ------------------

    def _defineParams(self, form):
        form.addSection(label='Input')
        form.addParam('inputType', params.EnumParam,
                      choices=self._exportTypes, default=2,  # Particles
                      label='Input type:',
                      help='Select the type of objects that you want to export.')
        form.addParam('inputSet', params.PointerParam,
                      pointerClass='SetOfMicrographs,SetOfCoordinates,SetOfParticles',
                      label="Set to export", important=True,
                      help="Select the micrographs, coordinates or particles "
                           "set to be exported to EMX.")
        form.addParam('outputStack', params.EnumParam,
                      default=STACK_SINGLE,
                      choices=['single stack', 'one stack per micrograph'],
                      condition='inputType==2',  # for Particles
                      display=params.EnumParam.DISPLAY_LIST,
                      label="Output images",
                      help="Select how you want to export the particles binary file.\n"
                           "*single stack*: write all particles into a single stack.\n"
                           "*one stack per micrograph*: create one stack with particles"
                           " beloging to the same micrograph.")

        form.addParam('ctfEstimation', params.RelationParam,
                      allowsNull=True,
                      condition='inputType==0',  # for Micrographs
                      relationName=RELATION_CTF,
                      attributeName='getInputSet',
                      label='Include CTF from',
                      help='You can select a CTF estimation associated with these '
                           'micrographs to be included in the EMX file')

        form.addParam('outputPrefix', params.StringParam, default='data',
                      label='EMX files prefix',
                      help='Select how do you want to name the EMX files. '
                           'For example, if you use "data" as prefix, two '
                           'files will be generated:\n'
                           '_data.emx_ and _data.mrc_')

    def getInputSet(self):
        return self.inputSet.get()

    # --------------------------- INSERT steps functions ----------------------
    def _insertAllSteps(self):
        self._insertFunctionStep('exportDataStep', self.inputSet.get().getObjId())

    # --------------------------- STEPS functions -----------------------------

    def exportDataStep(self, micsId):
        """ Export micrographs to EMX file.
        micsId is only passed to force redone of this step
        if micrographs change.
        """
        emxDir = self._getPath('emxData')
        xmlFile = self.outputPrefix.get() + '.emx'

        if self.outputStack == STACK_SINGLE:
            binaryFile = self.outputPrefix.get() + '.mrc'
        else:
            binaryFile = None  # None for binary file means to output one
            # stack per micrograph

        exportData(emxDir,
                   self.inputSet.get(),
                   ctfSet=self.ctfEstimation.get(),
                   xmlFile=xmlFile,
                   binaryFile=binaryFile)

    # --------------------------- INFO functions ------------------------------
    def _validate(self):
        errors = []
        return errors

    def _summary(self):
        summary = []
        fname = os.path.abspath(join(self._getPath('emxData'),
                                     self.outputPrefix.get() + '.emx'))
        if exists(fname):
            summary.append('Exported %s to %s' % (
                self._exportTypes[self.inputType.get()], fname))
        return summary

    def _methods(self):
        return self._summary()
