'''
Created on 27 Sep 2016

@author: Janion
'''

class CheckSignalEvent():
    '''
    Event which relates to a train needing to check a signal.
    '''
    
    CODE = "C"

    def __init__(self, sectionName):
        '''
        Constructor
        '''
        self.entityName = sectionName

################################################################################
    
    def getEntityName(self):
        return self.entityName

################################################################################
    
    @staticmethod
    def isToHardware():
        return False;

################################################################################
    
    @staticmethod
    def isEvent(message):
        return message.index(CheckSignalEvent.CODE) != -1
    