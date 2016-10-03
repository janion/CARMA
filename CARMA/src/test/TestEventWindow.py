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
        trainBookSizer = self.createNotebook(self.TRAIN, trains)
        self.trainBook = trainBookSizer.GetChildren()[1].GetWindow()
        
        sections = self.manager.getSections()
        sectionBookSizer = self.createNotebook(self.SECTION, sections)
        self.sectionBook = sectionBookSizer.GetChildren()[1].GetWindow()
        
        signals = self.manager.getSignals()
        signalBookSizer = self.createNotebook(self.SIGNAL, signals)
        self.signalBook = signalBookSizer.GetChildren()[1].GetWindow()
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(trainBookSizer, 1, wx.ALL|wx.EXPAND, 5)
        sizer.Add(sectionBookSizer, 1, wx.ALL|wx.EXPAND, 5)
        sizer.Add(signalBookSizer, 1, wx.ALL|wx.EXPAND, 5)
        
        return sizer
        
################################################################################

    def createNotebook(self, title, entities):
        notebookSizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self.panel, label = title)
        notebookSizer.Add(label, 0, wx.ALL|wx.EXPAND, 0)
        
        nb = wx.Notebook(self.panel, size=(21,21), style=wx.BK_DEFAULT)
        for entity in entities:
            self.addListPageToNotebook(nb, entity.getName())

        notebookSizer.Add(nb, 1, wx.ALL|wx.EXPAND, 0)
        return notebookSizer
        
################################################################################

    def addListPageToNotebook(self, title, nb):
        scrollPane = scrolled.ScrolledPanel(nb)
        lc = wx.ListCtrl(scrollPane, style=wx.LC_REPORT)
        lc.InsertColumn(0, self.ENTITY_TABLE_TITLES[0])
        lc.InsertColumn(1, self.ENTITY_TABLE_TITLES[1])
        
        scrollSizer = wx.BoxSizer(wx.HORIZONTAL)
        scrollSizer.Add(lc, 1, wx.ALL|wx.EXPAND, 0)
        scrollPane.SetSizer(scrollSizer)
        
        nb.AddPage(scrollPane, title)
        
################################################################################

    def populateNotebooks(self):
        self.populateLists(self.trainBook)
        self.populateLists(self.sectionBook)
        self.populateLists(self.signalBook)
        
################################################################################

    def populateLists(self, notebook):
        pageCount = notebook.GetPageCount()
        for i in xrange(pageCount):
            scrollPane = notebook.GetPage(i)
            listCtrl = scrollPane.GetSizer().GetChildren()[0].GetWindow()
            listCtrl.DeleteAllItems()
            
            entity = self.manager.getEntity(notebook.GetPageText(i))
            attributes = self.getEntityAttributes(entity)
            
            for x in xrange(len(attributes)):
                attribute = attributes[x]
                listCtrl.InsertStringItem(x, attribute[0])
                listCtrl.SetStringItem(x, 1, attribute[1])
        
################################################################################

    def getEntityAttributes(self, entity):
        attributes = []
        if isinstance(entity, Train):
            attributes.append(["Axle count", str(entity.getAxleCount())])
            attributes.append(["Power", str(entity.getPower())])
            attributes.append(["Nose section", entity.getNoseSectionName()])
        elif isinstance(entity, TrackSection):
            attributes.append(["Previous section", entity.getPreviousSectionName()])
            attributes.append(["Next section", entity.getNextSectionName()])
            attributes.append(["Signal", entity.getSignalName()])
            attributes.append(["Power", str(entity.getPower())])
            attributes.append(["Train", entity.getTrainName()])
            attributes.append(["Check point passed", str(entity.getCheckPointPassed())])
            attributes.append(["Stop point passed", str(entity.getStopPointPassed())])
            attributes.append(["Axle count", str(entity.getAxleCount())])
        elif isinstance(entity, Signal):
            attributes.append(["State", entity.getState()])
        
        return attributes
        
################################################################################

    def createMenu(self):
        # Prepare the menu bar
        menuBar = wx.MenuBar()

        # File menu
        menu1 = wx.Menu()
        menu1.Append(101, "Save")
        menu1.Append(102, "Load")
        menu1.AppendSeparator()
        menu1.Append(104, "Close")
        # Add menu to the menu bar
        menuBar.Append(menu1, "File")

        # Entity menu
        menu2 = wx.Menu()
        # Create menu
        menu21 = wx.Menu()
        menu21.Append(2011, self.TRAIN)
        menu21.Append(2012, self.SECTION)
        menu21.Append(2013, self.SIGNAL)
        # Edit menu
        menu22 = wx.Menu()
        menu22.Append(2021, self.TRAIN)
        menu22.Append(2022, self.SECTION)
        menu22.Append(2023, self.SIGNAL)
        # Add submenus to the entity menu
        menu2.AppendMenu(201, "Create", menu21)
        menu2.AppendMenu(201, "Edit", menu22)
        # Add menu to the menu bar
        menuBar.Append(menu2, "Entity")

        self.SetMenuBar(menuBar)
        
        self.Bind(wx.EVT_MENU, self.close, id=104)
        
        self.Bind(wx.EVT_MENU, self.createTrain, id=2011)
        self.Bind(wx.EVT_MENU, self.createSection, id=2012)
        self.Bind(wx.EVT_MENU, self.createSignal, id=2013)
        
################################################################################

    def createTrain(self, event):
        name = self.createEntity("train")
        if name != None:
            self.manager.createTrain(name)
            self.addListPageToNotebook(name, self.trainBook)
            self.populateNotebooks()
        
################################################################################

    def createSection(self, event):
        name = self.createEntity("section")
        if name != None:
            self.manager.createSection(name)
            self.addListPageToNotebook(name, self.sectionBook)
            self.populateNotebooks()
        
################################################################################

    def createSignal(self, event):
        name = self.createEntity("signal")
        if name != None:
            self.manager.createSignal(name)
            self.addListPageToNotebook(name, self.signalBook)
            self.populateNotebooks()
        
################################################################################

    def createEntity(self, entityTypeName):
        dlg = wx.TextEntryDialog(self, 'Enter %s name' %entityTypeName, 'Create %s' %entityTypeName, '')

        isValid = False
        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            if self.manager.isUniqueEntityName(name):
                isValid = True
                self.entityBox.SetItems(self.entityBox.GetItems() + [name])

        dlg.Destroy()
        
        if isValid:
            return name
        else:
            return None
        
################################################################################

    def close(self, event):
        self.Destroy()
