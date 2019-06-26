#import cv2
import time
from picamera import PiCamera

#camera = cv2.VideoCapture(0)
pictureNumber = 0
while True:
    #picam
    #region
    camera.start_preview()
    time.sleep(30)
    camera.capture('img%s.jpg'%('{0:05d}'.format(pictureNumber)))
    #endregion 

    #cv2
    #region
    # return_value,image = camera.read()
    # #cv2.imshow('image', image)
    # cv2.imwrite('image%s.jpg'%(pictureNumber),image)
    # time.sleep(30)
    #endregion

    pictureNumber += 1
