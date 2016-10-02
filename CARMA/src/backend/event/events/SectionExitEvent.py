'''
Created on 27 Sep 2016

@author: Janion
'''

class SectionExitEvent():
    '''
    Event which relates to a train leaving a section.
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
        return message.index(SectionExitEvent.CODE) != -1
    