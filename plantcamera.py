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
while True:
    last_time = time.time()
    arduino.write('ON\n'.encode('ascii'))
    camera.start_preview()
    time.sleep(10)
    camera.capture('images/img{0:016d}.jpg'.format(int(time.time() - start_time)))
    camera.capture('static/latest.jpg')
    camera.stop_preview()
    arduino.write('OFF\n'.encode('ascii'))

    pictureNumber += 1

    time.sleep((60 * 5) - ((time.time() - start_time) % (60 * 5)))
