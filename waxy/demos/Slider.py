#!/usr/bin/env python

from waxy import *
import pylab
import numpy

def myfunc(x,params):

    y=params[0]+params[1]*x+params[2]*x**2
    
    return y
    
    
def myplot(x,y):

    pylab(x,y,'-o')
    title('This is a test')
    xlabel('This')
    ylabel('That')
    
    show()

class MainFrame(VerticalFrame):

    def Body(self):
        self.CenterOnScreen()

        self.CreateStatusBar()
        self.SetStatusText("This is the statusbar")

        menubar = MenuBar(self)
        menu1 = Menu(self)
        menu1.Append("E&xit", self.CloseWindow, "Exit demo",hotkey="Ctrl+Q")
        menubar.Append(menu1, "&File")
        
        
        s=Slider(self,min=-5.0,max=5.0,tickfreq=0.1,ticks='bottom',labels=True)
        self.AddComponent(s,stretch=True)
        s=FloatSlider(self,min=-5.0,max=5.0,tickfreq=0.1,ticks='bottom',labels=True)
        self.AddComponent(s,stretch=True)
        self.Pack()
        self.SetSize((640, 480))

    def CloseWindow(self,event):
        self.Close()                


if __name__=="__main__":
    app = Application(MainFrame, title="Slider Example")
    app.Run()

