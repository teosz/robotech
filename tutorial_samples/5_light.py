DEFINE THRESHOLD=40

def main():
    DefineSensors(None,None,LIGHT,None)
    OnFwd(OUT_AC, 75)
    while True:
        if SensorVal(2) > THRESHOLD:
            OnRev(OUT_C, 75)
            Wait(100)
            
            while SensorVal(2) > THRESHOLD:
                pass
            
            OnFwd(OUT_AC, 75)
