def inline_turn_around():
    OnRev(OUT_C, 75) 
    Wait(900)
    OnFwd(OUT_AC, 75)

def main():

    OnFwd(OUT_AC, 75)
    Wait(1000)
    inline_turn_around()
    Wait(2000)
    inline_turn_around()
    Wait(1000)
    inline_turn_around()
    Off(OUT_AC)
    

