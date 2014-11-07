moveMutex=Mutex()

def task_moverandom():

    while True:

        ttt = Random(500) + 40
        tt2 = Random(1)
        Acquire(moveMutex)
        if tt2 > 0:
            OnRev(OUT_A, 75) 
            OnFwd(OUT_C, 75) 
            Wait(ttt)
        else:
            OnRev(OUT_C, 75) 
            OnFwd(OUT_A, 75) 
            Wait(ttt)
            
        ttt = Random(1500) + 50
        OnFwd(OUT_AC, 75)
        Wait(ttt)
        Release(moveMutex)

def task_submain():

    SetSensorType(IN_1, SENSOR_TYPE_LIGHT);
    SetSensorMode(IN_1, SENSOR_MODE_RAW);
    while True:

        if (SENSOR_1 < 100) or (SENSOR_1 > 750):
            Acquire(moveMutex)
            OnRev(OUT_AC, 75); Wait(300)
            Release(moveMutex)

def main():
    Precedes(task_moverandom, task_submain)


