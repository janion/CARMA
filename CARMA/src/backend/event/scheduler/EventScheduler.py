'''
Created on 27 Sep 2016

@author: Janion
'''

class EventScheduler():
    '''
    Propagates events to subscribers.
    '''
    toHardwareCallBacks = []
    toSoftwareCallBacks = []

    @staticmethod
    def subscribeForEvents(callBack, toHardware):
        '''
        Add callback to handle events.
        '''
        if toHardware:
            EventScheduler.toHardwareCallBacks.append(callBack)
        else:
            EventScheduler.toSoftwareCallBacks.append(callBack)

################################################################################

    @staticmethod
    def scheduleEvent(event):
        '''
        Send event to all subscribers.
        '''
        if event.isToHardware():
            for callBack in EventScheduler.toHardwareCallBacks:
                callBack(event)
        else:
            for callBack in EventScheduler.toSoftwareCallBacks:
                callBack(event)
            