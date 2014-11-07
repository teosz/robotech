DEFINE MOVE_TIME=500
DEFINE TURN_TIME=360

def main():

    a=5
    
    for repeat in range(a):
        OnFwd(OUT_AC, 75)
        Wait(MOVE_TIME)
        OnRev(OUT_C, 75)
        Wait(TURN_TIME)

    Off(OUT_AC)

