#SLAVE

DEFINE BT_CONN=1
DEFINE OUTBOX=5
DEFINE INBOX=1

def sub_BTCheck(conn):
    if (BluetoothStatus(conn)!=NO_ERR):
        TextOut(5,LCD_LINE2,"Error")
        Wait(1000)
        Stop(True)
        

def main():
    numin=Integer()
    
    sub_BTCheck(0)
    TextOut(5,LCD_LINE1,"Slave receiving")
    SendResponseNumber(OUTBOX,0xFF) #unblock master
    while True:
        if (ReceiveRemoteNumber(INBOX,true,numin) != STAT_MSG_EMPTY_MAILBOX):
            TextOut(0,LCD_LINE3,"                   ");
            NumOut(5,LCD_LINE3,numin);
            SendResponseNumber(OUTBOX,0xFF);
     
        Wait(10); #take breath (optional)
