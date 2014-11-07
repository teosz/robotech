
def main():
    DefineSensors(TOUCH,None,None,None)
    OnFwd(OUT_AC, 75)
    while True:
        if SensorVal(1) == 1:
        
            OnRev(OUT_AC, 75); Wait(300)
            OnFwd(OUT_A, 75); Wait(300)
            OnFwd(OUT_AC, 75)
