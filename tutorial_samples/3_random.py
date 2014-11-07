def main():

    while True:
        move_time = Random(600)   # default type is an integer
        turn_time = Random(400)
        OnFwd(OUT_AC, 75)
        Wait(move_time)
        OnRev(OUT_A, 75)
        Wait(turn_time)
