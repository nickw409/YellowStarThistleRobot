import csv
import sys
import time
import traceback
import queue
import os
from gpiozero import Button, LED
from signal import pause
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *

startButton = Button(17)
stopButton = Button(2)
runningLED = LED(19)

def onAttachHandler(self):
    print("Phidget Attached")

def onVoltageRatioChangeHandler(self, voltageRatio):
    self.voltageRatio = voltageRatio
    self.newVoltage = True

def main():
    print("Setting up Phidget...")

    try:
        ch = VoltageRatioInput()
        ch.setOnAttachHandler(onAttachHandler)
        ch.setOnVoltageRatioChangeHandler(onVoltageRatioChangeHandler)
        print("Phidget Set Up.")

    except PhidgetException as e:
        sys.stderr.write("\nExiting with error(s)...")
        print(e)
        print("Cleaning up...")
        ch.close()

    runningLED.on()
    line = []
    testNum = 0

    while 1:
        if startButton.is_pressed:
            testNum += 1
            timeStruct = time.localtime()
            startTime = "{}-{}-{}T{}{}{}".format(timeStruct[0],
                                                    timeStruct[1],
                                                    timeStruct[2],
                                                    timeStruct[3],
                                                    timeStruct[4],
                                                    timeStruct[5])
            output_file = startTime + ".csv"
            simpleQ = startCollecting(ch, testNum, output_file)
            time.sleep(0.5)
            offset = configureOffset(77262, ch.voltageRatio)
            print(offset)
            currentVoltage = ch.voltageRatio
            currentSec = time.time()
            secondsElapsed = 0
            while not stopButton.is_pressed:
                if currentVoltage != ch.voltageRatio:
                    force = 77262 * ch.voltageRatio - offset
                    currentVoltage = ch.voltageRatio
                    force = "{0:.2f}".format(force)
                    print(force)
                    if time.time() - currentSec > 0.9:
                        secondsElapsed += 1
                        currentSec = time.time()
                    seconds = "{}".format(secondsElapsed)
                    simpleQ.put((seconds, force))
            try:
                stopCollecting(ch, testNum, simpleQ, output_file)
                time.sleep(1)

            except error as e:
                print("Something went wrong.")
                print(e)

    pause()

def startCollecting(ch, testNum, output_file):
    print("Starting new test case...")
    output_file = "/home/pi/data_logger/data/" + output_file

    with open(output_file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        line = []
        output = "Test Case Number: {}".format(testNum)
        line.append([output])
        writer.writerows(line)

    try:
        print("Waiting for Attachment...")
        ch.openWaitForAttachment(10000)
        ch.setDataInterval(10)

    except PhidgetException as e:
        print("Failed to attach to Phidget.")
        print(e)
    
    simpleQ = queue.SimpleQueue()
    return simpleQ

def stopCollecting(ch, testNum, simpleQ, output_file):
    print("Stopping Data Collection...")
    output_file = "/home/pi/data_logger/data/" + output_file
    try:
        with open(output_file, 'a') as csvFile:
            writer = csv.writer(csvFile)
            for i in range(simpleQ.qsize()):
                time, force = simpleQ.get()
                data = []
                data.append([time, force])
                writer.writerows(data)
            line = []
            line.append(["Ending Test Case"])
            writer.writerows(line)
            print("Finished")

    except error as e:
        print("Error when writing to output")
        print(e)

    try:
        ch.close()

    except error as e:
        print("Phidget didn't shut down properly")
        print(e)
    print("Phidget Shut Down.")

def configureOffset(slope, voltage):
    return slope * voltage


main()
