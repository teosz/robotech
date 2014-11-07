from numpy import *

from waxy import *

from matplotlib.backends.backend_wxagg import FigureCanvasWx as FigureCanvas
from matplotlib.backends.backend_wx import FigureManager
from matplotlib.figure import Figure
from matplotlib.axes import Subplot

def export_fig(parent,filename=None):
    from matplotlib.backends.backend_pdf import FigureCanvasPdf
    
    if not filename:
    
#        parent.canvas.Show(False)
            
        dlg = FileDialog(parent, "Export to...",default_dir=os.getcwd(),
                        wildcard='PNG Files|*.png|PDF Files|*.pdf|EPS Files|*.eps|SVG Files|*.svg|All Files|*.*',save=1)
        result = dlg.ShowModal()
        if result == 'ok':
            filename = dlg.GetPaths()[0]
        else:
            filename=None

        filter_index=dlg.GetFilterIndex()
            
        dlg.Destroy()

        parent.canvas.Show(True)
        
        
    if filename:
    
        nme,ext=os.path.splitext(filename)
        if not ext:  # do the filter index
            ext='.pdf'
            
            print filter_index
            
            if filter_index==0:
                ext='.png'
            elif filter_index==1:
                ext='.pdf'
            elif filter_index==2:
                ext='.eps'
        
            filename=nme+ext
    
        nme,ext=os.path.splitext(filename)

        if os.path.exists(filename):
            dlg = MessageDialog(parent, '"%s" already exists. Do you want to replace it?' % filename,
            'A file or folder with the same name already exists in plasticity. Replacing it will overwrite its current contents.',icon='warning',cancel=1)
            result = dlg.ShowModal()
            
            if result=='cancel':
                return
        
        if ext=='.pdf': # hack to fix a problem in the pdf backend
            orig_dpi = parent.fig.dpi.get()
            canvas_pdf = FigureCanvasPdf(parent.fig)
            parent.fig.savefig(filename)
            parent.fig.set_canvas(parent.canvas)  # restore automagically switched attributes
            parent.fig.dpi.set(orig_dpi)
        else:
            parent.fig.savefig(filename)



class MainFrame(Frame):

    def __init__(self,x,y,style,parent=None):
        self.fig=None
        Frame.__init__(self,parent,'Plot','H',size=(750,750))
        self.x=x
        self.y=y
        self.style=style
        self.Plot()
        
    def Body(self):
    
        self.CreateMenu()
        self.CenterOnScreen()
        
        self.fig = Figure(figsize=(7,5),dpi=100)
        self.canvas = FigureCanvas(self, -1, self.fig)
        self.figmgr = FigureManager(self.canvas, 1, self)

        self.axes = [self.fig.add_subplot(111)]
        
    def CreateMenu(self):
    
        menubar = MenuBar()

        menu = Menu(self)
        menu.Append("&Run", self.Run, "Run",hotkey="Ctrl+R")
        menu.Append("Export Figure...", self.Export, "Export the Screen")
        menu.Append("&Quit", self.Quit, "Quit",hotkey="Ctrl+Q")

        menubar.Append(menu, "&File")
        self.running=False
        
        self.SetMenuBar(menubar)
        self.CreateStatusBar()

    def Export(self,event=None):
        export_fig(self)
        
    
    def Run(self,event=None):
    
        if self.running:
            self.y=self.y_bak
            self.UpdatePlot()

        else:        
            t=0.0
            self.y_bak=self.y
            
            for t in linspace(0,2*pi*4,100):
                self.y=y*cos(t)
                self.UpdatePlot()

        self.running=not self.running
        
    def UpdatePlot(self):
        self.h.set_ydata(self.y)
        self.canvas.draw()
        self.canvas.gui_repaint()
        wx.Yield()
        
    def Plot(self):
        self.axes[0].clear()
        self.h,=self.axes[0].plot(self.x,self.y,self.style,linewidth=3)
        
        self.canvas.draw()
        self.canvas.gui_repaint()


    def Quit(self,event=None):
        self.Close()

def Plot(x,y,style='-'):
    app = Application(MainFrame,x,y,style)
    app.Run()

if __name__=="__main__":

    x=linspace(-10,10,100)
    y=x*sin(x)+x
    Plot(x,y)
