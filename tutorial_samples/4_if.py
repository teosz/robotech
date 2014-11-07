DEFINE MOVE_TIME=500
DEFINE TURN_TIME=360

a=0

def main():
    while True:
        
        OnFwd(OUT_AC, 75)
        Wait(MOVE_TIME)
        if Random() > 0:
            OnRev(OUT_C, 75)
        else:
            OnRev(OUT_A, 75)
            
        Wait(TURN_TIME)
