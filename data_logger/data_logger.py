import csv
import sys
import time
import traceback
import serial
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *

def onAttachHandler(self):
    print("Phidget Attached")
    print("Press Enter to end the program.\n")

def onStateChangeHandler(self, state):
    print("State: {}\n".format(state))

def onVoltageRatioChangeHandler(self, voltageRatio):
    self.voltageRatio = voltageRatio
    current_time_struct = time.localtime()
    current_time = "{}:{}:{}".format(current_time_struct[3],
                                        current_time_struct[4],
                                        current_time_struct[5])
    lines = []

    try:
        with open("phidget_output.csv", newline = '') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                lines.append(row)
            #print(lines + "\n")
    except:
        print("File does not exist, creating file.\n")

    with open("phidget_output.csv", 'w') as csvFile:
        writer = csv.writer(csvFile)
        if len(lines) < 1:
            lines.append(['Time', 'Voltage'])
        lines.append([current_time, voltageRatio])
        writer.writerows(lines)
        print("voltage: {}\n".format(voltageRatio))


def main():
    port = "/dev/ttyACM0"
    try:
        print("Trying Aruino Set Up...")
        s1 = serial.Serial(port, 9600)
        if s1.name == port:
            current_time_struct = time.localtime()
            current_time = "{}:{}:{}".format(current_time_struct[3],
                                            current_time_struct[4],
                                            current_time_struct[5])
            s1.flushInput()
            lines = []
            time.sleep(1.5)
        
            try:
                with open("hx711_output.csv", newline = '') as csvFile:
                    print("Successfully found CSV file.\n")
                    reader = csv.reader(csvFile)
            except:
                print("File does not exist, creating file.\n")
                with open("hx711_output.csv", 'w') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerows(["Time", "Weight"])

            with open("hx711_output.csv", 'w') as csvFile:
                print("Successfully opened CSV file for writing\n")
                writer = csv.writer(csvFile)
                while True:
                    current_time_struct = time.localtime()
                    current_time = '{}:{}:{}'.format(current_time_struct[3],
                                                    current_time_struct[4],
                                                    current_time_struct[5])

                    if s1.in_waiting > 0:
                        num_bytes = s1.read(1)
                        weight = s1.read(num_bytes)
                        writer.writerows([current_time, weight])

    except:
        try:
            ch = VoltageRatioInput()
            ch.setOnAttachHandler(onAttachHandler)
            ch.setOnVoltageRatioChangeHandler(onVoltageRatioChangeHandler)
            ch.voltageRatio = 0.0

            try:
                print("Waiting for Attachment")
                ch.openWaitForAttachment(10000)
                ch.setDataInterval(1000)
            except PhidgetException as e:
                print("Attachment Timed Out")

            #time.sleep(10)
        
            #Checks to see if enter has been pressed
            readin = sys.stdin.readline()

            while readin != "\n":
                time.sleep(1)

            ch.close()
            return 0

        except PhidgetException as e:
            sys.stderr.write("\nExiting with error(s)...")
            DisplayError(e)
            traceback.print_exc()
            print("Cleaning up...")
            ch.close()
            return 1
        except RunTimeError as e:
            sys.stderr.write("Runtime Error: \n\t" + e)
            traceback.print_exc()
            return 1


main()


