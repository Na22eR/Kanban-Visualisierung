import RPi.GPIO as GPIO
import time
from threading import Thread

#  GPIO Pins einrichten
GPIO.setmode(GPIO.BCM)                               # GPIO Modus (BOARD / BCM)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Knopf rote Lampe
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Knopf gelbe Lampe
GPIO.setup(20, GPIO.OUT)                             # Rote Lampe
GPIO.setup(21, GPIO.OUT)                             # Gelbe Lampe
GPIO.setup(17, GPIO.OUT)                             # Ultraschallsensor Auslöser
GPIO.setup(24, GPIO.IN)                              # Ultraschallsensor Echo

#  Aktualisierungsmethoden
def updateLeer(channel):
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.LOW)

def updateVoll(channel):
    GPIO.output(21, GPIO.HIGH)
    GPIO.output(20, GPIO.LOW)

#  Event detection & Callback Funktion
GPIO.add_event_detect(18, GPIO.RISING)
GPIO.add_event_detect(19, GPIO.RISING)
GPIO.add_event_callback(18, updateVoll)
GPIO.add_event_callback(19, updateLeer)

def distanz():
    GPIO.output(17, True)

    time.sleep(0.00001)
    GPIO.output(17, False)

    StartZeit = time.time()
    StopZeit = time.time()

    while GPIO.input(24) == 0:
        StartZeit = time.time()

    while GPIO.input(24) == 1:
        StopZeit = time.time()

    TimeElapsed = StopZeit - StartZeit
    distanz = (TimeElapsed * 34300) / 2

    return distanz

#  Endlosschleife Ultraschallsensor
while True:
    abstand = distanz()
    print('Gemessene Entfernung: %.1f cm' % abstand)
    if (abstand > 50):
        print('Kanban-Behälter ist leer.')
        updateLeer(19)
    elif (abstand < 50):
        print('Kanban-Behälter ist gefüllt.')
        updateVoll(18)
    time.sleep(2)