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

#  Event detection & Callback Funktion
GPIO.add_event_detect(18, GPIO.RISING, callback=updateVoll())
GPIO.add_event_detect(19, GPIO.RISING, callback=updateLeer())

#  Voreinstellungen Gewichtssensor
hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(458)
hx.reset()
hx.tare()
print('Kalibrierung abgeschlossen!')

#  Endlosschleife der Waage
while True:
    val = max(0, int(hx.get_weight(5)))
    print('Kanban-Behälter Inhalt:', val, 'Gramm')
    if (val < 50):
        print('Kanban-Behälter ist leer.')
        updateLeer()
    elif (val > 50):
        print('Kanban-Behälter ist voll.')
        updateVoll()

    hx.power_down()
    hx.power_up()
    time.sleep(2)