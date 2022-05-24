from tkinter import *
import RPi.GPIO as GPIO
import time
import threading


#  Fenster einrichten
root = Tk()                                          # Fenster
root.geometry('1600x900')                            # Größe
root.wm_title('Kanbanvisualisierung')                # Titel
root.config(background="#FFFFFF")                    # Hintergrundfarbe

#  GPIO Pins einrichten
GPIO.setmode(GPIO.BCM)                               # GPIO Modus (BOARD / BCM)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Knopf rote Lampe
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Knopf gelbe Lampe
GPIO.setup(20, GPIO.OUT)                             # Rote Lampe
GPIO.setup(21, GPIO.OUT)                             # Gelbe Lampe
GPIO_TRIGGER = 17                                    # Int Variablen für GPIO Pin Nummer
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)                   # Ultraschallsensor
GPIO.setup(GPIO_ECHO, GPIO.IN)                       # Ultraschallsensor Echo


#  Aktualisierungsmethoden
def updateLeer(channel):
    Kanban_Voll.grid(row=1, column=1, padx=10, pady=10, sticky='n')
    Kanban_Leer.grid(row=1, column=1, padx=10, pady=10, sticky='n')
    Lampe_Aus.grid_forget()
    Lampe_Aus.grid(row=0, column=2, padx=10, pady=10)
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.LOW)

def updateVoll(channel):
    Kanban_Leer.grid_forget()
    Lampe_Aus.grid_forget()
    Lampe_Aus.grid(row=0, column=0, padx=10, pady=10)
    GPIO.output(21, GPIO.HIGH)
    GPIO.output(20, GPIO.LOW)

def distanz():
    GPIO.output(GPIO_TRIGGER, True)

    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartZeit = time.time()
    StopZeit = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        StartZeit = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()

    TimeElapsed = StopZeit - StartZeit
    distanz = (TimeElapsed * 34300) / 2

    return distanz


#  Event detection & Callback Funktion
GPIO.add_event_detect(18, GPIO.RISING)
GPIO.add_event_detect(19, GPIO.RISING)
GPIO.add_event_callback(18, updateVoll)
GPIO.add_event_callback(19, updateLeer)


class Messung(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        try:
            while True:
                abstand = distanz()
                print('Gemessene Entfernung = %.1f cm' % abstand)
                if abstand > 50:
                    print('Leer')
                    updateLeer(19)

                elif abstand < 50:
                    print('Voll')
                    updateVoll(18)
                time.sleep(10)

            # Beim Abbruch durch STRG+C resetten
        except KeyboardInterrupt:
            print('Messung vom User gestoppt')
            GPIO.cleanup()


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
    messen = Messung()
    root.mainloop()