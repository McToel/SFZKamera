import time
import serial
from picamera import PiCamera
import datetime
import pandas as pd
from multiprocessing import Process, Manager

#ffmpeg -i img%5d.jpg -t 30 timelapse.mp4
#ffmpeg -i chimg%16d.jpg -t 30 timelapse2.mp4
#ffmpeg -framerate 30 -i image%04d.jpg -c:v libx264 -r 30 outputfile.mp4

def serial_listener(port, baudrate):
    print('starting')
    serial_device = serial.Serial(port, baudrate = baudrate, timeout = 10)
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
                measurement = measurement[0:len(measurement)-2].decode("utf-8")
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



if __name__ == '__main__':
    camera = PiCamera()

    mgr = Manager()

    # arduino = serial.Serial('COM4', baudrate = 9600, timeout = 10)
    # stm32 = serial.Serial('COM5', baudrate = 9600, timeout = 10)

    arduino = serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 10)
    # stm32 = serial.Serial('/dev/ttyACM1', baudrate = 9600, timeout = 10)
    time.sleep(5) #wait for the serial to initialize

    start_time = time.time()

    print("running")
    pictureNumber = 0
    last_time = start_time
    try:
        sl = Process(target = serial_listener, args=('/dev/ttyACM1', 9600,))
        sl.start()
        while True:
            #picam
            if(time.time() - last_time) > 60 * 5:
                last_time = time.time()
                arduino.write('ON'.encode('ascii'))
                camera.start_preview()
                time.sleep(10)
                camera.capture('img%s.jpg'%('{0:016d}'.format(time.time() - start_time)))
                camera.capture('static/latest.jpg')))
                camera.stop_preview()
                arduino.write('OFF'.encode('ascii'))

                pictureNumber += 1
            else:
                time.sleep(0.5)
    except KeyboardInterrupt:
        sl.terminate()
        sl.join()