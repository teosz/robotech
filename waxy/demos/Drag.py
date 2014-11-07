#!/usr/bin/env python

from waxy import *
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
        
        
    def GetRect(self):
        return wx.Rect(self.pos[0], self.pos[1],
                      self.bitmap.GetWidth(), self.bitmap.GetHeight())
        
class MyCanvas(Canvas):

    def Init(self):
        self.SetBackgroundColour('WHITE')
        self.SetScrollbars(20, 20, 100, 100)
        self.sprite = Sprite('heretic2')
        self.sprite.pos=wx.Point(50,50)
        self.selected=False
        self.starting_mouse_pos=None
        self.sprite_orig_pos=None
        
    def OnLeftDown(self,event=None):
        
        if self.sprite.HitTest(event.Position):
            self.selected=True
            self.starting_mouse_pos=event.Position
            self.sprite_orig_pos=self.sprite.pos
            self.sprite.reversed=not self.sprite.reversed
            self.Refresh()
            
    def OnLeftUp(self,event=None):
        self.selected=False

    def OnMotion(self,event=None):
        if not event.Dragging():
            return
            
        if not self.selected:
            return
        
        print "move.",event.Position
        self.sprite.pos=self.sprite_orig_pos+event.Position-self.starting_mouse_pos
            
        self.Refresh()

    
    def OnDraw(self, dc):
        dc.SetTextForeground('BLUE')
        dc.SetPen(wx.MEDIUM_GREY_PEN)
        for i in range(50):
            dc.DrawLine(0, i*10, i*10, 0)

        self.sprite.Draw(dc)
    

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
