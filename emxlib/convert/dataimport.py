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

from os.path import join, dirname, exists
from collections import OrderedDict

from pyworkflow.em.constants import ALIGN_NONE

import emxlib.utils as utils
from emxlib.constants import *



class EmxImport():
    """
    Import micrographs, coordinates or particles from EMX file.

    EMX is a joint initiative for data exchange format between different
    EM software packages.
    """


    def __init__(self, protocol, emxFile, alignType=ALIGN_NONE):
        self.protocol   = protocol
        self._emxFile   = emxFile
        self.copyOrLink = protocol.getCopyOrLink()
        self.alignType  = alignType

    def _loadEmxInfo(self):
        """ Load the EMX file and get some information about the type
        of objects contained and the binary data.
        """
        emxData = utils.EmxData()

        emxDir = dirname(self._emxFile)
        self.classElement = None
        self.binaryFile = None
        self.object = None
        self.objDict = {} # store the first object of each class

        for classElement in utils.CLASSLIST:
            obj = emxData.readFirstObject(classElement, self._emxFile)
            if obj is not None:
                self.objDict[classElement] = obj
                #is the binary file of this type
                binaryFile = join(emxDir, obj.get(utils.FILENAME))
                if exists(binaryFile):
                    self.object = obj
                    self.binaryFile = binaryFile
                    self.classElement = classElement

    def loadAcquisitionInfo(self):
        """ Try to read acquistion from input file. """
        acquisitionDict = OrderedDict()

        if exists(self._emxFile):
            self._loadEmxInfo()

            for k, v in PARAM_DICT.iteritems():
                # Read from the EMX files the values and fill acquisition
                if self.object.get(v) is not None:
                    acquisitionDict[k] = self.object.get(v)

        return acquisitionDict

    #--------------------------- STEPS functions --------------------------------------------
    def importData(self):
        """ Import micrographs, coordinates and particles from EMX file.
        If the file contains information about the CTF, it will be also
        taken into account.
        """
        prot = self.protocol
        acquisition = prot.getAcquisition()
        from convert import importData
        #emxFile=self._getRelPathExecutionDir(emxFile)
        importData(prot, self._emxFile, prot._getExtraPath(),
                   acquisition, prot.samplingRate.get(), self.copyOrLink,
                   self.alignType)

    def importMicrographs(self):
        self.importData()

    def importParticles(self):
        self.importData()

    #--------------------------- INFO functions --------------------------------------------
    def validate(self, objectClassName):
        """ Do some validation about the input EMX file.
        Params:
            objectClassName: it could be either (MICROGRAPHS or PARTICLES)
        """
        emxFile = self._emxFile
        errors = []
        # Check that input EMX file exist
        if not exists(emxFile):
            errors.append("Input EMX file doesn't exists:\n*%s*" % emxFile)
        else:
            self._loadEmxInfo()
            if self.object is None:
                errors.append("Cannot find any object in EMX file:\n*%s*" % emxFile)
            else:
                if self.binaryFile is None:
                    errors.append("Cannot find binary data *%s* associated with EMX metadata file.\n" % self.binaryFile)

                if objectClassName not in self.objDict:
                    errors.append("EMX object *%s* not found in EMX file:\n*%s*" % emxFile)

        if self.alignType != ALIGN_NONE:
            f = open(emxFile)
            if not 'transformationMatrix' in f.read():
                errors.append("Align type different from None, but no transformation matrix found in file %s*" % emxFile)
            f.close()
        return errors

    def validateMicrographs(self):
        return self.validate(utils.MICROGRAPH)

    def validateParticles(self):
        return self.validate(utils.PARTICLE)
