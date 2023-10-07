import requests
import pandas as pd
import serial
import time


serialInst = serial.Serial()
selectedPort = 'COM16'
serialInst.baudrate = 115200
serialInst.port = selectedPort
serialInst.open()
while 1:    
    fire_url="https://firms.modaps.eosdis.nasa.gov/api/area/csv/30f5022fe2bc7ee0c40a6ec180c838a5/VIIRS_SNPP_NRT/world/1"
    fire_data = pd.read_csv(fire_url,usecols = ['latitude','longitude'])

    latest_fire_long=fire_data["longitude"][len(fire_data["longitude"])-1]
    latest_fire_lat=fire_data["latitude"][len(fire_data["latitude"])-1]
    print(latest_fire_lat)
    print(latest_fire_long)

    wheather_url="http://api.weatherapi.com/v1/current.json?key=229827838a4a4ee5a69104214230710&q="+str(latest_fire_lat)+" "+str(latest_fire_long)+"&aqi=no"

    response=requests.get(wheather_url)

    data = response.json()
    #time.sleep(3600)
    while 1:

        serialInst.write((latest_fire_lat.astype('str') + " " + latest_fire_long.astype('str') + " " + str(data['current']['wind_kph'])).encode())
    
        if serialInst.in_waiting:
            packet = serialInst.readline()
            print(packet)
        time.sleep(3)