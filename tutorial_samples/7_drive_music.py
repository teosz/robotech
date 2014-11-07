def task_music():
    while True:
        PlayTone(262,400);  Wait(500);
        PlayTone(294,400);  Wait(500);
        PlayTone(330,400);  Wait(500);
        PlayTone(294,400);  Wait(500);

def task_movement():

    while True:
        OnFwd(OUT_AC, 75); Wait(3000);
        OnRev(OUT_AC, 75); Wait(3000);

def main():
    Precedes(task_music, task_movement);
