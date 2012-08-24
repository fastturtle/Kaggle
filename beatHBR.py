import sys
import csv
import time
from nltk import *
from datetime import datetime
from pprint import pprint
from collections import defaultdict

class LanguageProcessor():

	def __init__(self):
		self.restrictions = []
		self.st = LancasterStemmer()

	def find_top_10(self, field):
		data = self._csv_reader(fname, field)

		for article in data:
			encoded_article = {field: (article[field].lower() if type(article[field]) == str else article[field]) for field in article }

	def article_encoder(self, fname, *args):
		"""Encodes all fields possible for each article as nltk text objects"""
		data = self._csv_reader(fname, *args)
		# out = []
		for article in data:
			encoded_article = {field: (Text(article[field].lower()) if type(article[field]) == str else article[field]) for field in article }
			yield encoded_article
	
	def annual_encoder(self, fname, *args):
		data = self._csv_reader(fname, *args)
		annual = {}
		for article in data:
			yr = article['date'].year
			# print yr
			if annual.get(yr):
				annual[yr] = {field: annual[yr].get(field, '') + article[field].lower() for field in article if type(article[field]) == str}
			else:
				annual[yr] = {field: article[field].lower() for field in article if type(article[field]) == str}
		
		return annual

	def _csv_reader(self, fname, args=()):
		""" Private method that decodes a CSV file, adds a date field, removes the unnecessary date field, 
			and returns returns a generator that can loop through each article."""
		with open(fname, 'rb') as i:
			reader = csv.DictReader(i)

			for row in reader:
				# Create properly formatted date
				row['date'] = datetime.strptime(row['SYSTEM PUB DATE'], '%d-%b-%y')
				
				# If no arguments are supplied, return all fields, except for unformatted date information
				if args == ():
					yield {key: row[key] for key in row if key != 'SYSTEM PUB DATE'}
				else:
					yield {key: row[key] for key in args}


if __name__ == "__main__":
	fname = sys.argv[1]
	p = LanguageProcessor()
	fields = ('date', 'ABSTRACT')

	article_data =  [article for article in p.article_encoder(fname, fields)]
	annual_data = p.annual_encoder(fname, fields)

	print annual_data[1977]