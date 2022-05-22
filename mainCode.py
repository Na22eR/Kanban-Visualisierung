from tkinter import *
import threading
import smtplib
import ssl
import time
import RPi.GPIO as GPIO



#  GPIO Pins Lampe & Schalter
GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    #Schalter rote Lampe
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    #Schalter gelbe Lampe
GPIO.setup(20,GPIO.OUT)                                #Rote Lampe
GPIO.setup(21,GPIO.OUT)                                #Gelbe Lampe

#  GPIO Pins Ultraschallsensor
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 17
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#  SMTP Einstellungen
tlsContext = ssl.create_default_context()
defaultSMTP = 'smtp.gmail.com'
defaultPort = 587



class GUI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        #  Fenster einrichten
        self.root = Tk()
        self.root.geometry('1600x900')
        self.root.wm_title("Kanbanvisualisierung")  # Fenster Titel
        self.root.config(background="#FFFFFF")  # Hintergrundfarbe des Fensters

        frame = Frame(self.root, width=400, height=400)
        Rotes_Licht = Frame(frame, width=50, height=50, bg='red')
        Gruenes_Licht = Frame(frame, width=50, height=50, bg='yellow')
        Behaelter = Frame(frame, width=100, height=200, bg='black')
        Kanban_Voll = Frame(frame, width=90, height=195, bg='blue')
        Kanban_Leer = Frame(frame, width=90, height=150, bg='grey')
        Lampe_Aus = Frame(frame, width=50, height=50, bg='black')

        #  Platzieren GUI-Elemente auf Grid
        Rotes_Licht.grid(row=0, column=0, padx=10, pady=10)
        Gruenes_Licht.grid(row=0, column=2, padx=10, pady=10)
        Behaelter.grid(row=1, column=1, padx=10, pady=10)
        Kanban_Voll.grid(row=1, column=1, padx=10, pady=10, sticky='n')
        Kanban_Leer.grid(row=1, column=1, padx=10, pady=10, sticky='n')
        Lampe_Aus.grid(row=0, column=2, padx=10, pady=10)

        #  Definieren GUI-Knöpfe
        Label(frame, text='Kanbanbehälter').grid(row=2, column=1, padx=10, pady=10)
        Button(frame, text="Leer", command=GUI.GUI_Leer).grid(row=3, column=0, padx=10, pady=10)
        Button(frame, text="Voll", command=GUI.GUI_Voll).grid(row=3, column=2, padx=10, pady=10)
        frame.pack(expand=True)
        self.root.mainloop()

        #  Aktualisierungsmethoden
        def GUI_Leer():
            Kanban_Voll.grid(row=1, column=1, padx=10, pady=10, sticky='n')
            Kanban_Leer.grid(row=1, column=1, padx=10, pady=10, sticky='n')
            Lampe_Aus.grid_forget()
            Lampe_Aus.grid(row=0, column=2, padx=10, pady=10)
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(21, GPIO.LOW)
            sendEMail('***REMOVED***', '***REMOVED***', "Teeeäst", "Python sagt Hi", "<***REMOVED***>", "<***REMOVED***>")

        def GUI_Voll():
            Kanban_Leer.grid_forget()
            Lampe_Aus.grid_forget()
            Lampe_Aus.grid(row=0, column=0, padx=10, pady=10)
            GPIO.output(21, GPIO.HIGH)
            GPIO.output(20, GPIO.LOW)

        def GPIO_Leer(channel):
            Kanban_Voll.grid(row=1, column=1, padx=10, pady=10, sticky='n')
            Kanban_Leer.grid(row=1, column=1, padx=10, pady=10, sticky='n')
            Lampe_Aus.grid_forget()
            Lampe_Aus.grid(row=0, column=2, padx=10, pady=10)
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(21, GPIO.LOW)
            sendEMail('***REMOVED***', '***REMOVED***', "Teeeäst", "Python sagt Hi", "<***REMOVED***>", "<***REMOVED***>")

        def GPIO_Voll(channel):
            Kanban_Leer.grid_forget()
            Lampe_Aus.grid_forget()
            Lampe_Aus.grid(row=0, column=0, padx=10, pady=10)
            GPIO.output(21, GPIO.HIGH)
            GPIO.output(20, GPIO.LOW)


def sendEMail(username, password, text, subject, mFrom, mTo):
    server = smtplib.SMTP(defaultSMTP, defaultPort)
    server.starttls(context=tlsContext)
    server.login(username, password)
    data = 'From:%s\nTo:%s\nSubject:%s\n\n%s' % (mFrom, mTo, subject, text)
    server.sendmail(mFrom, mTo, data.encode('utf-8'))
    server.quit()
    print('Mail sent! :)')


def distanz():
    # setze Trigger auf HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # setze Trigger nach 0.01ms aus LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartZeit = time.time()
    StopZeit = time.time()

    # speichere Startzeit
    while GPIO.input(GPIO_ECHO) == 0:
        StartZeit = time.time()

    # speichere Ankunftszeit
    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()

    # Zeit Differenz zwischen Start und Ankunft
    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distanz = (TimeElapsed * 34300) / 2

    return distanz


#  Event detection & Callback Funktion
GPIO.add_event_detect(18, GPIO.RISING)
GPIO.add_event_detect(19, GPIO.RISING)
GPIO.add_event_callback(18, GUI.GPIO_Voll)
GPIO.add_event_callback(19, GUI.GPIO_Leer)



#  Main Methode
if __name__ == '__main__':
    GuiFenster = GUI()

    try:
        while True:
            abstand = distanz()
            print("Gemessene Entfernung = %.1f cm" % abstand)
            time.sleep(1)
            if abstand < 50:
                print('Leer')
                # Aufrufen der GPIO und GUI Leer Methode

        # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        GPIO.cleanup()