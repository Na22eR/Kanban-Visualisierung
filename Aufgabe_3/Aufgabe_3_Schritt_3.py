import RPi.GPIO as GPIO
import time

#  GPIO Pins einrichten
GPIO.setmode(GPIO.BCM)                               # GPIO Modus (BOARD / BCM)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Knopf rote Lampe
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Knopf gelbe Lampe
GPIO.setup(20, GPIO.OUT)                             # Rote Lampe
GPIO.setup(21, GPIO.OUT)                             # Gelbe Lampe
GPIO.setup(17, GPIO.OUT)                             # Ultraschallsensor Auslöser
GPIO.setup(24, GPIO.IN)                              # Ultraschallsensor Echo

#  Aktualisierungsmethode
def update(channel):
    if channel == 19:
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(21, GPIO.LOW)
    if channel == 18:
        GPIO.output(21, GPIO.HIGH)
        GPIO.output(20, GPIO.LOW)

#  Event detection & Callback Funktion
GPIO.add_event_detect(18, GPIO.RISING)
GPIO.add_event_detect(19, GPIO.RISING)
GPIO.add_event_callback(18, update)
GPIO.add_event_callback(19, update)

def distanz():
    GPIO.output(17, GPIO.HIGH)

    time.sleep(0.00001)
    GPIO.output(17, GPIO.LOW)

    StartZeit = time.time()
    StopZeit = time.time()

    while GPIO.input(24) == GPIO.LOW:
        StartZeit = time.time()

    while GPIO.input(24) == GPIO.HIGH:
        StopZeit = time.time()

    TimeElapsed = StopZeit - StartZeit
    distanz = (TimeElapsed * 34300) / 2

    return distanz