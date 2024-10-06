import csv
from datetime import *

"""
TP2 : Système de gestion de livres pour une bibliothèque

Groupe de laboratoire : 01
Numéro d'équipe :  05
Noms et matricules : TU, Hien-Minh (2377236), ADAOURI, Aymene (2398803)
"""

##########################################################################################################
# PARTIE 1 : Création du système de gestion et ajout de la collection actuelle
##########################################################################################################

with open('collection_bibliotheque.csv', newline='') as premiere_collection:
    premiere_collection = csv.DictReader(premiere_collection)
    bibliotheque = {}

    for row in premiere_collection:
        bibliotheque[row['cote_rangement']] = {"titre" : row["titre"], "auteur" : row["auteur"], "date_publication" : row["date_publication"]}

print(f' \n Bibliotheque initiale : {bibliotheque} \n')

##########################################################################################################
# PARTIE 2 : Ajout d'une nouvelle collection à la bibliothèque
##########################################################################################################

with open('nouvelle_collection.csv', newline='') as nouvelle_collection:
    nouvelle_collection = csv.DictReader(nouvelle_collection)

    for row in nouvelle_collection:
        if row['cote_rangement'] not in bibliotheque.keys():
            bibliotheque[row['cote_rangement']] = {"titre" : row["titre"], "auteur" : row["auteur"], "date_publication" : row["date_publication"]}
            print(f"Le livre {row['cote_rangement']} ---- {row['titre']} par {row['auteur']} ---- a été ajouté avec succès")
        else:
            print(f"Le livre {row['cote_rangement']} ---- {row['titre']} par {row['auteur']} ---- est déjà présent dans la bibliothèque")


##########################################################################################################
# PARTIE 3 : Modification de la cote de rangement d'une sélection de livres
##########################################################################################################

for cote in tuple(bibliotheque.keys()):
    if bibliotheque[cote]["auteur"] == "William Shakespeare":
        bibliotheque["WS" + cote[1:]] = bibliotheque.pop(cote)

print(f' \n Bibliotheque avec modifications de cote : {bibliotheque} \n')

##########################################################################################################
# PARTIE 4 : Emprunts et retours de livres
##########################################################################################################

emprunts_cote = []

with open("emprunts.csv", newline='') as emprunts:
    emprunts = csv.DictReader(emprunts)
    for cote in bibliotheque.keys():
        bibliotheque[cote]["emprunts"] = "disponible"

    for row in emprunts:
        if row['cote_rangement'] in bibliotheque.keys():
            bibliotheque[row['cote_rangement']]["emprunts"] = "emprunté"
            bibliotheque[row['cote_rangement']]["date_emprunt"] = row['date_emprunt']
            emprunts_cote.append(row['cote_rangement'])

print(f'\n Bibliotheque avec ajout des emprunts : {bibliotheque} \n')

##########################################################################################################
# PARTIE 5 : Livres en retard
##########################################################################################################

current_day = datetime.now().strftime("%Y-%m-%d").split("-")
current_day = datetime(*map(int, current_day))

for cote in emprunts_cote:
    if bibliotheque[cote]["emprunts"] == "emprunté":
        date_emprunt = datetime(*map(int, bibliotheque[cote]["date_emprunt"].split("-")))
        retour = (current_day - date_emprunt).days
        if 30 < retour <= 80:
            bibliotheque[cote]['frais_retard'] = f"{(retour - 30) * 2}$"
            print(f"Le livre {cote} est en retard : frais de {bibliotheque[cote]['frais_retard']}")
        elif 80 < retour < 365:
            bibliotheque[cote]["frais_retard"] = f"100$"
            print(f"Le livre {cote} est en retard : frais de {bibliotheque[cote]['frais_retard']}")
        elif 365 <= retour:
            bibliotheque[cote]["livres_perdus"] = "perdu"
            bibliotheque[cote]["frais_retard"] = f"100$"
            print(f"Le livre {cote} est en retard : frais de {bibliotheque[cote]['frais_retard']}")

print(f' \n Bibliotheque avec ajout des retards et frais : {bibliotheque} \n')