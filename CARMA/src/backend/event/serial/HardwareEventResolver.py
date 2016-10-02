'''
Created on 27 Sep 2016

@author: Janion
'''
from src.backend.event.events.DetectionEvent import DetectionEvent
from src.backend.event.scheduler.EventScheduler import EventScheduler

class HardWareEventResolver():
    '''
    Resolves events from serial messages from the associated arduino.
    '''
    
    HARDWARE_EVENT_TYPES = [DetectionEvent]

    def __init__(self):
        '''
        Constructor
        '''

################################################################################

    def resolve(self, message):
        '''
        Resolve and schedule an event from the message.
        '''
        for eventType in self.HARDWARE_EVENT_TYPES:
            if eventType.isEvent(message):
                event = eventType(message=message)
                EventScheduler.scheduleEvent(self, event)
                break
        