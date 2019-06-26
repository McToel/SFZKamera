import cv2
import time
from picamera import PiCamera

camera.start_preview()
time.sleep(30)
camera.capture('/home/pi/Desktop/image.jpg')
#camera.stop_preview()

camera = cv2.VideoCapture(0)
pictureNumber = 0
while True:
    #picam
    #region
    camera.start_preview()
    time.sleep(30)
    camera.capture('image%s.jpg'%(pictureNumber))
    #endregion 

    #cv2
    #region
    # return_value,image = camera.read()
    # #cv2.imshow('image', image)
    # cv2.imwrite('image%s.jpg'%(pictureNumber),image)
    # time.sleep(30)
    #endregion

    pictureNumber += 1