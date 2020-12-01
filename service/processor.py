from service import analyze
import pandas as pd
from os import path
from datetime import datetime
import pathlib
import json

class Processor:

	def __init__(self, stop_resource='./resources/stopwords.txt'):
		words_to_skip = set()
		script_dir = path.dirname(__file__)
		file_path = path.join(script_dir, stop_resource)
		with open(file_path, 'r') as stop_words_resource:
			for word in stop_words_resource.read().split('\n'):
				words_to_skip.add(word)
		self.words_to_skip = words_to_skip
		self.analyzer = analyze.Analyzer()
		# write_dir = 'output ' + str(datetime.now())
		write_dir_loc = path.join(script_dir, 'resources', 'output', datetime.now().date().isoformat())
		write_dir = pathlib.Path(write_dir_loc).mkdir(parents=True, exist_ok=True)
		self.write_directory = write_dir_loc


	# take file that's already decoded and in bytes, and do analysis, returning pandas df of results
	def process(self, request_id, file, skip_words, core_words, persist=False):
		df = pd.DataFrame()
		if skip_words:
			analysis = self.analyzer.parse_file(file, words_to_skip=self.words_to_skip, core_words=core_words)
		else:
			analysis = self.analyzer.parse_file(file, core_words=core_words)
		if (len(analysis) == 0): # analysis turned up empty for words
			if persist:
				self.write_result(request_id, df, skip_words, core_words)
			return df
		df = pd.DataFrame(analysis)
		if persist:
			self.write_result(request_id, df, skip_words, core_words)
		return df

	# Write dataframe to local file for latter persistence, acting as a primitive storage
	def write_result(self, request_id, df, skip_words, core_words):
		json_info = json.dumps({'dataframe': df.to_json(), 'skip_words': skip_words, 'core_words': core_words})
		file_path = path.join(self.write_directory, request_id)
		with open(file_path, 'w') as write_file:
			write_file.write(json_info)
