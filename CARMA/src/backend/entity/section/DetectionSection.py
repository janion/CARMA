'''
Created on 28 Sep 2016

@author: Janion
'''

class DetectionSection(object):
    '''
    Holds information about detection points along a section.
    '''

    def __init__(self, checkSignalPin, stopPin, exitPin):
        '''
        Constructor.
        '''
        self.checkSignalPin = checkSignalPin
        self.stopPin = stopPin
        self.exitPin = exitPin

################################################################################

    def getCheckSignalPin(self):
        return self.checkSignalPin

################################################################################

    def getStopPin(self):
        return self.stopPin

################################################################################

    def getExitPin(self):
        return self.exitPin
        