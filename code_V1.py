import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(20,GPIO.OUT)
GPIO.output(20,GPIO.LOW)

GPIO.setup(21,GPIO.OUT)
GPIO.output(21,GPIO.LOW)

while True:
    if GPIO.input(19) == GPIO.HIGH:
        GPIO.output(20,GPIO.HIGH)
        GPIO.output(21,GPIO.LOW)
    if GPIO.input(18) == GPIO.HIGH:
        GPIO.output(21,GPIO.HIGH)
        GPIO.output(20,GPIO.LOW)

GPIO.cleanup()

