DEFINE THRESHOLD=40
DEFINE MIC=SensorVal(2)

def main():
    DefineSensors(None,SOUND,None,None)
    while True: 
        while (MIC <= THRESHOLD):
            pass
        
        OnFwd(OUT_AC, 75)
        Wait(300)
         
         
        while (MIC <= THRESHOLD):
           pass

        Off(OUT_AC)
        Wait(300)


