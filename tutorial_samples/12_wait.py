def main():

    SetSensor(IN_1,SENSOR_TOUCH)
    t3 = CurrentTick()
    OnFwd(OUT_AC, 75)
    
    while (SENSOR_1 != 1) and ((CurrentTick()-t3) <= 1000):
        pass
    
    Off(OUT_AC);


