'''
Created on 27 Sep 2016

@author: Janion
'''
from src.backend.event.scheduler.EventScheduler import EventScheduler
from src.backend.event.events.SignalSetEvent import SignalSetEvent

class Signal():
    '''
    Signal protecting a track section.
    '''
    
    RED = "R"
    GREEN = "G"
    YELLOW = "Y"

    def __init__(self, name):
        '''
        Constructor
        '''
        self.name = name
        self.state = self.RED

################################################################################

    def getState(self):
        return self.state

################################################################################

    def setState(self, state):
        self.state = state
        EventScheduler.scheduleEvent(SignalSetEvent(self.name, state))

################################################################################

    def getName(self):
        return self.name
        