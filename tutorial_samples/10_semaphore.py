sem=0  # make sure this one is global

def task_move_square():
    while True:
        while (sem == 1):
            pass
        sem = 1
        OnFwd(OUT_AC, 75)
        sem = 0
        Wait(1000)
        
        while sem==1:
            pass
        
        sem = 1
        
        
        OnRev(OUT_C, 75)
        sem = 0
        Wait(850)

def task_submain():

    SetSensor(IN_1, SENSOR_TOUCH)
    while True:

        if SENSOR_1 == 1:
            while (sem == 1):
                pass
            sem = 1
            OnRev(OUT_AC, 75); Wait(500)
            OnFwd(OUT_A, 75); Wait(850)
            sem = 0

def main():

    sem = 0
    Precedes(task_move_square, task_submain)



