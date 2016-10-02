'''
Created on 27 Sep 2016

@author: Janion
'''

class PowerEvent():
    '''
    Event which relates to throttle being set on a particular track section.
    '''
    
    CODE = "P"

    def __init__(self, sectionName, power):
        '''
        Constructor
        '''
        self.entityName = sectionName
        self.value = power

################################################################################
    
    def getEntityName(self):
        return self.entityName

################################################################################
    
    def getValue(self):
        return self.value

################################################################################
    
    @staticmethod
    def isToHardware():
        return True;

################################################################################
    
    @staticmethod
    def isEvent(message):
        return message.index(PowerEvent.CODE) != -1
    