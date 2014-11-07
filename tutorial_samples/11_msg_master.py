#MASTER

DEFINE BT_CONN=1
DEFINE OUTBOX=5
DEFINE INBOX=1

def sub_BTCheck(conn):
    if (BluetoothStatus(conn)!=NO_ERR):
        TextOut(5,LCD_LINE2,"Error")
        Wait(1000)
        Stop(True)

def main():
    instr=String()
    outstr=String()
    iStr=String()
    
    i=Integer(0)
    
    sub_BTCheck(BT_CONN)  #check slave connection
    while True:
        iStr = NumToStr(i)
        outstr = StrCat("M",iStr)
        TextOut(10,LCD_LINE1,"Master Test")
        TextOut(0,LCD_LINE2,"IN:")
        TextOut(0,LCD_LINE4,"OUT:")
        ReceiveRemoteString(INBOX, True,instr)
        #  SendRemoteString(BT_CONN,OUTBOX,outstr)  # for some reason, this line doesn't work!  
        TextOut(10,LCD_LINE3,instr)
        TextOut(10,LCD_LINE5,outstr)
        Wait(100)
        i+=1
