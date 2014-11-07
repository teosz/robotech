
moveMutex=Mutex()

def task_move_square():
    while True:
        Acquire(moveMutex)
        OnFwd(OUT_AC, 75); Wait(1000)
        OnRev(OUT_C, 75); Wait(500)
        Release(moveMutex)

def task_check_sensors():
  while True:
      if SENSOR_1 == 1:
          Acquire(moveMutex)
          OnRev(OUT_AC, 75); Wait(500)
          OnFwd(OUT_A, 75); Wait(500)
          Release(moveMutex)

def main():
    Precedes(task_move_square, task_check_sensors)
    SetSensorTouch(IN_1)


