DEFINE TIME=300
DEFINE MAXVOL=7
DEFINE MINVOL=1
DEFINE MIDVOL=3

DEFINE pause_4th=Wait(TIME)
DEFINE pause_8th=Wait(TIME/2)
DEFINE note_4th=PlayFileEx("! Click.rso",MIDVOL,FALSE); pause_4th
DEFINE note_8th=PlayFileEx("! Click.rso",MAXVOL,FALSE); pause_8th

def main():
    PlayFileEx("! Startup.rso",MINVOL,False)
    Wait(2000)
    note_4th
    note_8th
    note_8th
    note_4th
    note_4th
    pause_4th
    note_4th
    note_4th
    Wait(100)
