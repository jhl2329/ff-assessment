import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from service import analyze

class TestMainMethod(unittest.TestCase):

	def test_check_good_run(self):
		file_str = open('tests/resources/sample2.txt', 'r')
		sorted_list = analyze.parse_file(file_str.read())
		self.assertEqual(len(sorted_list), 25)
		file_str.close()

	def test_check_small_run(self):
		file_str = open('tests/resources/sample.txt', 'r')
		sorted_list = analyze.parse_file(file_str.read())
		self.assertEqual(len(sorted_list), 5)
		file_str.close()

class TestLetters(unittest.TestCase):

	def test_valid_word(self):
		some_word = 'abcd'
		self.assertTrue(analyze.is_all_letters(some_word))

	def test_invalid_letter(self):
		some_word = '?'
		self.assertFalse(analyze.is_all_letters(some_word))

	def test_invalid_word(self):
		some_word = 'abc?def'
		self.assertFalse(analyze.is_all_letters(some_word))

	def test_invalid_word_2(self):
		some_word = 'KMDKâ??L'
		self.assertFalse(analyze.is_all_letters(some_word))

class TestPuncuation(unittest.TestCase):
	def test_word_punctuation(self):
		some_word = 'DVQ,'
		self.assertEqual(analyze.process_punctuation(some_word), 'DVQ')

class TestProcessCoreWords(unittest.TestCase):
	def test_core_word(self):
		word = 'ALZ'
		self.assertEqual('A', analyze.process_suffix(word))

	def test_core_word_casing(self):
		word = 'alz'
		self.assertEqual('a', analyze.process_suffix(word))

	def test_core_word_replace(self):
		word = 'ABCPZL'
		# rule collision but assume suffix replacement with longer suffix takes precedent
		result = analyze.process_suffix(word)
		self.assertNotEqual('ABCA', result)
		self.assertEqual('ABCAZ', result)

	def test_core_word_replace_casing(self):
		word = 'abcPzL'
		self.assertEqual('abcAZ', analyze.process_suffix(word))

	def test_core_word_replace_none(self):
		word = 'Jae'
		self.assertEqual('Jae', analyze.process_suffix(word))

if __name__ == '__main__':
	unittest.main()