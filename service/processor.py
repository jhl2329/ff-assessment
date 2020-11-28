from service import analyze
import pandas as pd
from os import path

class Processor:

	def __init__(self, stop_resource='./resources/stopwords.txt'):
		words_to_skip = set()
		script_dir = path.dirname(__file__)
		file_path = path.join(script_dir, stop_resource)
		with open(file_path, 'r') as stop_words_resource:
			for word in stop_words_resource.read().split('\n'):
				words_to_skip.add(word)
		self.words_to_skip = words_to_skip

		# take file that's already decoded and in bytes, and do analysis, returning pandas df of results
	def process(self, file, skip_words, core_words):
		analysis = analyze.parse_file(file) if not skip_words else analyze.parse_file(file, self.words_to_skip) # list of tuples
		if (len(analysis) == 0): # analysis turned up empty for words
			return pd.DataFrame()
		df = pd.DataFrame(analysis)
		df.columns = ['Word', 'Count']
		return df
