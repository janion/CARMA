'''
Created on 1 Oct 2016

@author: Janion
'''
import wx
import  wx.lib.scrolledpanel as scrolled
from src.backend.event.events.CheckSignalEvent import CheckSignalEvent
from src.backend.event.events.PowerEvent import PowerEvent
from src.backend.event.events.SectionExitEvent import SectionExitEvent
from src.backend.event.events.SignalSetEvent import SignalSetEvent
from src.backend.event.events.StopPointEvent import StopPointEvent
from src.backend.event.scheduler.EventScheduler import EventScheduler
from src.backend.entity.train.Train import Train
from src.backend.entity.section.TrackSection import TrackSection
from src.backend.entity.signal.Signal import Signal
from src.backend.entity.manager.EntityManager import EntityManager

class TestEntity():
    def __init__(self, name):
        self.name = name
        
    def getName(self):
        return self.name

class TestEventWindow(wx.Frame):

    ENTITY_TABLE_TITLES = ["Property", "Value"]
    EVENT_TABLE_TITLES = ["Event type", "Entity", "Value"]
    TRAIN = "Train"
    SECTION = "Section"
    SIGNAL = "Signal"
    ENTITIES = [TRAIN, SECTION, SIGNAL]
    EVENTS = {"CheckSignalEvent" : CheckSignalEvent,
              "PowerEvent" : PowerEvent,
              "SectionExitEvent" : SectionExitEvent,
              "SignalSetEvent" : SignalSetEvent,
              "StopPointEvent" : StopPointEvent
              }
    VALUED_EVENTS = {PowerEvent : int,
                     SignalSetEvent : str
                     }
    
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, pos=(150,150), size=(800,550))
        self.panel = wx.Panel(self)

        self.createMenu()
        
        EventScheduler.subscribeForEvents(self.hardwareEvent, False)
        EventScheduler.subscribeForEvents(self.softwareEvent, True)
        self.manager = EntityManager()

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.createEventInteractionPanel(), 1, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add(self.createNotebooksPanel(), 1, wx.ALL|wx.EXPAND, 5)
        self.populateNotebooks()
        
        self.panel.SetSizer(mainSizer)
        
################################################################################

    def softwareEvent(self, event):
        self.hardwareEvent(event)
        self.populateNotebooks()
        
################################################################################

    def hardwareEvent(self, event):
        eventName = str(event.__class__).split(".")[-1]
        entityName = event.getEntityName()
        value = "N/A"
        if event.isToHardware():
            value = str(event.getValue())
        
        index = self.eventLog.GetItemCount()
        self.eventLog.InsertStringItem(index, eventName)
        self.eventLog.SetStringItem(index, 1, entityName)
        self.eventLog.SetStringItem(index, 2, value)
        
################################################################################

    def createEventInteractionPanel(self):
        eventSizer = wx.BoxSizer(wx.HORIZONTAL)
        eventSizer.Add(self.createEventButtons(), 1, wx.ALL|wx.EXPAND, 5)
        eventSizer.Add(self.createEventLog(), 1, wx.ALL|wx.EXPAND, 5)

        return eventSizer
        
################################################################################

    def createEventButtons(self):
        btnSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer.Add(self.createParametersSizer(), 0, wx.ALL|wx.EXPAND, 0)
        for title in self.EVENTS.keys():
            btn = wx.Button(self.panel, label=title)
            btn.Bind(wx.EVT_BUTTON, self.scheduleEvent)
            btnSizer.Add(btn, 0, wx.ALL|wx.EXPAND, 5)
        
        return btnSizer
        
################################################################################

    def createParametersSizer(self):
        labelSizer = wx.BoxSizer(wx.HORIZONTAL)
        labelSizer.Add(wx.StaticText(self.panel, label="Entity:"), 1, wx.ALL|wx.EXPAND, 0)
        labelSizer.Add(wx.StaticText(self.panel, label="Value:"), 1, wx.ALL|wx.EXPAND, 0)
        
        inputSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.entityBox = wx.Choice(self.panel, choices = self.manager.getAllEntityNames())
        inputSizer.Add(self.entityBox, 1, wx.ALL|wx.EXPAND, 5)
        self.valueBox = wx.TextCtrl(self.panel)
        inputSizer.Add(self.valueBox, 1, wx.ALL|wx.EXPAND, 5)
        
        paramSizer = wx.BoxSizer(wx.VERTICAL)
        paramSizer.Add(labelSizer, 0, wx.ALL|wx.EXPAND, 0)
        paramSizer.Add(inputSizer, 0, wx.ALL|wx.EXPAND, 0)
        
        return paramSizer
        
################################################################################

    def scheduleEvent(self, event):
        btn = event.GetEventObject()
        entityName = self.entityBox.GetStringSelection()
        eventClass = self.EVENTS[btn.GetLabel()]
        
        if not eventClass.isToHardware():
            EventScheduler.scheduleEvent(eventClass(entityName))
        else:
            value = self.VALUED_EVENTS[eventClass](self.valueBox.GetValue())
            EventScheduler.scheduleEvent(eventClass(entityName, value))
        
