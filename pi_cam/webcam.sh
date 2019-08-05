#!/bin/bash

date_taken=$(date +'%Y-%m-%d_%H%M%S')

fswebcam -r 1920x1080 --no-banner -b /home/pi/py_cam/images/$date_taken.jpg

