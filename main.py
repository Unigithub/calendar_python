import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import date
import json
import os


# définition des variables
month = date.today().month
year = date.today().year
color_case = "#ADD8E6"

# Fonction pour afficher les mois et l'année
def print_Month_Year(month, year):
    month_Names = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    written_Month = month_Names[month - 1]
    month_Year = tkinter.Label(calendarFrame, text=written_Month + " " + str(year), font=("Arial", 22))
    month_Year.grid(column=2, row=0, columnspan=3)


# Fonction pour changer les mois
def switchMonths(direction):
    global calendarFrame
    global month
    global year
    # On check si on change de mois
    if month == 12 and direction == 1:
        month = 0
        year += 1
    if month == 1 and direction == -1:
        month = 13
        year -= 1

    textObjectDict.clear()
    saveDict.clear()

    calendarFrame.destroy()
    calendarFrame = tkinter.Frame(window)
    calendarFrame.grid(padx=10, pady=10)
    print_Month_Year(month + direction, year)
    makeButtons()
    monthGenerator(dayMonthStarts(month + direction, year), daysInMonth(month + direction, year))
    month += direction

# Boutton d'affichage
def makeButtons():
    goBack = tkinter.Button(calendarFrame, text="◄", command=lambda: switchMonths(-1), font=("Arial", 16), width=3)
    goBack.grid(column=0, row=0)
    goForward = tkinter.Button(calendarFrame, text="►", command=lambda: switchMonths(1), font=("Arial", 16), width=3)
    goForward.grid(column=6, row=0)

# Fonction pour calculer si c'est une année bisextile
def is_Leap_Year(year):
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        return True
    else:
        return False

def on_drop(event, day):
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img = img.resize((100, 100), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        day_Images[day].configure(image=img)
        day_Images[day].image = img
        image_Paths[day] = file_path

# Créer le calendrier
def monthGenerator(startDate, numberOfDays):
    day_Names = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

    # Placer les jours de la semaine en haut du calendrier
    for nameNumber in range(len(day_Names)):
        names = tkinter.Label(calendarFrame, text=day_Names[nameNumber], fg="black")
        names.grid(column=nameNumber, row=1, sticky='nsew')

    index = 0
    day = 1
    for row in range(6):
        for column in range(7):
            if index >= startDate and day <= numberOfDays:
                # Créer un cadre pour chaque jour
                dayFrame = tkinter.Frame(calendarFrame, width=100, height=100, highlightbackground="black", highlightthickness=1, bg=color_case)
                dayFrame.grid_propagate(False)
                dayFrame.grid(row=row + 2, column=column, sticky="nsew", padx=3, pady=3)
                dayFrame.columnconfigure(0, weight=1)
                dayFrame.rowconfigure(1, weight=1)

                # Ajouter une étiquette de numéro de jour
                dayNumber = tkinter.Label(dayFrame, text=day, bg=color_case)
                dayNumber.grid(row=0)

                # Ajouter une étiquette pour l'image
                img_label = tkinter.Label(dayFrame, width=100, height=100, bg=color_case)
                img_label.grid(row=1)
                img_label.bind("<Button-1>", lambda e, d=day: on_drop(e, d))

                # Ajouter l'objet image au dictionnaire
                day_Images[day] = img_label
                day += 1
            index += 1
    # Créer les boutons pour save & load JSON's
    loadFrom = tkinter.Button(calendarFrame, text="Load", command=loadFromJSON)
    saveToButton = tkinter.Button(calendarFrame, text="Save", command=saveToJSON)

    # Placer les boutons en bas de l'interface graphique
    loadFrom.grid(row=8, column=4)
    saveToButton.grid(row=8, column=2)

def saveToJSON():
    # Sauvegarder les données textuelles brutes des objets texte
    for day in range(len(textObjectDict)):
        saveDict[day] = textObjectDict[day + 1].get("1.0", "end - 1 chars")

    # Ajouter les chemins des images au dictionnaire de sauvegarde
    for day in range(1, len(day_Images) + 1):
        if day in image_Paths:
            saveDict[f'image_{day}'] = image_Paths[day]
        else:
            saveDict[f'image_{day}'] = None

    # Demander à l'utilisateur l'emplacement d'un fichier et enregistre un JSON contenant le texte de chaque jour.
    fileLocation = filedialog.asksaveasfilename(initialdir="/", title="Save")
    if fileLocation != '':
        with open(fileLocation, 'w') as jFile:
            json.dump(saveDict, jFile)

def loadFromJSON():
    # Demander à l'utilisateur d'ouvrir un fichier JSON
    fileLocation = filedialog.askopenfilename(initialdir="/", title="Select a JSON to open")
    if fileLocation != '':
        f = open(fileLocation)
        global saveDict
        saveDict = json.load(f)

        # Copier les données textuelles sauvegardées dans les objets textuels actuels
        for day in range(len(textObjectDict)):
            textObjectDict[day + 1].insert("1.0", saveDict[str(day)])

        # Recharger les images à partir des paths save
        for day in range(1, len(day_Images) + 1):
            image_path = saveDict.get(f'image_{day}')
            if image_path and os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)
                day_Images[day].configure(image=img)
                day_Images[day].image = img

