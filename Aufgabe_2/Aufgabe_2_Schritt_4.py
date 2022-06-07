import RPi.GPIO as GPIO
import hx711.HX711 as HX711
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

#  Event detection & Callback Funktion
GPIO.add_event_detect(18, GPIO.RISING, callback=update())
GPIO.add_event_detect(19, GPIO.RISING, callback=update())