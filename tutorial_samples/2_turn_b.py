DEFINE MOVE_TIME=1000
DEFINE TURN_TIME=360

def main():
    OnFwd(OUT_AC, 75)
    Wait(MOVE_TIME)
    OnRev(OUT_C, 75)
    Wait(TURN_TIME)
    Off(OUT_AC)
