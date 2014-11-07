def main():
    t0 = CurrentTick()
    time=0
    
    while time<10000:
        time = CurrentTick()-t0
        OnFwd(OUT_AC, 75)
        Wait(Random(1000))
        OnRev(OUT_C, 75)
        Wait(Random(1000))
  
    
    Off(OUT_AC);

