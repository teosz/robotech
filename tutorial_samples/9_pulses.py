def main():
    SetSensorType(IN_1, SENSOR_TYPE_TOUCH)
    SetSensorMode(IN_1, SENSOR_MODE_PULSE)
    while True:

        ClearSensor(IN_1)
        while SENSOR_1<=0:
            pass
        
        Wait(500)
        if SENSOR_1 == 1:
            Off(OUT_AC)
        if SENSOR_1 == 2:
            OnFwd(OUT_AC, 75)
