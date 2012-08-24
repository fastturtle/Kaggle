import sys
import csv
import time
from nltk import *
from datetime import datetime
from pprint import pprint
from collections import defaultdict

"""
TO DO:
	1. Pre-process text data to remove unnecessary symbols such as ".", "\", "`", etc...
	2. Implement LancasterStemmer to convert words to their stems.
	3. Change string concatenation in annual_encoder to nltk token list concatenation

"""

class LanguageProcessor():
""" Class for reading and parsing CSV text data. See NLTK package for more information on nltk
	methods (ie. Text(), LancasterStemmer(), etc...)
	Some useful nltk methods that can be used on Text objects are: 
		concordance(word) -- returns context in which word is used
		similar(word) -- returns words that are used in a range of contexts similar to word
		common_contexts(word1, word2) -- returns contexts shared by word1 and word2
		collections() -- builds list of strings containing words that are commonly used together
		FreqDist(text_object) -- returns a FreqDist object that can be searched or plotted with plotting module

		See https://sites.google.com/site/naturallanguagetoolkit/book for more information.

	Usage:
		processor = LanguageProcessor()
		article_data = [article for article in processor.article_encoder(csv_file_loc, date_field, [fields_to_extract])]
		annual_data = processor.annual_encoder(csv_file_loc, date_field[, (fields_to_extract)])

	Notice that the article_encoder and annual_encoder are used differently. annual_encoder returns a dictionary whose keys
	are years and text for each article has been concatenated. article_encoder returns a generator, which should be slightly
	faster.
"""
	def __init__(self):
		self.st = LancasterStemmer() # For extracting word stems...more to come on this later!

	def find_top_10(self, field):
		"""In development"""
		data = self._csv_reader(fname, field)

		for article in data:
			encoded_article = {field: (article[field].lower() if type(article[field]) == str else article[field]) for field in article }

	def article_encoder(self, date_field, fname, *args):
		"""Encodes all fields possible for each article as nltk text objects and returns a generator."""
		data = self._csv_reader(fname, date_field, *args)
		for article in data:
			encoded_article = {field: (Text(article[field].lower()) if type(article[field]) == str else article[field]) for field in article }
			yield encoded_article
	
	def annual_encoder(self, date_field, fname, *args):
		data = self._csv_reader(fname, date_field, *args)
		annual = {}
		for article in data:
			yr = article['date'].year
			# print yr
			if annual.get(yr):
				annual[yr] = {field: annual[yr].get(field, '') + article[field].lower() for field in article if type(article[field]) == str}
			else:
				annual[yr] = {field: article[field].lower() for field in article if type(article[field]) == str}
		
		return annual

	def _csv_reader(self, date_field, fname, args=()):
		""" Private method that decodes a CSV file, adds a date field, removes the unnecessary date field, 
			and returns returns a generator that can loop through each article.				
		"""
		with open(fname, 'rb') as i:
			reader = csv.DictReader(i)

			for row in reader:
				# Create properly formatted date
				row['date'] = datetime.strptime(row[date_field], '%d-%b-%y')
				
				# If no arguments are supplied, return all fields, except for unformatted date information
				if args == ():
					yield {key: row[key] for key in row if key != 'SYSTEM PUB DATE'}
				else:
					yield {key: row[key] for key in args}


if __name__ == "__main__":
	# Uses HBR data found at https://www.kaggle.com/c/harvard-business-review-vision-statement-prospect/data
	fname = sys.argv[1]
	p = LanguageProcessor()
	fields = ('date', 'ABSTRACT')

	article_data =  [article for article in p.article_encoder(fname, 'SYSTEM PUB DATE',fields)]
	annual_data = p.annual_encoder(fname, 'SYSTEM PUB DATE', fields)

	print annual_data[1977]