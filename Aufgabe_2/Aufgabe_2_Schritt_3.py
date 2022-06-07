import RPi.GPIO as GPIO
import hx711.HX711 as HX711
import time

#  GPIO Pins einrichten
GPIO.setmode(GPIO.BCM)                               # GPIO Modus (BOARD / BCM)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Knopf rote Lampe
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Knopf gelbe Lampe
GPIO.setup(20, GPIO.OUT)                             # Rote Lampe
GPIO.setup(21, GPIO.OUT)                             # Gelbe Lampe

#  Aktualisierungsmethoden
def updateLeer():
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.LOW)

def updateVoll():
    GPIO.output(21, GPIO.HIGH)
    GPIO.output(20, GPIO.LOW)

#  Optionaler Teil
updateLeer()
print('Methode Leer funktioniert!')
time.sleep(3)
updateLeer()
print('Methode Voll funktioniert!')