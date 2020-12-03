from service import analyze
from db import db
import pandas as pd
from os import path
from datetime import datetime
import pathlib
import json
import os
import redis

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
		self.cache = db.Db()


	# take file that's already decoded and in bytes, and do analysis, returning json of results
	def process(self, request_id, file, skip_words, core_words, file_name, persist=False):
		df = pd.DataFrame()
		if skip_words:
			analysis = self.analyzer.parse_file(file, words_to_skip=self.words_to_skip, core_words=core_words)
		else:
			analysis = self.analyzer.parse_file(file, core_words=core_words)
		if (len(analysis) == 0): # analysis turned up empty for words
			json_info = self.create_json_view(df, skip_words, core_words, file_name)
			if persist:
				self.write_result(request_id, json_info)
			return json_info
		df = pd.DataFrame(analysis)
		json_info = self.create_json_view(df, skip_words, core_words, file_name)
		if persist:
			self.write_result(request_id, json_info)
		return json_info

	def get(self, request_id):
		json_info = self.cache.get(request_id)
		if json_info is not None:
			return json.loads(json_info)
		return None

	def get_all(self):
		keys = self.cache.get_all_keys()
		return keys

	# Write json to redis cache for persistence
	def write_result(self, request_id, json):
		self.cache.set(request_id, json)

	def create_json_view(self, df, skip_words, core_words, file_name):
		return json.dumps({
			'data': df.to_json(), 
			'skip_words': skip_words, 
			'core_words': core_words,
			'timestamp': datetime.now().date().isoformat(),
			'file_name': file_name
		})