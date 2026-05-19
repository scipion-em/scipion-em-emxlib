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
from pwem import RELATION_CTF
from pwem.protocols import EMProtocol
from pyworkflow.utils import join, exists

from emxlib.constants import *
from emxlib.convert import exportData



class ProtEmxExport(EMProtocol):
    """
    Export micrographs, coordinates or particles to EMX format.

    EMX is a joint initiative for data exchange format between different
    EM software packages.
    """
    """
        Export micrographs, coordinates, particles, or averages into
        EMX format for interoperability between electron microscopy
        software packages. The protocol converts Scipion-compatible
        datasets into standardized EMX files together with their
        associated binary image stacks.

        AI Generated:

        EMX Export (ProtEmxExport) — User Manual

            Overview

            The EMX Export protocol allows the conversion of cryo-EM
            datasets into the EMX exchange format, a standardized format
            designed to facilitate interoperability between different
            electron microscopy software packages. The protocol supports
            the export of micrographs, particle coordinates, particles,
            and class averages together with their associated metadata
            and image files.

            In cryo-EM workflows, EMX export is particularly useful when
            transferring datasets between processing platforms, sharing
            data with collaborators, or preparing standardized datasets
            for external analysis pipelines.

            Inputs and General Workflow

            The protocol requires the selection of an input dataset type,
            including micrographs, coordinates, particles, or averages.
            Depending on the selected type, the protocol dynamically
            adjusts the compatible input object expected from the user.

            For particle datasets, users can choose whether all particles
            should be exported into a single image stack or separated into
            individual stacks associated with each micrograph. When
            exporting micrographs, an optional CTF estimation set can also
            be included in the EMX metadata.

            During execution, the protocol generates an EMX metadata file
            together with the associated binary image stacks in MRC format.
            Users may also define a custom output prefix to control the
            naming of the exported files.

            Outputs and Interpretation

            After completion, the protocol produces a standardized EMX
            dataset containing metadata and image information compatible
            with external cryo-EM software environments. The generated
            files preserve the structural organization and acquisition
            metadata required for downstream processing and data exchange.

            Practical Recommendations

            EMX export is particularly valuable when integrating workflows
            across multiple cryo-EM software packages or when sharing
            datasets between collaborators and facilities. Including CTF
            information during export can improve compatibility with
            downstream processing pipelines that rely on microscope
            correction metadata.

            Final Perspective

            The protocol provides a practical mechanism for standardized
            cryo-EM data exchange, helping users maintain compatibility,
            reproducibility, and interoperability across different
            structural biology software environments.
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
