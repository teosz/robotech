# grid.py

# todo: styles

import wx
import wx.grid as gridlib
import waxyobject

class Grid(gridlib.Grid, waxyobject.WaxyObject):

    __events__ = {
        'CellLeftClick': gridlib.EVT_GRID_CELL_LEFT_CLICK,
        'CellRightClick': gridlib.EVT_GRID_CELL_RIGHT_CLICK,
        'CellLeftDoubleClick': gridlib.EVT_GRID_CELL_LEFT_DCLICK,
        'CellRightDoubleClick': gridlib.EVT_GRID_CELL_RIGHT_DCLICK,
        'LabelLeftClick': gridlib.EVT_GRID_LABEL_LEFT_CLICK,
        'LabelRightClick': gridlib.EVT_GRID_LABEL_RIGHT_CLICK,
        'LabelLeftDoubleClick': gridlib.EVT_GRID_LABEL_LEFT_DCLICK,
        'LabelRightDoubleClick': gridlib.EVT_GRID_LABEL_RIGHT_DCLICK,
        'RowSize': gridlib.EVT_GRID_ROW_SIZE,
        'ColSize': gridlib.EVT_GRID_COL_SIZE,
        'RangeSelect': gridlib.EVT_GRID_RANGE_SELECT,
        'CellChange':gridlib.EVT_GRID_CELL_CHANGE,
        'SelectCell':gridlib.EVT_GRID_SELECT_CELL,
        'EditorShown':gridlib.EVT_GRID_EDITOR_SHOWN, 
        'EditorHidden':gridlib.EVT_GRID_EDITOR_HIDDEN,
        'EditorCreated':gridlib.EVT_GRID_EDITOR_CREATED,
    }


    def __init__(self, parent, numrows=10, numcolumns=10):
        gridlib.Grid.__init__(self, parent, wx.NewId())
        self.CreateGrid(numrows, numcolumns)
        self.BindEvents()
        
    def SetGlobalSize(self, rowsize, colsize):
        """ Set all cells to the same size. """
        for i in range(self.GetNumberRows()):
            self.SetRowSize(i, rowsize)
        for i in range(self.GetNumberCols()):
            self.SetColSize(i, colsize)

    def __setitem__(self, index, value):
        assert isinstance(index, tuple) and len(index) == 2
        row, column = index
        self.SetCellValue(row, column, value)

    def __getitem__(self, index):
        assert isinstance(index, tuple) and len(index) == 2
        row, column = index
        return self.GetCellValue(row, column)

