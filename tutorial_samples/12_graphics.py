DEFINE X_MAX=99
DEFINE Y_MAX=63
DEFINE X_MID=(X_MAX+1)/2
DEFINE Y_MID=(Y_MAX+1)/2

def main():
    i=1234
    
    TextOut(15,LCD_LINE1,"Display")
    NumOut(60,LCD_LINE1, i)
    PointOut(1,Y_MAX-1)
    PointOut(X_MAX-1,Y_MAX-1)
    PointOut(1,1)
    PointOut(X_MAX-1,1)
    Wait(200)
    RectOut(5,5,90,50)
    Wait(200)
    LineOut(5,5,95,55)
    Wait(200)
    LineOut(5,55,95,5)
    Wait(200)
    CircleOut(X_MID,Y_MID-2,20)
    Wait(800)
    ClearScreen()
    GraphicOut(30,10,"faceclosed.ric")
    Wait(500)
    ClearScreen()
    GraphicOut(30,10,"faceopen.ric")
    Wait(1000)

