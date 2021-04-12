import sys

import csv
import json
import re


from main_program.database import Database
from main_program.scraping import Scrap


def main():
    url = menu()

    reviews_data = []

    scrap = Scrap(url)

    data = scrap.data

    saisie = askSave()
    list_to_replace = ["/", "\\", ":", "<", ">", "|"]
    foldername = url
    for c in list_to_replace:
        foldername = foldername.replace(c, "")

    if(saisie == "1"):
        db = Database()
    for d in data:
        with open('result/' + foldername + '.json', 'w', encoding='utf8') as outfile:
            json.dump(d, outfile, indent=4, ensure_ascii=False)
        if(saisie == "1"):
            db.saveBDD(d)

        

def askSave():
    choix = ["1", "2"]
    print("Voulez-vous sauvegarder les données dans la BDD")
    print("1/ Oui")
    print("2/ Non")
    saisie = input()
    if(saisie not in choix):
        print("Erreur saisie")
        askSave()
    return saisie


def menu():
    url = input("Saisir l'url d'un restaurant: ")
    if(url == ""):
        url = "https://www.tripadvisor.fr/"
        url += "Restaurant_Review-g150812-d17328287-Reviews-or00-"
        url += "Porfirio_s_Restaurante-Playa_del_Carmen_Yucatan_Peninsula.html"
    url.replace("Reviews-", "Reviews-or00-")
    return url


main()
