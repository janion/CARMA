'''
Created on 27 Sep 2016

@author: Janion
'''
from src.backend.entity.signal.Signal import Signal
from src.backend.event.scheduler.EventScheduler import EventScheduler
from src.backend.event.events.PowerEvent import PowerEvent
from src.backend.entity.train.Train import Train

class TrackSection():
    '''
    Track section which can be occupied by a single train at any given time.
    Each section has associated detection mechanisms, a power mechanism and a signal.
    '''

    def __init__(self, name):
        '''
        Constructor.
        '''
        self.name = name
        self.power = Train.STOP
        self.train = None
        self.previousSection = None
        self.nextSection = None
        self.signal = None
        self.trainPassedCheckPoint = False
        self.trainPassedStopPoint = False
        self.axleCount = 0

################################################################################

    def setPower(self, power):
        '''
        Set power supplied to section and raise powerEvent.
        '''
        self.power = power
        EventScheduler.scheduleEvent(PowerEvent(self.name, power))

################################################################################

    def getSignalState(self):
        '''
        Get state of signal at end of section.
        '''
        self.signal.getState()

################################################################################

    def getDetectionSection(self):
        return self.detectionSection

################################################################################

    def setTrain(self, train):
        '''
        Set train occupying this section and set power accordingly.
        '''
        if train != None:
            train.occupySection(self)
            self.previousSection.setSignalstate(Signal.RED)
            self.setPower(train.getPower())
        else:
            if self.train != None:
                # Unoccupy section if train was on it
                self.train.unoccupySection(self)
            self.previousSection.setSignalstate(Signal.GREEN)
            self.setPower(Train.STOP)
            # Reset event filter booleans
            self.trainPassedCheckPoint = False
            self.trainPassedStopPoint = False
            
        self.train = train

################################################################################

    def setSignalState(self, state):
        '''
        Set state of the signal at the end of this section.
        '''
        self.signal.setState(state)

################################################################################

    def setTrainPassedCheckPoint(self, passed):
        '''
        Set whether train has passed check point.
        '''
        self.trainPassedCheckPoint = passed

################################################################################

    def setTrainPassedStopPoint(self, passed):
        '''
        Set whether train has passed stop point.
        '''
        self.trainPassedStopPoint = passed

################################################################################

    def getTrain(self):
        return self.train

################################################################################

    def exitDetected(self):
        '''
        Train has been detected exiting the section.
        '''
        self.axleCount -= 1
        self.nextSection.entryDetected(self.train)
        if self.axleCount == 0:
            self.setTrain(None)

################################################################################

    def entryDetected(self, train):
        '''
        Train has been detected entering the section.
        '''
        self.axleCount += 1
        if self.train == None:
            self.setTrain(train)

################################################################################

    def getPreviousSectionName(self):
        if self.previousSection != None:
            return self.previousSection.getName()
        else:
            return str(None)

################################################################################

    def getNextSectionName(self):
        if self.nextSection != None:
            return self.nextSection.getName()
        else:
            return str(None)

################################################################################

    def getSignalName(self):
        if self.signal != None:
            return self.signal.getName()
        else:
            return str(None)

################################################################################

    def getPower(self):
        return self.power

################################################################################

    def getTrainName(self):
        if self.train != None:
            return self.train.getName()
        else:
            return str(None)

################################################################################

    def getCheckPointPassed(self):
        return self.trainPassedCheckPoint

################################################################################

    def getStopPointPassed(self):
        return self.trainPassedStopPoint

################################################################################

    def getAxleCount(self):
        return self.axleCount

################################################################################

    def getName(self):
        return self.name
            