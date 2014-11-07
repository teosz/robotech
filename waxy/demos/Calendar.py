#!/usr/bin/env python

from waxy import *
import wx.lib.calendar

class MainFrame(VerticalFrame): # frame has a sizer built in

    def Body(self):

        self.CenterOnScreen()

        self.CreateStatusBar()
        self.SetStatusText("This is the statusbar")

        menubar = MenuBar(self)
        menu1 = Menu(self)
        menu1.Append("E&xit", self.CloseWindow, "Exit demo",hotkey="Ctrl+Q")
        menubar.Append(menu1, "&File")
        
        self.calend = wx.lib.calendar.Calendar(self, -1)
        self.calend.SetCurrentDay()
        self.calend.grid_color = 'BLUE'
        self.calend.SetBusType()
        self.calend.Show(True)
        
        self.Bind(wx.lib.calendar.EVT_CALENDAR, self.MouseClick, self.calend)
        
        
        self.SetSize((640, 480))
        
    def MouseClick(self, evt):
        text = '%s CLICK   %02d/%02d/%d' % (evt.click, evt.day, evt.month, evt.year)  # format date
        print 'Date Selected: ' + text + '\n'

    
        
        
    def CloseWindow(self,event):
        self.Close()

if __name__=="__main__":
    app = Application(MainFrame, title="Calendar")
    app.Run()
