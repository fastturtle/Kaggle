"""
Creates a benchmark by predicting the most popular skus in each category
"""

from collections import defaultdict
import csv
from nltk import *

wd = "../../data/downloaded/small/"
wd = ""
def get_popular_skus():
	"""Returns a dictionary of the most popular skus in each category"""
	with open(wd + "train.csv") as infile:
		reader = csv.reader(infile, delimiter=",")
		reader.next() # burn the header

		queries = defaultdict(lambda: defaultdict(int))

		for (user, sku, category, query, click_time, query_time) in reader:
			query = query.lower()
			queries[query][sku] += 1

		for query in queries:
			queries[query] = sorted(queries[query].items(), key=lambda x: x[1])
			queries[query].reverse()
		return queries

def make_predictions(queries):
	"""Write the predictions out"""
	with open(wd + "test.csv") as infile:
		reader = csv.reader(infile, delimiter=",")
		reader.next() # burn the header
		with open("popular_skus.csv", "w") as outfile:
			writer = csv.writer(outfile, delimiter=",")
			# writer.writerow(["sku"])
			for (user, category, query, click_time, query_time) in reader:
				try:
					query = query.lower()
					guesses = [x[0] for x in queries[query][0:5]]
					writer.writerow([" ".join(guesses)])
				except TypeError:
					writer.writerow(["0"])

def build_haystack():


def main():
	"""Creates the benchmark"""
	queries = get_popular_skus()
	make_predictions(queries)

if __name__ == "__main__":
	main()
