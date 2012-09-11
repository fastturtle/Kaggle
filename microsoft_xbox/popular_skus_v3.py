"""
Creates a benchmark by predicting the most popular skus in each category
"""
from __future__ import division
from collections import defaultdict
import csv
import nltk
import operator
from datetime import datetime
# from numpy import *

wd = "../../data/downloaded/small/"
wd = ""

def get_popular_skus():
	"""Returns a dictionary of the most popular skus in each category"""
	with open(wd + "train.csv") as infile:
		reader = csv.reader(infile, delimiter=",")
		reader.next() # burn the header

		queries = defaultdict(lambda: defaultdict(int))
		# words = []
		words = defaultdict(list)

		for (user, sku, category, query, click_time, query_time) in reader:
			query = query.lower()
			queries[query][sku] += 1

			# Create list of words used in queries
			tokens = query.split(" ")
			words[query] = tokens

		for query in queries:
			queries[query] = sorted(queries[query].items(), key=lambda x: x[1])
			queries[query].reverse()
		return queries, words

def make_predictions(queries, haystack):
	"""Write the predictions out"""
	with open(wd + "test.csv") as infile:
		reader = csv.reader(infile, delimiter=",")
		reader.next() # burn the header
		i = 0
		with open("popular_skus.csv", "w") as outfile:
			writer = csv.writer(outfile, delimiter=",")
			# writer.writerow(["sku"])
			for (user, category, query, click_time, query_time) in reader:
				i += 1
				if i%100 == 0: print "Processed %d rows" % i
				try:
					query = query.lower()
					best_match = search_haystack(query, haystack)

					guesses = [x[0] for x in queries[best_match][0:5]]

					writer.writerow([" ".join(guesses)])

				except TypeError:
					writer.writerow(["0"])

def search_haystack(query, haystack):
	matches = {}
	query_tokens = query.split(" ")

	# Look through the haystack and return the length of intersection of
	# words in query with words in sentence.
	# Make this more efficient!!!

	# t1 = datetime.now()
	for sentence in haystack:
		setnence_tokens = haystack[sentence]
		rank = len(set(setnence_tokens).intersection(query_tokens)) / len(setnence_tokens)
		matches[sentence] = rank

	sorted_matches = sorted(matches.iteritems(), key=operator.itemgetter(1) \
							, reverse=True)

	best_match = ""
	for match in sorted_matches[:5]:
		if match[1] == 1.0 and len(match[0]) > len(best_match):
			best_match = match[0]

	# if best_match == "":
	# 	print query, sorted_matches[:5]

	return best_match

def main():
	"""Creates the benchmark"""
	queries, words = get_popular_skus()
	make_predictions(queries, words)

if __name__ == "__main__":
	main()
