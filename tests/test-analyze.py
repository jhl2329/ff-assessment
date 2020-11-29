import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from service import analyze

class TestMainMethod(unittest.TestCase):

	def test_check_good_run(self):
		file_str = open('tests/resources/sample2.txt', 'r')
		test_analyzer = analyze.Analyzer()
		sorted_list = test_analyzer.parse_file(file_str.read())
		self.assertEqual(len(sorted_list), 25)
		file_str.close()

	def test_check_small_run(self):
		file_str = open('tests/resources/sample.txt', 'r')
		test_analyzer = analyze.Analyzer()
		sorted_list = test_analyzer.parse_file(file_str.read())
		self.assertEqual(len(sorted_list), 5)
		file_str.close()

	def test_possible_valid_root_word(self):
		file_str = open('tests/resources/sample5.txt', 'r')
		test_analyzer = analyze.Analyzer()
		sorted_list = test_analyzer.parse_file(file_str.read(), core_words=True)
		self.assertEqual(len(sorted_list), 2)

		first_val = sorted_list[0]
		self.assertEqual('E', first_val[0])
		self.assertEqual(2, first_val[1])

		'''
			Since algo assumes rest of words are valid, even though there's a rule to replace 'L' with empty space
			(like in the case of EL becoming E), since there is no C in the whole file, algo assumes the 'L' in 'CL'
			is a false suffix and actual word is actually CL.
		'''
		second_val = sorted_list[1]
		self.assertEqual('CL', second_val[0])
		self.assertEqual(2, second_val[1])

		file_str.close()

	def test_casing_doesnt_matter(self):
		file_str = open('tests/resources/sample6.txt' ,'r')
		test_analyzer = analyze.Analyzer()
		result = test_analyzer.parse_file(file_str.read())
		self.assertEqual(len(result), 1)
		file_str.close()


class TestLetters(unittest.TestCase):

	def test_valid_word(self):
		some_word = 'abcd'
		test_analyzer = analyze.Analyzer()
		self.assertTrue(test_analyzer.is_all_letters(some_word))

	def test_invalid_letter(self):
		some_word = '?'
		test_analyzer = analyze.Analyzer()
		self.assertFalse(test_analyzer.is_all_letters(some_word))

	def test_invalid_word(self):
		some_word = 'abc?def'
		test_analyzer = analyze.Analyzer()
		self.assertFalse(test_analyzer.is_all_letters(some_word))

	def test_invalid_word_2(self):
		some_word = 'KMDKâ??L'
		test_analyzer = analyze.Analyzer()
		self.assertFalse(test_analyzer.is_all_letters(some_word))

class TestPuncuation(unittest.TestCase):

	def test_word_punctuation(self):
		some_word = 'DVQ,'
		test_analyzer = analyze.Analyzer()
		self.assertEqual(test_analyzer.process_punctuation(some_word), 'DVQ')

class TestProcessCoreWords(unittest.TestCase):

	def test_core_word(self):
		word = 'ALZ'
		test_analyzer = analyze.Analyzer()
		self.assertEqual('A', test_analyzer.get_resulting_word(word, 'LZ'))

	def test_core_word_suffix_collision(self):
		word = 'ABCPZL'
		test_analyzer = analyze.Analyzer()
		# rule collision but assume suffix replacement with longer suffix takes precedent
		suffix_result = test_analyzer.ends_in_suffix(word)
		self.assertEqual('PZL', suffix_result)
		result = test_analyzer.get_resulting_word(word, suffix_result)
		self.assertNotEqual('ABCA', result)
		self.assertEqual('ABCAZ', result)


if __name__ == '__main__':
	unittest.main()