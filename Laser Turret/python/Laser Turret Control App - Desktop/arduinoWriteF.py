import time
from tkinter import messagebox
import json
import serial


def arduinoWriteF(x, arduino):
    try:
        arduino.write(bytes(str(x), 'utf-8'))
        time.sleep(0.5)
    except:
        with open("appWorkingData.json") as asur:
            APPSETTINGS = json.load(asur)
        try:
            messagebox.showinfo("Info", "Due to an unknow error, serial communication is resetting.")
            arduino = serial.Serial(port=f'COM{APPSETTINGS["arduinoPort"]}', baudrate=APPSETTINGS['arduinoSerialCommunicationBaudrate'])
            time.sleep(2)
        except:
            messagebox.showerror("Error connecting to Arduino", f"Make sure you have an Arduino connected on PORT: {APPSETTINGS['arduinoPort']} and running on a BAUDRATE OF: {APPSETTINGS['arduinoSerialCommunicationBaudrate']}")
