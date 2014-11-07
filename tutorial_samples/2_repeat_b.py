DEFINE MOVE_TIME=500
DEFINE TURN_TIME=360

def main():

    for repeat in range(10):
        for repeat in range(4):
            
            OnFwd(OUT_AC, 75)
            Wait(MOVE_TIME)
            OnRev(OUT_C, 75)
            Wait(TURN_TIME)

    Off(OUT_AC)
