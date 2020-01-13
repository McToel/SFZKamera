#import cv2
import time
import serial
from picamera import PiCamera


#ffmpeg -i img%5d.jpg -t 30 timelapse.mp4
#ffmpeg -i chimg%16d.jpg -t 30 timelapse2.mp4

#camera = cv2.VideoCapture(0)
camera = PiCamera()

arduino = serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 10)
time.sleep(10) #wait for the arduino to initialize

start_time = time.time()

print("running")
pictureNumber = 0
while True:
    #picam
    arduino.write('ON'.encode('ascii'))
    camera.start_preview()
    time.sleep(5)
    camera.capture('img%s.jpg'%('{0:016d}'.format(time.time() - start_time)))
    camera.stop_preview()
    arduino.write('OFF'.encode('ascii'))
    time.sleep(115)


    pictureNumber += 1
