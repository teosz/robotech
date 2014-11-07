def inline_turn_around(pwr,turntime):

    OnRev(OUT_C, pwr)
    Wait(turntime)
    OnFwd(OUT_AC, pwr)

def main():

    OnFwd(OUT_AC, 75)
    Wait(1000)
    inline_turn_around(75, 2000)
    Wait(2000)
    inline_turn_around(75, 500)
    Wait(1000)
    inline_turn_around(75, 3000)
    Off(OUT_AC)
