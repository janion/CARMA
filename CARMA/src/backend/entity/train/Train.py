'''
Created on 27 Sep 2016

@author: Janion
'''

class Train():
    '''
    Train travelling across the network.
    '''
    
    VERY_FAST = 100
    FAST = 75
    MEDIUM = 50
    SLOW = 25
    STOP = 0

    def __init__(self, name):
        '''
        Constructor.
        '''
        self.name = name
        self.power = self.STOP
        self.occupiedSections = []
        self.axleCount = 0

################################################################################

    def setPower(self, power):
        '''
        Set power supplied to train.
        '''
        self.power = power
        for section in self.occupiedSections:
            section.setPower(power)

################################################################################

    def getPower(self):
        return self.power

################################################################################

    def occupySection(self, section):
        '''
        Add section which is occupied by the train.
        '''
        self.occupiedSections.append(section)

################################################################################

    def unoccupySection(self, section):
        '''
        Remove section which is occupied.
        '''
        self.occupiedSections.remove(section)

################################################################################

    def getSignalState(self):
        '''
        Get state of signal at the end of the nose section and react if necessary.
        '''
        return self.occupiedSections[-1].getSignalState()

################################################################################

    def getNoseSectionName(self):
        '''
        Get name of section on which the front of the train lies.
        '''
        if len(self.occupiedSections) > 0:
            return self.occupiedSections[0].getName()
        else:
            return str(None)

################################################################################

    def getAxleCount(self):
        return self.axleCount

################################################################################

    def getName(self):
        return self.name
        