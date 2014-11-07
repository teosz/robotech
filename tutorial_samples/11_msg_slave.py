DEFINE BT_CONN=1
DEFINE INBOX=5
DEFINE OUTBOX=1


def sub_BTCheck(conn):
    
    if (BluetoothStatus(conn)!=NO_ERR):
        TextOut(5,LCD_LINE2,"Error")
        Wait(1000)
        Stop(True)

def main():
    instr=String('')
    outstr=String('')
    iStr=String('')
    
    i=Integer(0)
    sub_BTCheck(0)                #check master connection
    while True:
        iStr = NumToStr(i)
        outstr = StrCat("S",iStr)
        TextOut(10,LCD_LINE1,"Slave Test")
        TextOut(0,LCD_LINE2,"IN:")
        TextOut(0,LCD_LINE4,"OUT:")
        ReceiveRemoteString(INBOX, True, instr)
        SendResponseString(OUTBOX,outstr)
        TextOut(10,LCD_LINE3,instr)
        TextOut(10,LCD_LINE5,outstr)
        Wait(100)
        i+=1
