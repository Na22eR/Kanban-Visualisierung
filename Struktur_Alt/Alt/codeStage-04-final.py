import RPi.GPIO as GPIO
import time
from threading import Thread
from tkinter import *

#  Aktualisierungsmethode
def update(channel):
    if channel == 19:
        Kanban_Voll.grid(row=1, column=1, padx=10, pady=10, sticky='n')
        Kanban_Leer.grid(row=1, column=1, padx=10, pady=10, sticky='n')
        Lampe_Aus.grid_forget()
        Lampe_Aus.grid(row=0, column=2, padx=10, pady=10)
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(21, GPIO.LOW)
    if channel == 18:
        Kanban_Leer.grid_forget()
        Lampe_Aus.grid_forget()
        Lampe_Aus.grid(row=0, column=0, padx=10, pady=10)
        GPIO.output(21, GPIO.HIGH)
        GPIO.output(20, GPIO.LOW)

#  Event detection & Callback Funktion
GPIO.add_event_detect(18, GPIO.RISING)
GPIO.add_event_detect(19, GPIO.RISING)
GPIO.add_event_callback(18, update)
GPIO.add_event_callback(19, update)

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
    try:
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

    # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print('Messung vom User gestoppt')
        GPIO.cleanup()

#  Separater Thread für Waage
secondaryThread = Thread(target=messen)

#  Fenster einrichten
root = Tk()                                          # Fenster
root.geometry('1600x900')                            # Größe
root.wm_title('Kanbanvisualisierung')                # Titel
root.config(background="#FFFFFF")                    # Hintergrundfarbe

#   Definieren GUI-Elemente
frame = Frame(root, width=400, height=400)
Rotes_Licht = Frame(frame, width=50, height=50, bg='red')
Gruenes_Licht = Frame(frame, width=50, height=50, bg='yellow')
Behaelter = Frame(frame, width=100, height=200, bg='black')
Kanban_Voll = Frame(frame, width=90, height=195, bg='blue')
Kanban_Leer = Frame(frame, width=90, height=150, bg='grey')
Lampe_Aus = Frame(frame, width=50, height=50, bg='black')

# Platzieren GUI-Elemente auf Grid
Rotes_Licht.grid(row=0, column=0, padx=10, pady=10)
Gruenes_Licht.grid(row=0, column=2, padx=10, pady=10)
Behaelter.grid(row=1, column=1, padx=10, pady=10)
Kanban_Voll.grid(row=1, column=1, padx=10, pady=10, sticky='n')
Kanban_Leer.grid(row=1, column=1, padx=10, pady=10, sticky='n')
Lampe_Aus.grid(row=0, column=2, padx=10, pady=10)
Label(frame, text='Kanbanbehälter').grid(row=2, column=1, padx=10, pady=10)

frame.pack(expand=True)


#  Main Methode
if __name__ == '__main__':
    secondaryThread.start()
    root.mainloop()