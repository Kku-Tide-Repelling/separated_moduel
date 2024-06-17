import time
import RPi.GPIO as GPIO

PIR_PIN_ONE = 16
PIR_PIN_THREE = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN_ONE, GPIO.IN)
GPIO.setup(PIR_PIN_THREE, GPIO.IN)

def detect_motion():
    time.sleep(1)
    print("찾는중..")
    if GPIO.input(PIR_PIN_ONE) or GPIO.input(PIR_PIN_THREE):
        print("감지!")
        return True
    else:
        print("감지되지 않았습니다.")
        return False
