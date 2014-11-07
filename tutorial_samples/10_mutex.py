moveMutex=Mutex()

def task_move_square():

    while True:
        Acquire(moveMutex)
        OnFwd(OUT_AC, 75); Wait(1000)
        OnRev(OUT_C, 75); Wait(850)
        Release(moveMutex)

def task_check_sensors():

    while True:
        if SENSOR_1 == 1:
        
            Acquire(moveMutex)
            OnRev(OUT_AC, 75); Wait(500)
            OnFwd(OUT_A, 75); Wait(850)
            Release(moveMutex)
            
def main():
    SetSensor(IN_1,SENSOR_TOUCH)
    Precedes(task_check_sensors, task_move_square)


