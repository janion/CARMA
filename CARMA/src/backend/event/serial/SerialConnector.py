'''
Created on 27 Sep 2016

@author: Janion
'''

import serial
from time import sleep
from threading import Thread

from src.backend.event.serial.HardwareEventResolver import HardWareEventResolver
from src.backend.event.serial.HardwareEventSerialiser import HardwareEventSerialiser

class SerialConnector():
    '''
    Connect to a serial port where an arduino is connected
    '''
    
    FULL_STOP = "."
    SLEEP_PERIOD = 50

    def __init__(self, params):
        '''
        Constructor
        '''
        self.initSerial()
        # Create serialiser and resolver
        self.serializer = HardwareEventSerialiser(self.serial)
        self.resolver = HardWareEventResolver()
        # Start a thread to constantly poll the serial connection for messages
        listenerThread = Thread(target=self.monitorSerialEvents, args=() )
        listenerThread.start()
            
################################################################################
                 
    def initSerial(self):
        '''
        Look for a serial connection to the arduino.
        '''
        for x in xrange(9):
            try:
                self.serial = serial.Serial('COM%d' %x, 9600)
#                 init = self.serial.read(self.serial.inWaiting()) # Does this need to happen to trigger the exception?
                break;
            except:
                pass
            
################################################################################
                 
    def monitorSerialEvents(self):
        '''
        Constantly monitor the serial connection for messages.
        '''
        string = ""
        while True:
            try:
                if self.serial.inWaiting() > 0:
                    string += self.serial.read(self.serial.inWaiting())
                    
            except serial.serialutil.SerialException:
                pass
            
            fsIndex = string.index(self.FULL_STOP)
            
            while fsIndex != -1:
                message = string[0 : fsIndex]
                # Remove read message
                string.replace(message + self.FULL_STOP, "")
                self.resolver.resolve(message)
                # Look for next message
                fsIndex = string.index(self.FULL_STOP)
            
            sleep(self.SLEEP_PERIOD)
        