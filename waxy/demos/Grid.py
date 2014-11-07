#!/usr/bin/env python

from waxy import *

class MainFrame(VerticalFrame): # frame has a sizer built in

    def Body(self):


        self.CreateStatusBar()
        self.SetStatusText("This is the statusbar")

        menubar = MenuBar(self)
        menu1 = Menu(self)
        menu1.Append("E&xit", self.CloseWindow, "Exit demo",hotkey="Ctrl+Q")
        menubar.Append(menu1, "&File")
        
        
        self.cellbox=TextBox(self)
        self.AddComponent(self.cellbox,border=10,stretch=True)
        self.cellbox.OnChar=self.EditCell
        
        self.grid = Grid(self,100,40)
        self.AddComponent(self.grid,border=10,expand='both')
        self.grid.OnSelectCell=self.OnSelectCell
        
        self.Pack()
        self.SetSize((1000, 800))
        
        self.CenterOnScreen()

        self.Show()
        self.grid.SetFocus()
        self.cellbox.SetValue(self.grid[0,0])

    def EditCell(self,event):
        
        if event.KeyCode>0 and event.KeyCode<255:  # a character
        
            v=self.cellbox.GetValue()
            r,c=self.grid.GetGridCursorRow(),self.grid.GetGridCursorCol()


            if event.KeyCode==13: # return
                self.grid[r,c]=v
                self.grid.SetFocus()
            elif event.KeyCode==27: # escape
                self.cellbox.SetValue("")
                self.grid.SetFocus()

        event.Skip()
        

    def CloseWindow(self,event):
        self.Close()

    def OnSelectCell(self,event):
        r,c=event.Row,event.Col
        self.cellbox.SetValue(self.grid[r,c])
        event.Skip()
        
        

if __name__=="__main__":
    app = Application(MainFrame, title="Grid")
    app.Run()
