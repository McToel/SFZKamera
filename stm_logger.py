import time
import serial
import datetime
import pandas as pd

PORT = '/dev/ttyACM1'
BAUDRATE = 9600

print('starting')
serial_device = serial.Serial(PORT, baudrate=BAUDRATE, timeout=10)
time.sleep(5)
data = pd.read_csv('data.csv', index_col=False)
appended_rows = 0
measurements = 0
fails = 0
print('running')
while True:
    if serial_device.in_waiting:
        try:
            time.sleep(0.05)
            measurement = serial_device.readline()
            measurement = measurement[0:len(measurement) - 2].decode("utf-8")
            # print(measurement)
            measurement = measurement.split(',')
            index = len(data)
            data = data.append(pd.Series(dtype=int), ignore_index=True)
            for i, value in enumerate(measurement):
                data.iat[index, i] = int(value)
            data.at[index, 'time'] = datetime.datetime.now()
            appended_rows += 1
            measurements += 1
            if appended_rows > 100:
                data.to_csv('data.csv', index=False)
                appended_rows = 0
            print('measurements:\t', measurements, '\tfails:\t', fails, end='\r')
        except:
            fails += 1
    else:
        time.sleep(0.5)
