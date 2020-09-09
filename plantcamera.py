import time
import serial
from picamera import PiCamera

PORT = '/dev/ttyACM0'
BAUDRATE = 9600

camera = PiCamera()


arduino = serial.Serial(PORT, baudrate=BAUDRATE, timeout=10)
time.sleep(5)  # wait for the serial to initialize

start_time = time.time()

print("running")
pictureNumber = 0
last_time = start_time
while True:
    # picam
    if (time.time() - last_time) > 60 * 5:
        last_time = time.time()
        arduino.write('ON'.encode('ascii'))
        camera.start_preview()
        time.sleep(10)
        camera.capture('images/img{0:016d}.jpg'.format(time.time() - start_time))
        camera.capture('static/latest.jpg')
        camera.stop_preview()
        arduino.write('OFF'.encode('ascii'))

        pictureNumber += 1
    else:
        time.sleep(0.5)
