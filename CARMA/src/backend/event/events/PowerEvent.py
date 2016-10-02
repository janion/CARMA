'''
Created on 27 Sep 2016

@author: Janion
'''

class PowerEvent():
    '''
    Event which relates to throttle being set on a particular track section.
    '''
    
    CODE = "P"

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
        return True;

################################################################################
    
    @staticmethod
    def isEvent(message):
        return message.index(PowerEvent.CODE) != -1
    