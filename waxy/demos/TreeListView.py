#!/usr/bin/env python

# treelistview-1.py

from waxy import *
import wx
# uses wx at the moment; will be fixed later

class MainFrame(Frame):

    def CreateTreeListView(self, parent):
        treelistview = TreeListView(parent,
                       columns=["Main column", "Column 1", "Column 2"],
                       has_buttons=1, lines=1)
        treelistview.Size = (400, 400)

        # add columns
        treelistview.SetMainColumn(0)
        treelistview.SetColumnWidth(0, 175)

        self.root = treelistview.AddRoot("the root item")
        treelistview.SetItemText(self.root, "col 1 root", 1)
        treelistview.SetItemText(self.root, "col 2 root", 2)

        for x in range(15):
            text = "Item %d" % (x,)
            child = treelistview.AppendItem(self.root, text)
            # child is a TreeItemId or something like that :-(
            treelistview.SetItemText(child, text + "(c1)", 1)
            treelistview.SetItemText(child, text + "(c2)", 2)
            # this should really be something like:
            # child.SetText(column, text)
            # or even:
            # child[column] = text
            # ...can we use a wrapper object without messing up everything?

            for y in range(5):
                text = "Item %d-%d" % (x, y)
                last = treelistview.AppendItem(child, text)
                treelistview.SetItemText(last, text + "(c1)", 1)
                treelistview.SetItemText(last, text + "(c1)", 1)

        return treelistview

    def Body(self):
        self.treelistview = self.CreateTreeListView(self)
        self.AddComponent(self.treelistview, expand='both')
        self.Pack()

app = Application(MainFrame)
app.Run()
