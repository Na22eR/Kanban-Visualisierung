import RPi.GPIO as GPIO
import time
from tkinter import *
from threading import Thread

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

def messen():
    while True:
        abstand = distanz()
        print('Gemessene Entfernung: %.1f cm' % abstand)
        if (abstand > 50):
            print('Kanban-Behälter ist leer.')
            update(19)
        elif (abstand < 50):
            print('Kanban-Behälter ist gefüllt.')
            update(18)
        time.sleep(2)

#  Separater Thread für den Ultraschallsensor
secondaryThread = Thread(target=messen)
secondaryThread.start()

#  Fenster einrichten
root = Tk()                                          # Fenster
root.geometry('1600x900')                            # Größe
root.wm_title('Kanbanvisualisierung')                # Titel
root.config(background="#FFFFFF")                    # Hintergrundfarbe

#   Definieren GUI-Elemente
framePacker = Frame(root)
Behaelter = Frame(framePacker, width=100, height=200, bg='black')
Kanban_Voll = Frame(framePacker, width=90, height=195, bg='blue')

# Platzieren GUI-Elemente auf Grid
Behaelter.grid(row=1, column=1, padx=10, pady=10)
Kanban_Voll.grid(row=1, column=1, padx=10, pady=10, sticky='n')
Label(framePacker, text='Kanbanbehälter').grid(row=2, column=1, padx=10, pady=10)
framePacker.pack(expand=True)

root.mainloop()