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
import re

from scoreCommon import *


def checkFile(truthPath, testPath):

    truthMatrix = loadFileFromPath(truthPath)
    testMatrix = loadFileFromPath(testPath)
    #print ('TruthMatrix:')
    #print (truthMatrix.shape[0:2])
    #print ('TestMatrix:')
    #print (truthMatrix.shape)

    if testMatrix.shape[0:2] != truthMatrix.shape[0:2]:
        raise ScoreException('Matrix %s has dimensions %s; expected %s.' %
                             (os.path.basename(testPath), testMatrix.shape[0:2],
                              truthMatrix.shape[0:2]))



def scoreP1(truthPath, testPath, FileType):
    truthMatrix = loadFileFromPath(truthPath)
    testMatrix = loadFileFromPath(testPath)

    #print (FileType)
    if FileType == 'AT':
        metrics = computeAT(truthMatrix, testMatrix)
    elif FileType == 'RT':
        metrics = computeRT(truthMatrix, testMatrix)
    else:
        raise ScoreException('Internal error: Unknown file type: %s' % FileType)

    return metrics



def score(truthDir, testDir):
    # Iterate over each file and call scoring executable on the pair
    scores = []
    for truthFile in sorted(os.listdir(truthDir)):

        #print ('This is File List')
        testPath = matchInputFile(truthFile, testDir)
        if testPath == 0:
            continue

        truthPath = os.path.join(truthDir, truthFile)
        #print (truthPath)
        #print (testPath)

        #print ('-----------------------------')

        m = re.search('Phase(\d+)', truthFile)
        PhaseNum = m.group(1)
        #print('PhaseNum: %s') % PhaseNum

        FileName = os.path.splitext(truthFile)[0]
        #print('FileName: %s') % FileName

        FileType = FileName.rsplit('_',1)[1]
        #print('FileType: %s') % FileType

        checkFile(truthPath, testPath)

        if PhaseNum == '1':
            metrics=scoreP1(truthPath, testPath, FileType)
        else:
            raise ScoreException(
                'Error: Only scoring for phase 1 is implemented.')

        #print(metrics)
        #print(FileType)


        scores.append({
            'dataset': FileName,
            'metrics': metrics
        })

    return scores
