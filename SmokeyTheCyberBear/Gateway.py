#import libs
import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
import threading

import requests
import pandas as pd
import serial
import time

#create main window
root = tk.Tk()
root.title("GATEWAY")
root.geometry("575x800")

#get a list of available ports
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portList = []

#print available ports
for onePort in ports:
    portList.append(str(onePort))
    print(str(onePort))

#create a dropdown menu for ports and baudrates
#ports
portListCombo = ttk.Combobox(root, width=50, values=portList)
portListCombo.grid(row=0, column=1, padx=10, pady=10)
connectLabel = tk.Label(root, text="Port: ")
connectLabel.grid(row=0, column=0, padx=10, pady=10)
#baudrates
baudLabel = tk.Label(root, text="Baudrate: ")
baudListCombo = ttk.Combobox(root, width=50, values=[10, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000])
baudListCombo.grid(row=1, column=1, padx=10, pady=10)
baudLabel.grid(row=1, column=0, padx=10, pady=10)

data_three = ttk.Treeview(root)
data_three["height"] = 30
data_three["columns"] = ("NAME", "VALUE")
data_three.column("#0", width=0, stretch = tk.NO)
data_three.column("NAME", width=150, minwidth=150, stretch=tk.NO)
data_three.column("VALUE", width=400, minwidth=200)

data_three.heading("NAME", text="VAR_NAME", anchor=tk.W)
data_three.heading("VALUE", text="VAR_VALUE", anchor=tk.W)

data_three.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

def connect():
    global is_connected
    selectedPort = portListCombo.get()
    #split selected port to get only the port name
    portVar = selectedPort.split(" ")
    serialInst.baudrate = baudListCombo.get()
    serialInst.port = portVar[0]
    serialInst.open()
    is_connected = True
    data_three.insert("", "end", values=("IS FIRE PRESENT", "1"))
    data_three.insert("", "end", values=("Latitude", ""))
    data_three.insert("", "end", values=("Longitute", ""))
    data_three.insert("", "end", values=("Node 1", ""))
    data_three.insert(data_three.get_children()[3], "end", values=("NODE ID: ", 0))
    data_three.insert(data_three.get_children()[3], "end", values=("NODE FIRE STATUS: ", 0))
    fire_url="https://firms.modaps.eosdis.nasa.gov/api/area/csv/30f5022fe2bc7ee0c40a6ec180c838a5/VIIRS_SNPP_NRT/world/1"
    fire_data = pd.read_csv(fire_url,usecols = ['latitude','longitude'])

    latest_fire_long=fire_data["longitude"][len(fire_data["longitude"])-1]
    latest_fire_lat=fire_data["latitude"][len(fire_data["latitude"])-1]

    wheather_url="http://api.weatherapi.com/v1/current.json?key=229827838a4a4ee5a69104214230710&q="+str(latest_fire_lat)+" "+str(latest_fire_long)+"&aqi=no"
    response=requests.get(wheather_url)
    data = response.json()
    while is_connected:
        data_three.item(data_three.get_children()[1], values=("Latitude", latest_fire_lat.astype('str')))
        data_three.item(data_three.get_children()[2], values=("Longitute", latest_fire_long.astype('str')))
        serialInst.write((latest_fire_lat.astype('str') + " " + latest_fire_long.astype('str') + " " + str(data['current']['wind_kph'])).encode())
        time.sleep(3)
        packet = serialInst.readline().decode("utf-8")
        print(packet)
        if(packet.isdigit):
            data_three.item(data_three.get_children(data_three.get_children()[3])[1],values=("NODE FIRE STATUS: ", packet))


def disconnect():
    global is_connected
    is_connected = False
    serialInst.close()

#connect button
connectButton = tk.Button(root, text="Connect", command=lambda: threading.Thread(target=connect).start())
connectButton.grid(row=0, column=2, padx=10, pady=10)

#disconnect button
disconnectButton = tk.Button(root, text="Disconnect", command=disconnect)
disconnectButton.grid(row=1, column=2, padx=10, pady=10)

#main loop
root.mainloop()