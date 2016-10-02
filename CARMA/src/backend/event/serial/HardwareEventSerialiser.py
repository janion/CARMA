'''
Created on 27 Sep 2016

@author: Janion
'''

from src.backend.event.serial.SerialConnector import SerialConnector
from src.backend.event.scheduler.EventScheduler import EventScheduler

class HardwareEventSerialiser():
    '''
    Serialises events into a form which can be parsed by an associated arduino.
    '''

    def __init__(self, serial):
        '''
        Constructor
        '''
        self.serial = serial
        EventScheduler.subscribeForEvents(self.handle, True)
            
################################################################################

    def handle(self, event):
        '''
        Take an event and serialise it into a form which the associated arduino can parse.
        '''
        eventString = event.getPinNumber() + event.getCode() + event.getProperty() + SerialConnector.FULL_STOP
        self.serial.write(eventString)
