#!/usr/bin/python
# -*- coding: latin-1 -*-
import sys

import csv
import json 
import re

import main_program.database as db
from main_program.scraping import Scrap





def main(url):

	reviews_data = []
	
	scrap = Scrap(url)

	data = scrap.data

	for d in data:
		with open('result/data.txt', 'w') as outfile:
			json.dump(d, outfile, indent = 4)
		db.saveBDD(d)
		
	


#on obtient la page web du restaurant au format html pour mieux pouvoir extraire les données voulues (or00 = page 1)
url = 'https://www.tripadvisor.fr/Restaurant_Review-g150812-d17328287-Reviews-or00-Porfirio_s_Restaurante-Playa_del_Carmen_Yucatan_Peninsula.html'
main(url)