# slider.py

import wx
import containers
import waxyobject
import styles
from panel import Panel
from label import Label

class Slider(wx.Slider, waxyobject.WaxyObject):
    __events__ = {
        'Scroll': wx.EVT_SCROLL,
    }

    def __init__(self, parent, tickfreq=5, min=0, max=100, event=None, size=None, **kwargs):
        style = 0
        style |= self._params(kwargs)
        style |= styles.window(kwargs)
        
        wx.Slider.__init__(self, parent, wx.NewId(), size=size or (-1,-1), style=style)
        self.SetTickFreq(tickfreq)
        self.SetRange(min, max)
        
        self.BindEvents()
        if event:
            self.OnScroll = event
        styles.properties(self, kwargs)

    #
    # style parameters
    
    __styles__ = {
        'labels': (wx.SL_LABELS, styles.NORMAL),
        'ticks': ({
            "left": wx.SL_LEFT | wx.SL_AUTOTICKS,
            "right": wx.SL_RIGHT | wx.SL_AUTOTICKS,
            "top": wx.SL_TOP | wx.SL_AUTOTICKS,
            "bottom": wx.SL_BOTTOM | wx.SL_AUTOTICKS,
        }, styles.DICTSTART),
        'orientation': ({
            "horizontal": wx.SL_HORIZONTAL,
            "vertical": wx.SL_VERTICAL,
        }, styles.DICTSTART),
    }


class FloatSlider(Panel):

    def __init__(self, parent, tickfreq=0.5, min=-5.0, max=5.0, format='%.1f',event=None, size=None, **kwargs):

        if 'labels' in kwargs:
            labels=kwargs['labels']
            kwargs['labels']=False

        Panel.__init__(self,parent,direction='v')


        intmin=0
        intmax=int(float(max-min)/tickfreq)
        inttickfreq=1

        self.min=min
        self.max=max
        self.tickfreq=tickfreq
        self.format=format

        self.slider=Slider(self, inttickfreq,intmin,intmax,event,size,**kwargs)
        self.slider.SetValue(self.slider.GetMax()/2)
        self.slider.OnScroll=self.OnScroll
        self.AddComponent(self.slider,stretch=True,border=10)

        if labels:
            p=Panel(self,direction='h')
            self.text1=Label(p,self.format % self.min,align='left')
            self.text2=Label(p,self.format % self.max,align='right')
            self.text3=Label(p,self.format % self.GetValue(),align='center')
            p.AddComponent(self.text1,expand=True,border=3)
            p.AddComponent(self.text3,expand=False,border=3)
            p.AddComponent(self.text2,expand=True,border=3)
            p.Pack()

            self.AddComponent(p,stretch=True)



        self.Pack()

    def OnScroll(self,event):
        self.text3.SetLabel(self.format % self.GetValue())
        self.text3.SetExtraStyle(wx.ALIGN_CENTER)
        self.OnUpdate()
        
    def OnUpdate(self):
        pass
        
    def GetValue(self):

        intval=float(self.slider.GetValue())
        intmax=float(self.slider.GetMax())

        val=(intval*self.tickfreq)+self.min

        return val

