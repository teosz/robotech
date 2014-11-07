#MASTER

DEFINE BT_CONN=1

def sub_BTCheck(conn):
    if (BluetoothStatus(conn)!=NO_ERR):
        TextOut(5,LCD_LINE2,"Error")
        Wait(1000)
        Stop(True)
        
DEFINE('MOTOR(p,s)',"""RemoteSetOutputState(BT_CONN, p, s, \\
                       OUT_MODE_MOTORON+OUT_MODE_BRAKE+OUT_MODE_REGULATED, \\
                       OUT_REGMODE_SPEED, 0, OUT_RUNSTATE_RUNNING, 0)""")

def main():
    sub_BTCheck(BT_CONN)
    RemotePlayTone(BT_CONN, 4000, 100)
    
    while (BluetoothStatus(BT_CONN)!=NO_ERR):
        pass
    
    Wait(110)
    RemotePlaySoundFile(BT_CONN, "! Click.rso", false)

    while (BluetoothStatus(BT_CONN)!=NO_ERR):
        pass
    
    #Wait(500)
    RemoteResetMotorPosition(BT_CONN,OUT_A,true)

    while (BluetoothStatus(BT_CONN)!=NO_ERR):
        pass
    
    MOTOR(OUT_A,100)
    Wait(1000)
    MOTOR(OUT_A,0)

