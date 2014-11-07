#!/usr/bin/env python

from waxy import *
import  wx


class CustomDataTable(wx.grid.PyGridTableBase):
    def __init__(self):
        wx.grid.PyGridTableBase.__init__(self)

        self.colLabels = ['ID', 'Description', 'Severity', 'Priority', 'Platform',
                          'Opened?', 'Fixed?', 'Tested?', 'TestFloat']

        self.dataTypes = [wx.grid.GRID_VALUE_NUMBER,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_CHOICE + ':only in a million years!,wish list,minor,normal,major,critical',
                          wx.grid.GRID_VALUE_NUMBER + ':1,5',
                          wx.grid.GRID_VALUE_CHOICE + ':all,MSW,GTK,other',
                          wx.grid.GRID_VALUE_BOOL,
                          wx.grid.GRID_VALUE_BOOL,
                          wx.grid.GRID_VALUE_BOOL,
                          wx.grid.GRID_VALUE_FLOAT + ':6,2',
                          ]

        self.data = [
            [1010, "The foo doesn't bar", "major", 1, 'MSW', 1, 1, 1, 1.12],
            [1011, "I've got a wicket in my wocket", "wish list", 2, 'other', 0, 0, 0, 1.50],
            [1012, "Rectangle() returns a triangle", "critical", 5, 'all', 0, 0, 0, 1.56]

            ]


    #--------------------------------------------------
    # required methods for the wxPyGridTableBase interface

    def GetNumberRows(self):
        return len(self.data) + 1

    def GetNumberCols(self):
        return len(self.data[0])

    def IsEmptyCell(self, row, col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True

    # Get/Set values in the table.  The Python version of these
    # methods can handle any data-type, (as long as the Editor and
    # Renderer understands the type too,) not just strings as in the
    # C++ version.
    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            return ''

    def SetValue(self, row, col, value):
        try:
            self.data[row][col] = value
        except IndexError:
            # add a new row
            self.data.append([''] * self.GetNumberCols())
            self.SetValue(row, col, value)

            # tell the grid we've added a row
            msg = wx.grid.GridTableMessage(self,            # The table
                    wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, # what we did to it
                    1                                       # how many
                    )

            self.GetView().ProcessTableMessage(msg)


    #--------------------------------------------------
    # Some optional methods

    # Called when the grid needs to display labels
    def GetColLabelValue(self, col):
        return self.colLabels[col]

    # Called to determine the kind of editor/renderer to use by
    # default, doesn't necessarily have to be the same type used
    # natively by the editor/renderer if they know how to convert.
    def GetTypeName(self, row, col):
        return self.dataTypes[col]

    # Called to determine how the data can be fetched and stored by the
    # editor and renderer.  This allows you to enforce some type-safety
    # in the grid.
    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False

    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)



class MyGrid(Grid):
    
    def __init__(self, parent):
        Grid.__init__(self, parent)
        table = CustomDataTable()

        self.SetTable(table, True)

        self.SetRowLabelSize(0)
        self.SetMargins(0,0)
        self.AutoSizeColumns(False)


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
        
        self.grid = MyGrid(self)
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
