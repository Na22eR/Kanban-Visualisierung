import RPi.GPIO as GPIO
from hx711 import HX711
import time

#  GPIO Pins einrichten
GPIO.setmode(GPIO.BCM)                               # GPIO Modus (BOARD / BCM)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Knopf rote Lampe
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Knopf gelbe Lampe
GPIO.setup(20, GPIO.OUT)                             # Rote Lampe
GPIO.setup(21, GPIO.OUT)                             # Gelbe Lampe

#  Aktualisierungsmethode
def update(channel):
    if channel == 19:
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(21, GPIO.LOW)
    if channel == 18:
        GPIO.output(21, GPIO.HIGH)
        GPIO.output(20, GPIO.LOW)

while True:
    if GPIO.input(19) == GPIO.HIGH:
        update(19)
    if GPIO.input(18) == GPIO.HIGH:
        update(18)