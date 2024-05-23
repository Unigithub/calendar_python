import tkinter
from tkinter import filedialog
from tkinter import PhotoImage
import os
import sys
import subprocess
import configparser
from PIL import Image, ImageTk
from datetime import date
import json


# défininition des variables
month = date.today().month
year = date.today().year

# Fonction pour afficher les mois et l'année
def print_Month_Year(month, year):
    month_Names = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    written_Month = month_Names[month - 1]
    month_Year = tkinter.Label(calendarFrame,  text = written_Month + " " + str(year), font= ("Arial", 22))
    month_Year.grid(column = 2, row = 0, columnspan = 3)


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
    calendarFrame.grid()
    print_Month_Year(month + direction, year)
    makeButtons()
    monthGenerator(dayMonthStarts(month + direction, year), daysInMonth(month + direction, year))
    month += direction

# Boutton d'affichage
def makeButtons():
    goBack = tkinter.Button(calendarFrame, text = "<", command = lambda : switchMonths(-1))
    goBack.grid(column = 0, row = 0)
    goForward = tkinter.Button(calendarFrame, text = ">", command = lambda : switchMonths(1))
    goForward.grid(column = 6, row = 0)

# Fonction pour calculer si c'est une année bisextile
def isLeapYear(year):
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        return True
    else:
        return False

# Créer le calendrier
def monthGenerator(startDate, numberOfDays):
    
    day_Names = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

    # Placer les jours de la semaine en haut du calendrier
    for nameNumber in range(len(day_Names)):
        names = tkinter.Label(calendarFrame, text = day_Names[nameNumber], fg = "black")
        names.grid(column = nameNumber, row = 1, sticky = 'nsew')

    index = 0
    day = 1
    for row in range(6):
        for column in range(7):
            if index >= startDate and index <= startDate + numberOfDays-1:
                # Créer une chat box pour chaque jour - TODO UPDATE pour les images
                dayFrame = tkinter.Frame(calendarFrame)

                # Créer une boîte de texte à l'intérieur de dayframe
                t = tkinter.Text(dayFrame, width = 15, height = 5)
                t.grid(row = 1)

                # Ajouter l'objet texte au dictionnaire de sauvegarde
                textObjectDict[day] = t 

                # Modifier le cadre du jour pour qu'il soit correctement formaté
                dayFrame.grid(row=row + 2, column=column, sticky = 'nsew')
                dayFrame.columnconfigure(0, weight = 1)
                dayNumber = tkinter.Label(dayFrame, text = day)
                dayNumber.grid(row = 0)
                day += 1
            index += 1
    # Créer les boutons pour save & load JSON's
    loadFrom = tkinter.Button(calendarFrame, text="Load", command = loadFromJSON)
    saveToButton = tkinter.Button(calendarFrame, text="Save", command = saveToJSON)

    # Placer les boutons en bas de l'interface graphique
    loadFrom.grid(row = 8, column = 4)
    saveToButton.grid(row = 8, column = 2)



def saveToJSON():
    # Sauvegarder dles données textuelles brutes des objets texte 
    for day in range(len(textObjectDict)):
        saveDict[day] = textObjectDict[day + 1].get("1.0", "end - 1 chars")

    # Demander à l'utilisateur l'emplacement d'un fichier et enregistre un JSON contenant le texte de chaque jour. 
    fileLocation = filedialog.asksaveasfilename(initialdir = "/", title = "Save JSON to..")
    if fileLocation != '':
        with open(fileLocation, 'w') as jFile:
            json.dump(saveDict, jFile)

def loadFromJSON():
    # Demander à l'utilisateur d'ouvrir un fichier JSON 
    fileLocation = filedialog.askopenfilename(initialdir = "/", title = "Select a JSON to open")
    if fileLocation != '':
        f = open(fileLocation)
        global saveDict
        saveDict = json.load(f)

        # Copie les données textuelles sauvegardées dans les objets textuels actuels
        for day in range(len(textObjectDict)):
            textObjectDict[day + 1].insert("1.0", saveDict[str(day)])


# Fonction permettant de calculer le jour du début du mois
def dayMonthStarts(month, year):
    # Obtenir les deux derniers chiffres (21 par défaut pour 2021)
    lastTwoYear = year - 2000
    # Division d'un nombre entier par 4
    calculation = lastTwoYear // 4
    # Ajouter le jour du mois (toujours 1)
    calculation += 1
    # Tableau pour l'ajout de la clé de mois appropriée
    if month == 1 or month == 10:
        calculation += 1
    elif month == 2 or month == 3 or month == 11:
        calculation += 4
    elif month == 5:
        calculation += 2
    elif month == 6:
        calculation += 5
    elif month == 8:
        calculation += 3
    elif month == 9 or month == 12:
        calculation += 6
    else:
        calculation += 0
    # Vérifier si c'est une année bissextile
    leapYear = isLeapYear(year)
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
def daysInMonth (month, year):
    # Tous les mois qui ont 31 jours
    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 12 or month == 10:
        numberDays = 31
    # Tous les mois qui ont 30 jours
    elif month == 4 or month == 6 or month == 9 or month == 11:
        numberDays = 30
    else:
        # Vérifier si l'année est bissextile pour déterminer le nombre de jours du mois de février.
        leapYear = isLeapYear(year)
        if leapYear:
            numberDays = 29
        else:
            numberDays = 28
    return numberDays

# Contient le texte brut saisi pour chaque jour
saveDict = {}

# Tient les objets textuels chaque jour
textObjectDict = {}

# Créer the main windows
window = tkinter.Tk()
window.title("Calender")
window.geometry("1000x800")

# centrer le calendrier
window.columnconfigure(0, weight = 1)

# Créer des frames pour la main root window.
calendarFrame = tkinter.Frame(window)

# Faire apparaître l'objet de la grille
calendarFrame.grid()

today = date.today()

# general
window.configure(background = '#424549')
window.title("calandar_POGO")
window.minsize(480, 360)
window.iconbitmap("calendar.ico")

print_Month_Year(month, year)
makeButtons()
monthGenerator(dayMonthStarts(month, year), daysInMonth(month, year))

# loap pour faire tourner la fenêtre en continue et la rendre interactive
window.mainloop()