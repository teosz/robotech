#  10 SQUARES
#
#This program make the robot run 10 squares
#
#

# Time for a straight move
DEFINE MOVE_TIME=500
# Time for turning 90 degrees
DEFINE TURN_TIME=360

def main():

    for repeat in range(10):  # Make 10 squares
        for repeat in range(4):
            
            OnFwd(OUT_AC, 75)
            Wait(MOVE_TIME)
            OnRev(OUT_C, 75)
            Wait(TURN_TIME)

    Off(OUT_AC)  # Now turn the motors off

