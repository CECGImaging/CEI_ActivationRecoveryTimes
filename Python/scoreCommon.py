#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Copyright Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################

import os
import scipy.io
import scipy.stats
import numpy as np
import math



class ScoreException(Exception):
    pass



def matchInputFile(truthFile, testDir):

    truthWithoutExt = os.path.splitext(truthFile)[0]

    testPathCandidates = [
        os.path.join(testDir, testFile)
        for testFile in os.listdir(testDir)
        if (truthWithoutExt == testFile[:len(truthWithoutExt)])
    ]
    #print(testPathCandidates)
    if not testPathCandidates:
        return(0)
        #raise ScoreException('No matching submission for: %s' % truthFile)
    elif len(testPathCandidates) > 1:
        raise ScoreException(
            'Multiple matching submissions for: %s' % truthWithoutExt)
    else:
        return testPathCandidates[0]
    #print(testPathCandidates[0])



def loadFileFromPath(filePath):
    #Load a matlab file as a NumPy array, given a file path
    try:
        #print('Reached .mat reading part')
        file = scipy.io.whosmat(filePath)
        #print(file)
        #print(file[0][0])

        fileMatrix= scipy.io.loadmat(filePath)[file[0][0]]
        #print(fileMatrix)
    except Exception as e:
        raise ScoreException('Could not decode matrix "%s" because: "%s"' % (os.path.basename(filePath), str(e)))

    return fileMatrix



def computeAT(truthVector, testVector):

    (r,pval) = scipy.stats.pearsonr(truthVector, testVector)
    AT_CC = r[0]
    #print(AT_CC)
    
    AT_MAE = np.mean(np.absolute(truthVector-testVector))
    #print(AT_MAE)

    metrics = [
        {
            'name': 'AT_CC',
            'value': AT_CC
        },
        {
            'name': 'AT_MAE',
            'value': AT_MAE
        },
        {
            'name': 'RT_CC',
            'value': None
        },
        {
            'name': 'RT_MAE',
            'value': None
        }
    ]
    return metrics



def computeRT(truthVector, testVector):

    (r,pval) = scipy.stats.pearsonr(truthVector, testVector)
    RT_CC = r[0]
    #print(RT_CC)
    
    RT_MAE = np.mean(np.absolute(truthVector-testVector))
    #print(RT_MAE)

    metrics = [
        {
            'name': 'AT_CC',
            'value': None
        },
        {
            'name': 'AT_MAE',
            'value': None
        },
        {
            'name': 'RT_CC',
            'value': RT_CC
        },
        {
            'name': 'RT_MAE',
            'value': RT_MAE
        }
    ]
    return metrics
