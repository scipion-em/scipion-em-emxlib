# **************************************************************************
# *
# *  Authors:     Grigory Sharov (gsharov@mrc-lmb.cam.ac.uk)
# *
# * MRC Laboratory of Molecular Biology (MRC-LMB)
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
"""
This file contains constants related to EMX protocols
"""

from collections import OrderedDict

# we declarate global constants to multiple usage
EMXLIB_HOME = 'EMXLIB_HOME'

# Mapping between form parameters and EMX tags
PARAM_DICT = OrderedDict([
                          ('voltage', 'acceleratingVoltage'),
                          ('sphericalAberration', 'cs'),
                          ('amplitudeContrast', 'amplitudeContrast'),
                          ('samplingRate', 'pixelSpacing__X')
                          ])

STACK_SINGLE = 0  # Write all images into a single stack
STACK_MICS = 1  # Write one stack per micrograph
