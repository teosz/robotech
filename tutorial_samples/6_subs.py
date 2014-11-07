def sub_turn_around(pwr):
    OnRev(OUT_C, pwr); Wait(900)
    OnFwd(OUT_AC, pwr)

def main():
    OnFwd(OUT_AC, 75)
    Wait(1000)
    sub_turn_around(75)
    Wait(2000)
    sub_turn_around(75)
    Wait(1000)
    sub_turn_around(75)
    Off(OUT_AC)
