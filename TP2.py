import csv
import datetime
try:
    from _datetime import *
    from _datetime import __doc__
except ImportError:
    from _pydatetime import *
    from _pydatetime import __doc__

__all__ = ("date", "datetime", "time", "timedelta", "timezone", "tzinfo",
           "MINYEAR", "MAXYEAR", "UTC")

"""
TP2 : Système de gestion de livres pour une bibliothèque

Groupe de laboratoire : 01
Numéro d'équipe :  05
Noms et matricules : TU, Hien-Minh (2377236), ADAOURI, Aymene (2398803)
"""

########################################################################################################## 
# PARTIE 1 : Création du système de gestion et ajout de la collection actuelle
########################################################################################################## 

bibliotheque = {}

with open("collection_bibliotheque.csv", newline='') as dictionnaire:
    dictionnaire = csv.reader(dictionnaire)
    next(dictionnaire)
    for row in dictionnaire:
        bibliotheque[row[3]] = {"titre" : row[0],"auteur" : row[1],"date_publication" : row[2]}

print(f' \n Bibliotheque initiale : {bibliotheque} \n')

########################################################################################################## 
# PARTIE 2 : Ajout d'une nouvelle collection à la bibliothèque
##########################################################################################################

with open("nouvelle_collection.csv", newline='') as new_collection:
    new_collection = csv.reader(new_collection)
    next(new_collection)

    for new_row in new_collection:
        titre_c, auteur_c, date_c, cle_c = new_row[0], new_row[1], new_row[2], new_row[3]
        list_keys = tuple(bibliotheque.keys())[1:]
        if not cle_c in list_keys:
            print(f"Le livre {cle_c} ---- {titre_c} par {auteur_c} ---- a été ajouté avec succès")
            bibliotheque[cle_c] = {"titre" : titre_c,"auteur" : auteur_c,"date_publication" : date_c}
        else:
            print(f"Le livre {cle_c} ---- {titre_c} par {auteur_c} ---- est déjà présent dans la bibliothèque")

########################################################################################################## 
# PARTIE 3 : Modification de la cote de rangement d'une sélection de livres
########################################################################################################## 

for key in tuple(bibliotheque.keys()):
    if bibliotheque[key]["auteur"] == "William Shakespeare":
        bibliotheque["WS" + key[1:]] = bibliotheque.pop(key)

print(f' \n Bibliotheque avec modifications de cote : {bibliotheque} \n')

########################################################################################################## 
# PARTIE 4 : Emprunts et retours de livres
########################################################################################################## 

emprunts_keys = []

with open("emprunts.csv", newline='') as emprunts:
    emprunts = csv.reader(emprunts)
    next(emprunts)
    for key in bibliotheque:
        bibliotheque[key]["emprunts"] = "disponible"
        bibliotheque[key]["date_emprunt"] = "----------"

    for row in emprunts:
        if row[0] in bibliotheque:
            bibliotheque[row[0]]["emprunts"] = "emprunte"
            bibliotheque[row[0]]["date_emprunt"] = row[1]
            emprunts_keys.append(row[0])


print(f' \n Bibliotheque avec ajout des emprunts : {bibliotheque} \n')

########################################################################################################## 
# PARTIE 5 : Livres en retard 
########################################################################################################## 

current_day = datetime.now().strftime("%Y-%m-%d").split("-")
current_day = datetime(*map(int, current_day))

for key in emprunts_keys:
    if bibliotheque[key]["emprunts"] == "emprunte":
        date_emprunt = datetime(*map(int, bibliotheque[key]["date_emprunt"].split("-")))
        retour = (current_day - date_emprunt).days
        if 30 < retour <= 80:
            bibliotheque[key]['frais_retard'] = f"{(retour - 30) * 2}$"
            print(f"Le livre {key} est en retard : frais de {bibliotheque[key]['frais_retard']}")
        elif 80 < retour < 365:
            bibliotheque[key]["frais_retard"] = f"{100}$"
            print(f"Le livre {key} est en retard : frais de {bibliotheque[key]['frais_retard']}")
        elif 365 <= retour:
            bibliotheque[key]["livres_perdus"] = "perdu"

print(f' \n Bibliotheque avec ajout des retards et frais : {bibliotheque} \n')
