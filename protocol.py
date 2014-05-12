# **************************************************************************
# *
# * Authors:     J.M. De la Rosa Trevin (jmdelarosa@cnb.csic.es)
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
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
# *  e-mail address 'jmdelarosa@cnb.csic.es'
# *
# **************************************************************************
"""
In this module are two protocols to Import/Export data from/to EMX.
"""

from pyworkflow.em.protocol import *
from pyworkflow.protocol.params import *


class ProtEmxImport(ProtImport):
    """
    Import micrographs, coordinates or particles from EMX file.
    
    EMX is a joint initiative for data exchange format between different 
    EM software packages. See more about [[http://i2pc.cnb.csic.es/emx][EMX format]]
    """
        
    #--------------------------- DEFINE param functions --------------------------------------------   
    def _defineParams(self, form):
        form.addSection(label='Input')
        form.addParam('inputEMX', FileParam, 
                      label="Input EMX file",
                      help='Provide the path to a valid EMX file.')
                 
    #--------------------------- INSERT steps functions --------------------------------------------  
    def _insertAllSteps(self):
        self._insertFunctionStep('importDataStep', self.inputEMX.get())       

    #--------------------------- STEPS functions --------------------------------------------       
    def importDataStep(self, emxFile):
        """ Export micrographs to EMX file.
        micsId is only passed to force redone of this step if micrographs change.
        """
        from convert import importData
        importData(self, emxFile, outputDir=self._getPath())
    
    #--------------------------- INFO functions -------------------------------------------- 
    def _validate(self):
        errors = []
        return errors
    
    def _citations(self):
        cites = []
        return cites
    
    def _summary(self):
        summary = []
        return summary
    
    def _methods(self):
        return self._summary()  # summary is quite explicit and serve as methods
    
    
class ProtEmxExport(EMProtocol):
    """
    Export micrographs, coordinates or particles to EMX format.
    
    EMX is a joint initiative for data exchange format between different 
    EM software packages. See more about [[http://i2pc.cnb.csic.es/emx][EMX format]]
    """
        
    #--------------------------- DEFINE param functions --------------------------------------------   
    def _defineParams(self, form):
        form.addSection(label='Input')
        form.addParam('inputSet', PointerParam, 
                      pointerClass='SetOfMicrographs,SetOfCoordinates,SetOfParticles', 
                      label="Set to export",
                      help='Select the microgrpahs, coordinates or particles set to be exported to EMX.')
        form.addParam('ctfEstimation', RelationParam, 
                      allowsNull=True, relationName=RELATION_CTF, attributeName='getInputSet', 
                      label='Include CTF from', 
                      help='You can select a CTF estimation associated with these\n'
                           'micrographs to be included in the EMX file')
        
        form.addParam('outputPrefix', StringParam, default='data',
                      label='EMX files prefix',
                      help='Select how do you want to name the EMX files.'
                           'For example, if you use "data" as prefix, two'
                           'files will be generated:\n'
                           '_data.emx_ and _data.mrc_')
                 
    def getInputSet(self):
        return self.inputSet.get()
    
    #--------------------------- INSERT steps functions --------------------------------------------  
    def _insertAllSteps(self):
        self._insertFunctionStep('exportDataStep', self.inputSet.get().getObjId())       

    #--------------------------- STEPS functions --------------------------------------------       
    def exportDataStep(self, micsId):
        """ Export micrographs to EMX file.
        micsId is only passed to force redone of this step if micrographs change.
        """
        from convert import exportData
        emxDir = self._getPath('emxData')
        xmlFile = self.outputPrefix.get() + '.emx'
        binaryFile = self.outputPrefix.get() + '.mrc'
        exportData(emxDir, self.inputSet.get(), ctfSet=self.ctfEstimation.get(), 
                   xmlFile=xmlFile, binaryFile=binaryFile)
        
        self._defineOutputs(emxOutput=EMXObject(join(emxDir, xmlFile), 
                                                join(emxDir, binaryFile)))
    
    #--------------------------- INFO functions -------------------------------------------- 
    def _validate(self):
        errors = []
        return errors
    
    def _citations(self):
        cites = []
        return cites
    
    def _summary(self):
        summary = []
        return summary
    
    def _methods(self):
        return self._summary()  # summary is quite explicit and serve as methods
            
        
