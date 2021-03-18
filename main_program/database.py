#!/usr/bin/python
# -*- coding: utf-8 -*-

import mysql.connector as MySQLdb



def seConnecter():
	#Pour modifier la connexion à la base de données, il faut modifier les lignes suivantes
	connexion = MySQLdb.connect(user = "root",  #Database User
								host = "localhost",	 #Database IP (server IP)
								database = "proj632")	 #Database name

	return connexion

def saveBDD(data):
	connexion=seConnecter()
	print("Connecté")
	curseur = connexion.cursor()

	#On sauvegarde chaque element de data
	for d in data:
		profil_exist = False

		requete = "select nom_profil from profil"
		curseur.execute(requete)

		#On verifie que l'utilisateur n'existe pas deja
		#Afin d'éviter les doublons
		for c in curseur.fetchall():
			if d["pseudo"] == c[0]:
				profil_exist = True
		
		#S'il n'existe pas on l'insert
		if(not profil_exist):
			requete = "insert into profil (nom_profil) values ('"+d["pseudo"]+"')"
			curseur.execute(requete)

		#Pour chaqu'une de ses reviews
		for r in d["profil_reviews"]:
			rest_exist = False
			com_exist = False
			
			#On verifie qu'il si le restaurant existe ou non
			requete = "select nom_rest from restaurant"
			curseur.execute(requete)
			for c in curseur.fetchall():
				if r["profil_restaurant"] == c[0]:
					rest_exist = True

			#S'il n'existe pas on le créer
			if(not rest_exist):
				requete = "insert into restaurant(nom_rest) values ('"+r["profil_restaurant"]+"')"
				curseur.execute(requete)

			#On selectionne les id du restaurant et du profil
			requete = "select id_rest, id_profil from profil, restaurant where nom_rest='"+r["profil_restaurant"]+"' and nom_profil='"+d["pseudo"]+"'"
			curseur.execute(requete)
			ids = curseur.fetchone()

			#Si l'utilisateur n'a pas encore commenté dans ce restaurant, on insert le commentaire
			requete = "select id_rest,id_profil from commentaire"
			curseur.execute(requete)
			if not ids in curseur.fetchall():
				try:
					requete = "insert into proj632.commentaire values(" + str(ids[0]) + "," + str(ids[1]) + ",'" + r["profil_text"] + "', '" + r["profil_review_date"] + "'," + str(r["profil_rating"]) + ")"
					curseur.execute(requete)
				except:
					print("Erreur d'insert")


	connexion.commit()