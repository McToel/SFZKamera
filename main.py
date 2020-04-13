import time
import serial
from picamera import PiCamera
import datetime
import pandas as pd
from multiprocessing import Process

#ffmpeg -i img%5d.jpg -t 30 timelapse.mp4
#ffmpeg -i chimg%16d.jpg -t 30 timelapse2.mp4
#ffmpeg -framerate 30 -i image%04d.jpg -c:v libx264 -r 30 outputfile.mp4

def serial_listener(serial_device):
    while True:
        if serial_device.in_waiting():
            time.sleep(0.05)
            mesurement = serial_device.readline()
            mesurement = mesurement.split(',')
            index = len(data)
            for i, value in enumerate(mesurement):
                data.iat[index, i] = value
            data.at[index, 'time'] = datetime.datetime.now()
        else:
            time.sleep(0.5)

camera = PiCamera()

data  = pd.DataFrame({'time_smt32_clock':[], 'sensor0':[], 'sensor1':[], 'sensor2':[], 'sensor3':[], 'sensor4':[], 'time':[]})

arduino = serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 10)
stm32 = serial.Serial('/dev/ttyACM1', baudrate = 9600, timeout = 10)
time.sleep(10) #wait for the serial to initialize

start_time = time.time()

print("running")
pictureNumber = 0
last_time = start_time
try:
    sl = Process(target = serial_listener, args=(stm32))
    sl.start()
    while True:
        #picam
        if(time.time() - last_time) > 60 * 5:
            last_time = time.time()
            arduino.write('ON'.encode('ascii'))
            camera.start_preview()
            time.sleep(10)
            camera.capture('img%s.jpg'%('{0:016d}'.format(time.time() - start_time)))
            camera.stop_preview()
            arduino.write('OFF'.encode('ascii'))

            pictureNumber += 1
        else:
            time.sleep(0.5)
except KeyboardInterrupt:
    sl.terminate()
    sl.join()
    data.to_csv('data.csv', index=False)
