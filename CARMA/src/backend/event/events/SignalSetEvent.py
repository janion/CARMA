'''
Created on 27 Sep 2016

@author: Janion
'''

class SignalSetEvent():
    '''
    Event which relates to a signal being set.
    '''
    
    CODE = "S"

    def __init__(self, signalName):
        '''
        Constructor
        '''
        self.entityName = signalName

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
        return message.index(SignalSetEvent.CODE) != -1
    