# Fonction permettant de calculer le jour du début du mois
def dayMonthStarts(month, year):
    # Obtenir les deux derniers chiffres (21 par défaut pour 2021)
    lastTwoYear = year - 2000
    # Division d'un nombre entier par 4
    calculation = lastTwoYear // 4
    # Ajouter le jour du mois (toujours 1)
    calculation += 1
    # Tableau pour l'ajout de la clé de mois appropriée
    month_Keys = [1, 4, 4, 0, 2, 5, 0, 3, 6, 1, 4, 6]
    calculation += month_Keys[month - 1]
    # Vérifier si c'est une année bissextile
    leapYear = is_Leap_Year(year)
    # Soustraire 1 s'il s'agit de janvier ou février d'une année bissextile
    if leapYear and (month == 1 or month == 2):
        calculation -= 1
    # Ajouter le code du siècle (supposons que nous sommes dans les années 2000)
    calculation += 6
    # Ajouter les deux derniers chiffres au calcul
    calculation += lastTwoYear
    # Obtenir un nombre basé sur le calcul (dimanche = 1, lundi =2..... samedi =0)
    dayOfWeek = calculation % 7
    return dayOfWeek

# Fonction pour calculer le nombre de jours dans un mois
def daysInMonth(month, year):
    # Tous les mois qui ont 31 jours
    if month in [1, 3, 5, 7, 8, 10, 12]:
        numberDays = 31
    # Tous les mois qui ont 30 jours
    elif month in [4, 6, 9, 11]:
        numberDays = 30
    else:
        # Vérifier si l'année est bissextile pour déterminer le nombre de jours du mois de février.
        leapYear = is_Leap_Year(year)
        if leapYear:
            numberDays = 29
        else:
            numberDays = 28
    return numberDays

# Contient le texte brut saisi pour chaque jour
saveDict = {}

# Tient les objets textuels chaque jour
textObjectDict = {}

# Tient les objets images pour chaque jour
day_Images = {}

# Tient les paths des images de chaque jour
image_Paths = {}

# Créer la fenêtre principale
window = tkinter.Tk()
window.title("Calendar")
window.geometry("1000x800")

# centrer le calendrier
window.columnconfigure(0, weight=1)

# Créer des frames pour la main root window.
calendarFrame = tkinter.Frame(window, background='#424549')
calendarFrame.grid(padx=10, pady=10)

# Faire apparaître l'objet de la grille
calendarFrame.grid()

today = date.today()

# general
window.configure(background='black')
window.title("calendar_POGO")
window.minsize(480, 360)
window.iconbitmap("calendar.ico")

print_Month_Year(month, year)
makeButtons()
monthGenerator(dayMonthStarts(month, year), daysInMonth(month, year))

# loop pour faire tourner la fenêtre en continu et la rendre interactive
window.mainloop()