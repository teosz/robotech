#!/usr/bin/env python

from waxy import *

def filltree(tree):
    root = tree.AddRoot("the root item")
    for i in range(10):
        child = tree.AppendItem(root, "Item %d" % (i,))
        for j in range(5):
            grandchild = tree.AppendItem(child, "Item %d" % (i*10+j))

    print [x for x in tree.GetChildNodes(root)]

    d = {
        "Hans": {
            "age": 30,
            "sign": "Aquarius",
            "job": "programmer",
        },
        "Fred": {
            "age": "unknown",
            "sign": "unknown",
            "shoe size": "unknown",
        },
        "Old Guy John": {
            "age": "old",
            "sign": "Aquarius",
        },
        "Bob": {
            "sign": "Taurus",
            "job": "proprietor",
        },
        "Christine": {
            "age": 17,
            "sign": "Aries",
            "job": "cashier",
        }
    }

    stuff = tree.AppendItem(root, "stuff")
    tree.LoadFromDict(stuff, d)

    return tree



class MainFrame(Frame): # frame has a sizer built in

    def Body(self):

        self.CenterOnScreen()

        self.CreateStatusBar()
        self.SetStatusText("This is the statusbar")

        menubar = MenuBar(self)
        menu1 = Menu(self)
        menu1.Append("E&xit", self.CloseWindow, "Exit demo",hotkey="Ctrl+Q")
        menubar.Append(menu1, "&File")
        
        splitter = Splitter(self)
        self.treeview = TreeView(splitter, twist_buttons=1, has_buttons=1)
        self.treeview.OnSelectionChanged = self.OnTreeSelectionChanged
        self.textbox = TextBox(splitter, multiline=1)
        splitter.Split(self.treeview, self.textbox, direction='v')
        self.AddComponent(splitter, expand='both')
        filltree(self.treeview)
        
        
        
        self.Pack()
        self.SetSize((640, 480))

    def CloseWindow(self,event):
        self.Close()

    def OnTreeSelectionChanged(self, event):
        item = event.GetItem()
        data = self.treeview.GetPyData(item)
        if data is None:
            data = self.treeview.GetItemText(item)
        self.textbox.Clear()
        self.textbox.AppendText(str(data))
        event.Skip()




if __name__=="__main__":
    app = Application(MainFrame, title="TreeView")
    app.Run()
