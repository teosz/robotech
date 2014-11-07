DEFINE P=40
DEFINE I=40
DEFINE D=70

def main():
    RotateMotorPID(OUT_A, 100, 180, P, I, D)
    Wait(2000)

