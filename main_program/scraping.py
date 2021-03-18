#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup  
import requests
import re

class Scrap:

	def __init__(self,url):
		self.url_rest = url
		self.set_soup()
		self.set_last_page()
		
		self.tupple_url_soup = []
		self.set_tupple()

		self.data = []
		self.set_data()




	def get_url_rest(self):
		return self.url_rest

	def get_last_page(self):
		return self.last_page

	def get_data(self):
		return self.data

	def get_soup(self):
		return self.soup

	def set_soup(self):
		#on get les données de la page à partir de son url
		r = requests.get(self.url_rest)
		#on extrait le texte brut de la page html 
		html_doc = r.text
		#on cherche à parser la page html 
		self.soup = BeautifulSoup(html_doc, 'html.parser')
		

	def set_last_page(self):
		self.last_page = self.get_soup().find('a', {'class' : 'pageNum last'}).string

	def set_tupple(self):
		url = self.url_rest
		for page in range(0,int(self.last_page)-1):
			page*=10
			if page == 0:
				page = "00"
			
			url = url[:url.find('Reviews')+8] + 'or'+str(page)+'-'+url[url.find('Reviews')+13:]

			r = requests.get(url)
			html_doc = r.text
			soup = BeautifulSoup(html_doc, 'html.parser')

			self.tupple_url_soup.append([url,soup])

	def set_data(self):
		for tupple in self.tupple_url_soup:
			self.data.append(self.scraping(tupple[1]))

	def save_data(self):
		for d in self.data:
			self.data.append(self.scraping(d))

	def scraping(self,soup):
		reviews_data = []
		#on cherche à obtenir toutes les informations de la page qui ont pour tag <a> 
		for review in soup.find_all('div', {'class' : "review-container"}):
			review_data = {}

			#recuperation du pseudo afin d'acceder à son profil
			review_data['pseudo']=(review.find('div', {'class' : 'info_text pointer_cursor'}).div.string).replace("'","\'")

			print("Commentaires de " + review_data["pseudo"])

			#on obtient la page web du restaurant au format html pour mieux pouvoir extraire les données voulues
			url_profil = 'https://www.tripadvisor.fr/Profile/' + review_data['pseudo'] + "?tab=reviews"
			#on get les données de la page à partir de son url
			r_profil = requests.get(url_profil)
			#on extrait le texte brut de la page html
			html_profil = r_profil.text
			#on cherche à parser la page html 
			soup_profil = BeautifulSoup(html_profil, 'html.parser')

			reviews_profil_data = []

			#on cherche à obtenir toutes les informations de la page qui ont pour tag <a> 
			for review_profil in soup_profil.find_all('div', {'class' : "nMewIgXP ui_card section"}):

				review_profil_data = {}

				#On recupere les données qui nous interesse 
				review_profil_data["profil_review_date"] = (review_profil.find('div', {'class' : '_287pE6AZ'}).span.a.string).replace("'"," ")
				#review_profil_data["profil_rest_date"] = review_profil.find('div', {'class' : '_3Coh9OJA'}).get_text()
				review_profil_data["profil_rating"] = int(review_profil.find('span', {'class' : 'ui_bubble_rating'})['class'][1][7:])/10
				review_profil_data["profil_text"] = (review_profil.find('div', {'class' : '_133ThCYf'}).q.get_text()).replace("'"," ")
				review_profil_data["profil_restaurant"] = (review_profil.find('div', {'class' : '_2ys8zX0p'}).string).replace("'"," ")

				reviews_profil_data.append(review_profil_data)
			
			review_data["profil_reviews"] = reviews_profil_data
			
			reviews_data.append(review_data)

		print("fin")

		return reviews_data


