def main():

    OnFwdReg(OUT_AC,50,OUT_REGMODE_IDLE)
    Wait(2000)
    Off(OUT_AC)
    PlayTone(4000,50)
    Wait(1000)
    ResetAllTachoCounts(OUT_AC)
    OnFwdReg(OUT_AC,50,OUT_REGMODE_SPEED)
    Wait(2000)
    Off(OUT_AC)
    PlayTone(4000,50)
    Wait(1000)
    OnFwdReg(OUT_AC,50,OUT_REGMODE_SYNC)
    Wait(2000)
    Off(OUT_AC)
    
