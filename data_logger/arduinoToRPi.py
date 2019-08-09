import serial
from time import sleep
port = "/dev/ttyACM0"

s1 = serial.Serial(port, 9600)
print(s1.name)
s1.flushInput()

sleep(1.5)

while True:
    if s1.inWaiting() > 0:
        input_value = s1.read(1)
        print(ord(input_value))
        #sleep(0.3)
