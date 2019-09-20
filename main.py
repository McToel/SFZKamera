#import cv2
import time
import serial
from picamera import PiCamera


#camera = cv2.VideoCapture(0)
camera = PiCamera()

arduino = serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 10)
time.sleep(10) #wait for the arduino to initialize

print("running")
pictureNumber = 0
while True:
    #picam
    #region
    arduino.write('ON'.encode('ascii'))
    camera.start_preview()
    time.sleep(5)
    camera.capture('img%s.jpg'%('{0:05d}'.format(pictureNumber)))
    camera.stop_preview()
    arduino.write('OFF'.encode('ascii'))
    time.sleep(115)
    #endregion 

    #cv2
    #region
    # return_value,image = camera.read()
    # #cv2.imshow('image', image)
    # cv2.imwrite('image%s.jpg'%(pictureNumber),image)
    # time.sleep(30)
    #endregion

    pictureNumber += 1