################################################################################

    def createEventLog(self):
        scrollPane = scrolled.ScrolledPanel(self.panel)
        self.eventLog = wx.ListCtrl(scrollPane, style=wx.LC_REPORT)
        self.eventLog.InsertColumn(0, self.EVENT_TABLE_TITLES[0])
        self.eventLog.InsertColumn(1, self.EVENT_TABLE_TITLES[1])
        self.eventLog.InsertColumn(2, self.EVENT_TABLE_TITLES[2])
        
        scrollSizer = wx.BoxSizer(wx.HORIZONTAL)
        scrollSizer.Add(self.eventLog, 1, wx.ALL|wx.EXPAND, 0)
        scrollPane.SetSizer(scrollSizer)
        
        return scrollPane
        
################################################################################

    def createNotebooksPanel(self):
        trains = self.manager.getTrains()
        self.trainBookSizer = self.createNotebook(self.TRAIN, trains)
        
        sections = self.manager.getSections()
        self.sectionBookSizer = self.createNotebook(self.SECTION, sections)
        
        signals = self.manager.getSignals()
        self.signalBookSizer = self.createNotebook(self.SIGNAL, signals)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.trainBookSizer, 1, wx.ALL|wx.EXPAND, 5)
        sizer.Add(self.sectionBookSizer, 1, wx.ALL|wx.EXPAND, 5)
        sizer.Add(self.signalBookSizer, 1, wx.ALL|wx.EXPAND, 5)
        
        return sizer
        
################################################################################

    def createNotebook(self, title, entities):
        notebookSizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self.panel, label = title)
        notebookSizer.Add(label, 0, wx.ALL|wx.EXPAND, 0)
        
        nb = wx.Notebook(self.panel, size=(21,21), style=wx.BK_DEFAULT)
        for entity in entities:
            scrollPane = scrolled.ScrolledPanel(nb)
            lc = wx.ListCtrl(scrollPane, style=wx.LC_REPORT)
            lc.InsertColumn(0, self.ENTITY_TABLE_TITLES[0])
            lc.InsertColumn(1, self.ENTITY_TABLE_TITLES[1])
            
            scrollSizer = wx.BoxSizer(wx.HORIZONTAL)
            scrollSizer.Add(lc, 1, wx.ALL|wx.EXPAND, 0)
            scrollPane.SetSizer(scrollSizer)
            
            nb.AddPage(scrollPane, entity.getName())

        notebookSizer.Add(nb, 1, wx.ALL|wx.EXPAND, 0)
        return notebookSizer
        
################################################################################

    def populateNotebooks(self):
        # FIXME This is too messy and coupled to the structure
        trainBook = self.trainBookSizer.GetChildren()[1].GetWindow()
        sectionBook = self.sectionBookSizer.GetChildren()[1].GetWindow()
        signalBook = self.signalBookSizer.GetChildren()[1].GetWindow()
        
        self.populateLists(trainBook)
        self.populateLists(sectionBook)
        self.populateLists(signalBook)
        
################################################################################

    def populateLists(self, notebook):
        pageCount = notebook.GetPageCount()
        for i in xrange(pageCount):
            scrollPane = notebook.GetPage(i)
            listCtrl = scrollPane.GetSizer().GetChildren()[0].GetChild()
            listCtrl.DeleteAllItems()
            
            entity = self.manager.getEntity(notebook.GetPageText())
            attributes = self.getEntityAttributes(entity)
            
            for attribute in attributes:
                listCtrl.InsertStringItem(0, attribute[0])
                listCtrl.SetStringItem(0, 1, attribute[1])
        
################################################################################

    def getEntityAttributes(self, entity):
        attributes = []
        if isinstance(entity, Train):
            attributes.append(["Axle count", str(entity.getAxleCount())])
            attributes.append(["Power", str(entity.getPower())])
            attributes.append(["Nose section", entity.getNoseSectionName()])
        elif isinstance(entity, TrackSection):
            attributes.append(["Previous section", entity.GetPreviousSectionName()])
            attributes.append(["Next section", entity.GetNextSectionName()])
            attributes.append(["Signal", entity.GetSignalName()])
            attributes.append(["Power", str(entity.GetPower())])
            attributes.append(["Train", entity.GetTrainName()])
            attributes.append(["Check point passed", entity.GetCheckPointPassed()])
            attributes.append(["Stop point passed", entity.GetStopPointPassed()])
            attributes.append(["Axle count", str(entity.getAxleCount())])
        elif isinstance(entity, Signal):
            attributes.append(["State", entity.GetState()])
        
        return attributes
        
################################################################################

    def createMenu(self):
        # Prepare the menu bar
        menuBar = wx.MenuBar()

        # 1st menu from left
        menu1 = wx.Menu()
        menu1.Append(101, "Create train")
        menu1.Append(102, "Create section")
        menu1.Append(103, "Create signal")
        menu1.AppendSeparator()
        menu1.Append(104, "Close")
        # Add menu to the menu bar
        menuBar.Append(menu1, "File")

        self.SetMenuBar(menuBar)
