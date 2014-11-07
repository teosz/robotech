#!/usr/bin/env python

from waxy import *

# Modified from:
# Recipe 189744: wxPython Graphics - Drawing rubberbands over a canvas 
# http://code.activestate.com/recipes/189744/

class Sprite:
    def __init__(self, fname):
        self.bitmap = Image(fname+".png").ConvertToBitmap()
        self.bitmap_rev = Image(fname+"rev.png").ConvertToBitmap()
        self.background = None
        self.pos=wx.Point(0,0)
        self.reversed=False
        
    def Draw(self, dc):
        # copy background from dc to memory object
        memdc = wx.MemoryDC()
        memdc.Blit(0, 0, self.bitmap.GetWidth(), self.bitmap.GetHeight(), dc,
                   self.pos[0], self.pos[1], wx.COPY, 1)
        self.background = memdc # keep around for later

        bitmap = self.bitmap if not self.reversed else self.bitmap_rev
        dc.DrawBitmap(bitmap, self.pos[0], self.pos[1], 1)
        
    def HitTest(self, pt):
        rect = self.GetRect()
        return rect.InsideXY(pt.x, pt.y)
        
    def Intersects(self, rect):
        myrect = self.GetRect()
        
        # adjust for negative
        arect=[val for val in rect]
        if arect[2]<0:
            arect[0]+=arect[2]
            arect[2]=-arect[2]

        if arect[3]<0:
            arect[1]+=arect[3]
            arect[3]=-arect[3]
        
        return myrect.Intersects(arect)
        
    def GetRect(self):
        return wx.Rect(self.pos[0], self.pos[1],
                      self.bitmap.GetWidth(), self.bitmap.GetHeight())

class MyCanvas(Canvas):

    def Init(self):
        self.SetBackgroundColour('WHITE')
        self.SetScrollbars(20, 20, 100, 100)
        self.sprite = Sprite('heretic2')
        self.sprite.pos=wx.Point(50,50)

        # mouse selection start point
        self.m_stpoint=Point(0,0)
        # mouse selection end point
        self.m_endpoint=Point(0,0)
        # mouse selection cache point
        self.m_savepoint=Point(0,0)
        
        # flags for left click/ selection
        self._leftclicked=False
        self._selected=False

    def OnLeftDown(self,event):
        
        # Left mouse button down, change cursor to
         # something else to denote event capture
         self.m_stpoint = event.GetPosition()
         self.SetCursor('cross')
      
         # invalidate current canvas
         self.Refresh()
         # cache current position
         self.m_savepoint = self.m_stpoint
         self.m_endpoint = self.m_savepoint
         self._selected = False
         self._leftclicked = True


    def OnMotion(self,event):
        
        if event.Dragging() and self._leftclicked:
            
            # Draw new rectangle
            self.m_endpoint =  event.GetPosition()
            self.m_savepoint = self.m_endpoint # cache current endpoint
            self.Refresh()
            
    def OnLeftUp(self,event):
        
        # User released left button, change cursor back
         self.SetCursor('arrow')       
         self._selected = True  #selection is done
         self._leftclicked = False # end of clicking  
         self.Refresh()

    def OnDraw(self, dc):
        dc.SetTextForeground('BLUE')
        dc.SetPen(wx.MEDIUM_GREY_PEN)
        for i in range(50):
            dc.DrawLine(0, i*10, i*10, 0)

        w = (self.m_endpoint.x - self.m_stpoint.x)
        h = (self.m_endpoint.y - self.m_stpoint.y)
        rect=self.m_stpoint.x, self.m_stpoint.y, w, h
        
        if self.sprite.Intersects(rect):
            self.sprite.reversed=True
        else:
            self.sprite.reversed=False

        self.sprite.Draw(dc)

        if not self._selected:
            dc.SetLogicalFunction(wx.XOR)
            wbrush = wx.Brush(wx.Colour(255,255,255), wx.TRANSPARENT)
            wpen = wx.Pen(wx.Colour(200, 200, 200), 1, wx.SOLID)
            dc.SetBrush(wbrush)
            dc.SetPen(wpen)
            
        
            # Set clipping region to rectangle corners
            # dc.SetClippingRegion(self.m_stpoint.x, self.m_stpoint.y, w,h)
            dc.DrawRectangle(*rect) 



    def GetCurrentSelection(self):
        """ Return the current selected rectangle """

        # if there is no selection, selection defaults to
        # current viewport

        left = Point(0,0)
        right = Point(0,0)

        # user dragged mouse to right
        if self.m_endpoint.y > self.m_stpoint.y:
            right = self.m_endpoint
            left = self.m_stpoint
        # user dragged mouse to left
        elif self.m_endpoint.y < self.m_stpoint.y:
            right = self.m_stpoint
            left = self.m_endpoint

        return (left.x, left.y, right.x, right.y)


    def ClearCurrentSelection(self):
        """ Clear the current selected rectangle """

        box = self.GetCurrentSelection()

        dc=wx.ClientDC(self)

        w = box[2] - box[0]
        h = box[3] - box[1]
        dc.SetClippingRegion(box[0], box[1], w, h)
        dc.SetLogicalFunction(wx.XOR)

        # The brush is not really needed since we
        # dont do any filling of the dc. It is set for 
        # sake of completion.

        wbrush = wx.Brush(wx.Colour(255,255,255), wx.TRANSPARENT)
        wpen = wx.Pen(wx.Colour(200, 200, 200), 1, wx.SOLID)
        dc.SetBrush(wbrush)
        dc.SetPen(wpen)
        dc.DrawRectangle(box[0], box[1], w,h)
        self._selected = false 

        # reset selection to canvas size
        self.ResetSelection()    

    def ResetSelection(self):
        """ Resets the mouse selection to entire canvas """

        self.m_stpoint = Point(0,0)
        sz=self._canvas.GetSize()
        w,h=sz.GetWidth(), sz.GetHeight()
        self.m_endpoint = wxPoint(w,h)


class MainFrame(VerticalFrame): # frame has a sizer built in

    def Body(self):


        self.CreateStatusBar()
        self.SetStatusText("This is the statusbar")

        menubar = MenuBar(self)
        menu1 = Menu(self)
        menu1.Append("E&xit", self.CloseWindow, "Exit demo",hotkey="Ctrl+Q")
        menubar.Append(menu1, "&File")


        self.canvas = MyCanvas(self)
        self.canvas.SetSize((400,300))
        self.AddComponent(self.canvas, expand=1, stretch=1)

        self.Pack()

        self.CenterOnScreen()

        self.Show()
        
        
    def CloseWindow(self,event):
        self.Close()



if __name__=="__main__":
    app = Application(MainFrame, title=__file__)
    app.Run()
