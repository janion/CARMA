'''
Created on 1 Oct 2016

@author: Janion
'''
import wx
from src.test.TestEventWindow import TestEventWindow

if __name__ == '__main__':
    app = wx.App()
    fr = TestEventWindow("Test")
    fr.Show()
    app.MainLoop()