from tkinter import *
import RPi.GPIO as GPIO


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


#  Aktualisierungsmethoden
def GUI_Leer():
    Kanban_Voll.grid(row=1, column=1, padx=10, pady=10, sticky='n')
    Kanban_Leer.grid(row=1, column=1, padx=10, pady=10, sticky='n')
    Lampe_Aus.grid_forget()
    Lampe_Aus.grid(row=0, column=2, padx=10, pady=10)
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.LOW)

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

def GPIO_Voll(channel):
    Kanban_Leer.grid_forget()
    Lampe_Aus.grid_forget()
    Lampe_Aus.grid(row=0, column=0, padx=10, pady=10)
    GPIO.output(21, GPIO.HIGH)
    GPIO.output(20, GPIO.LOW)


#  Event detection & Callback Funktion
GPIO.add_event_detect(18, GPIO.RISING)
GPIO.add_event_detect(19, GPIO.RISING)
GPIO.add_event_callback(18, GPIO_Voll)
GPIO.add_event_callback(19, GPIO_Leer)

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

#  Definieren GUI-Knöpfe
Label(frame, text='Kanbanbehälter').grid(row=2, column=1, padx=10, pady=10)
Button(frame, text="Leer", command=GUI_Leer).grid(row=3, column=0, padx=10, pady=10)
Button(frame, text="Voll", command=GUI_Voll).grid(row=3, column=2, padx=10, pady=10)

frame.pack(expand=True)


#  Main Methode
if __name__ == '__main__':
    root.mainloop()