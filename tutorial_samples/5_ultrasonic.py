# in cm
DEFINE NEAR=15

def main():
    DefineSensors(None,None,None,EYES)
    while True:
        OnFwd(OUT_AC,50)
        while SensorVal(4)>NEAR:
            pass
        
        Off(OUT_AC)
        OnRev(OUT_C,100)
        Wait(800)
