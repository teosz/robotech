DEFINE TURN_TIME=360

def main():
    
    move_time = 200           # set the initial value
    for repeat in range(50):
    
        OnFwd(OUT_AC, 75)
        Wait(move_time)       # use the variable for sleeping
        OnRev(OUT_C, 75)
        Wait(TURN_TIME)
        move_time += 200         # increase the variable

    Off(OUT_AC)
