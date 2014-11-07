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
    sub_BTCheck(BT_CONN)
    TextOut(10,LCD_LINE1,"Master sending")
    while True:
        i = Random(512);
        TextOut(0,LCD_LINE3,"                   ")
        NumOut(5,LCD_LINE3,i)
        ack = 0
        SendRemoteNumber(BT_CONN,OUTBOX,i)
        
        while (ack!=0xFF):
            pass
        
        while (ReceiveRemoteNumber(INBOX,true,ack) != NO_ERR):
            pass
        
      
        Wait(250)
