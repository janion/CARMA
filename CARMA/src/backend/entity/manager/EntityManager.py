'''
Created on 28 Sep 2016

@author: Janion
'''
from src.backend.entity.train.Train import Train
from src.backend.entity.section.TrackSection import TrackSection
from src.backend.entity.signal.Signal import Signal
from src.backend.event.scheduler.EventScheduler import EventScheduler
from src.backend.event.events.SectionExitEvent import SectionExitEvent
from src.backend.event.events.CheckSignalEvent import CheckSignalEvent
from src.backend.event.events.StopPointEvent import StopPointEvent

class EntityManager():
    '''
    Manager in charge of creating entities and dealing with events.
    '''

    def __init__(self):
        '''
        Constructor.
        '''
        self.trains = []
        self.sections = []
        self.signals = []
        EventScheduler.subscribeForEvents(self.handle, False)

################################################################################

    def createTrain(self, name):
        if self.isUniqueEntityName(name):
            self.trains.append(Train(name))

################################################################################

    def createSection(self, name):
        if self.isUniqueEntityName(name):
            self.sections.append(TrackSection(name))

################################################################################

    def createSignal(self, name):
        if self.isUniqueEntityName(name):
            self.signals.append(Signal(name))

################################################################################

    def isUniqueEntityName(self, name):
        for train in self.trains:
            if train.getName() == name:
                return False
        
        for section in self.sections:
            if section.getName() == name:
                return False
        
        for signal in self.signals:
            if signal.getName() == name:
                return False
        
        return True

################################################################################

    def getSectionFromName(self, name):
        for section in self.sections:
            if section.getName() == name:
                return section

################################################################################

    def handle(self, event):
        '''
        Handle detection events and set power and signal etc. accordingly.
        '''
        if isinstance(event, CheckSignalEvent):
            self.handleCheckSignalEvent(event)
        elif isinstance(event, StopPointEvent):
            self.handleStopPointEvent(event)
        elif isinstance(event, SectionExitEvent):
            pass

################################################################################

    def handleCheckSignalEvent(self, event):
        section = self.getSectionFromName(event.getEntityName())
        train = section.getTrain()
        signalState = section.getSignalState()
        if signalState == Signal.RED:
            train.setPower(Train.SLOW)

################################################################################

    def handleStopPointEvent(self, event):
        section = self.getSectionFromName(event.getEntityName())
        train = section.getTrain()
        signalState = section.getSignalState()
        if signalState == Signal.RED:
            train.setPower(Train.STOP)
        elif signalState == Signal.GREEN:
            train.setPower(Train.FAST)

################################################################################

    def handleSectionExitEvent(self, event):
        section = self.getSectionFromName(event.getEntityName())
        section.exitDetected()

################################################################################

    def getEntity(self, name):
        for section in self.sections:
            if section.getName() == name:
                return section
        
        for train in self.trains:
            if train.getName() == name:
                return train
        
        for signal in self.signals:
            if signal.getName() == name:
                return signal
        
        return None

################################################################################

    def getTrains(self):
        return self.trains

################################################################################

    def getSections(self):
        return self.sections

################################################################################

    def getSignals(self):
        return self.signals

################################################################################

    def getAllEntityNames(self):
        names = []
        for section in self.sections:
            names.append(section.getName())
        
        for train in self.trains:
            names.append(train.getName())
        
        for signal in self.signals:
            names.append(signal.getName())
        
        return names
        