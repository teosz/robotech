DEFINE turn_around=OnRev(OUT_B, 75); Wait(3400); a=5; OnFwd(OUT_AB, 75);

def main():
    a=0
    OnFwd(OUT_AB, 75)
    Wait(1000)
    turn_around
    Wait(2000)
    turn_around
    Wait(1000)
    turn_around
    Off(OUT_AB)
    
