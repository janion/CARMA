'''
Created on 28 Sep 2016

@author: Janion
'''
from src.backend.event.events.CheckSignalEvent import CheckSignalEvent
from src.backend.event.events.StopPointEvent import StopPointEvent 
from src.backend.event.events.SectionExitEvent import SectionExitEvent

class EntityResolver():
    '''
    Resolves entities from serial messages.
    '''

    def __init__(self, params):
        '''
        Constructor.
        '''
        # dictionaries of codes to section names
        self.checkSignalCodes = {}
        self.stopPointCodes = {}
        self.leaveSectionCodes = {}

################################################################################

    def createDetectionEvent(self, message):
        '''
        Create detection event from the message.
        '''
        code = self.getPinCode(message)
        
        if code in self.checkSignalCodes.keys():
            return CheckSignalEvent(self.checkSignalCodes[code])
        elif code in self.stopPointCodes.keys():
            return StopPointEvent(self.stopPointCodes[code])
        elif code in self.leaveSectionCodes.keys():
            return SectionExitEvent(self.leaveSectionCodes[code])
        else:
            return None

################################################################################

    def getPinCode(self, message):
        return "code"
        