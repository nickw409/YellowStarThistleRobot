#!/user/bin/python3

import subprocess
from gpiozero import Button, LED
from signal import pause
import time
from picamera import PiCamera

button = Button(17)
shut_down_button = Button(2)
led = LED(19)
directory = "/home/pi/py_cam/images/"
camera = PiCamera()
camera.rotation = 180
camera.resolution = (1920, 1080)
#camera.start_preview()
#time.sleep(2)

led.on()

def take_picture():
    current_time_struct = time.localtime()
    current_time = "{}-{}-{}".format(current_time_struct[3],
                                        current_time_struct[4],
                                        current_time_struct[5])
    # subprocess.call(['./webcam.sh'])
    camera.capture(directory + current_time + ".jpg", "jpeg")


def shutdown_pi():
    camera.close()
    subprocess.call(['./shutdown_pi.sh'])

button.when_pressed = take_picture
shut_down_button.when_pressed = shutdown_pi

pause()
