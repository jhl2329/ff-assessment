import unittest
import sys
import os
import uuid
import pandas as pd
import json
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

from service import processor

class TestSkipWords(unittest.TestCase):

	def test_skip(self):
		# set up input file and set to skip
		input_file = open('tests/resources/sample4.txt', 'r')
		test_processor = processor.Processor('../tests/resources/test-stop.txt')

		# get result of processor
		json_result = test_processor.process(str(uuid.uuid4()), input_file.read(), True, True, 'testfile')
		self.assertTrue(json_result is not None)
		j = json.loads(json_result)
		df = pd.read_json(j['data'])
		self.assertEqual(len(df), 2)
		input_file.close()

	def test_dont_skip(self):
		input_file = open('tests/resources/sample4.txt', 'r')
		test_processor = processor.Processor('../tests/resources/test-stop.txt')

		# get result of processor
		json_result = test_processor.process(str(uuid.uuid4()), input_file.read(), False, True, 'testfile')
		self.assertTrue(json_result is not None)
		j = json.loads(json_result)
		df = pd.read_json(j['data'])
		self.assertEqual(len(df), 4)
		input_file.close()

if __name__ == '__main__':
	unittest.main()